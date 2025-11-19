from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PostTestForm, PreTestForm, StudentLoginForm, StudentSignupForm
from .models import FitnessTestEntry, StudentProfile

# Create your views here.


def ensure_auth_tables():
    """Run migrations lazily if the auth tables are missing."""

    User = get_user_model()
    try:
        User.objects.exists()
    except OperationalError:
        call_command("migrate", interactive=False, run_syncdb=True)


def dashboard(request):
    return render(request, "dashboard.html")


def latest_valid_entry(student_profile: StudentProfile, test_type: str):
    """
    Return the newest FitnessTestEntry for the given student/test type that has
    valid decimal values.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, bmi, vo2_max, flexibility, strength, agility, speed, endurance
            FROM core_fitnesstestentry
            WHERE student_id = %s AND test_type = %s
            ORDER BY created_at DESC
            """,
            [student_profile.id, test_type],
        )
        rows = cursor.fetchall()

    for row in rows:
        entry_id, *metric_values = row
        try:
            [Decimal(str(value)) for value in metric_values]
        except (InvalidOperation, TypeError, ValueError):
            continue

        return FitnessTestEntry.objects.filter(pk=entry_id).first()
    return None


def signup(request):
    ensure_auth_tables()

    if request.method == "POST":
        signup_form = StudentSignupForm(request.POST)
        login_form = StudentLoginForm()  # empty, for the login panel

        if signup_form.is_valid():
            user, profile = signup_form.save()
            login(request, user)
            return redirect("pre_test_form")
    else:
        signup_form = StudentSignupForm()
        login_form = StudentLoginForm()

    return render(
        request,
        "signup.html",
        {
            "form": signup_form,  # register form
            "login_form": login_form,  # login form
            "active_panel": "register",
        },
    )


def login_view(request):
    ensure_auth_tables()

    if request.method == "POST":
        login_form = StudentLoginForm(request.POST)
        signup_form = StudentSignupForm()  # empty, for the register panel

        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            login(request, user)
            return redirect("pre_test_form")
    else:
        login_form = StudentLoginForm()
        signup_form = StudentSignupForm()

    return render(
        request,
        "signup.html",
        {
            "form": signup_form,
            "login_form": login_form,
            "active_panel": "login",
        },
    )



def personal_progress(request):
    return render(request, "personalprogress.html")


def class_analytics(request):
    return render(request, "classanalytics.html")


@login_required
def pre_test_form(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    active_tab = "post" if request.GET.get("tab") == "post" else "pre"
    force_new_post = request.GET.get("new") == "post"

    if force_new_post:
        active_tab = "post"

    pre_latest = latest_valid_entry(student_profile, FitnessTestEntry.PRETEST)
    post_latest = latest_valid_entry(student_profile, FitnessTestEntry.POSTTEST)

    pre_initial = None
    post_initial = None

    if force_new_post:
        post_initial = None

    if pre_latest:
        pre_initial = {
            "vo2_max": pre_latest.vo2_max,
            "flexibility": pre_latest.flexibility,
            "strength": pre_latest.strength,
            "agility": pre_latest.agility,
            "speed": pre_latest.speed,
            "endurance": pre_latest.endurance,
        }

    if post_latest and not force_new_post:
        post_initial = {
            "vo2_max": post_latest.vo2_max,
            "flexibility": post_latest.flexibility,
            "strength": post_latest.strength,
            "agility": post_latest.agility,
            "speed": post_latest.speed,
            "endurance": post_latest.endurance,
        }

    if request.method == "POST":
        active_tab = request.POST.get("active_tab", active_tab)
        force_new_post = force_new_post or request.POST.get("new_post") == "1"

        if active_tab == "post":
            post_form = PostTestForm(request.POST)
            pre_form = PreTestForm(initial=pre_initial)
            if post_form.is_valid():
                post_form.save(student_profile)
                messages.success(request, "New post-test entry saved successfully.")
                return redirect("student_progress")
        else:
            pre_form = PreTestForm(request.POST)
            post_form = PostTestForm(initial=post_initial)
            if pre_form.is_valid():
                pre_form.save(student_profile)
                messages.success(request, "Pre-test data saved successfully.")
                return redirect("student_progress")
    else:
        pre_form = PreTestForm(initial=pre_initial)
        post_form = PostTestForm(initial=None if force_new_post else post_initial)

    return render(
        request,
        "test-entry.html",
        {
            "pre_form": pre_form,
            "post_form": post_form,
            "active_tab": active_tab,
            "new_post": force_new_post,
        },
    )


@login_required
def post_test_entry(request):
    redirect_url = f"{reverse('pre_test_form')}?tab=post"
    if request.method == "POST":
        return redirect(redirect_url)
    return redirect(redirect_url)


def student_management(request):
    return render(request, "studentmanagement.html")


@login_required
def student_progress(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    pre_test_entry = latest_valid_entry(student_profile, FitnessTestEntry.PRETEST)
    post_test_entry = latest_valid_entry(student_profile, FitnessTestEntry.POSTTEST)

    return render(
        request,
        "studentprogress.html",
        {
            "pre_test": pre_test_entry,
            "post_test": post_test_entry,
        },
    )


def update_profile(request):
    return render(request, "updateprofile.html")


def update_profile_posttest(request):
    return render(request, "updateprofileposttest.html")


def view_student(request):
    return render(request, "viewstudent.html")


def admin_page(request):
    # custom admin page (NOT Django’s /admin/ site)
    return render(request, "admin.html")
