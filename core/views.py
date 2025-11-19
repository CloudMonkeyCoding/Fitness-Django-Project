from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PreTestForm, StudentLoginForm, StudentSignupForm
from .models import StudentProfile

# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")

def signup(request):
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

    return render(request, "signup.html", {
        "form": signup_form,          # register form
        "login_form": login_form,     # login form
    })

def login_view(request):
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

    return render(request, "signup.html", {
        "form": signup_form,
        "login_form": login_form,
    })



def personal_progress(request):
    return render(request, "personalprogress.html")


def class_analytics(request):
    return render(request, "classanalytics.html")


@login_required
def pre_test_form(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        form = PreTestForm(request.POST)
        if form.is_valid():
            form.save(student_profile)
            messages.success(request, "Pre-test data saved successfully.")
            return redirect("student_progress")
    else:
        form = PreTestForm()

    return render(request, "pre-testform.html", {"form": form})


@login_required
def pretest_entry(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        form = PreTestForm(request.POST)
        if form.is_valid():
            form.save(student_profile)
            messages.success(request, "Pre-test data saved successfully.")
            return redirect("pretest_entry")
    else:
        form = PreTestForm()

    return render(request, "pretest-entry.html", {"form": form})


def student_management(request):
    return render(request, "studentmanagement.html")


def student_progress(request):
    return render(request, "studentprogress.html")


def update_profile(request):
    return render(request, "updateprofile.html")


def update_profile_posttest(request):
    return render(request, "updateprofileposttest.html")


def view_student(request):
    return render(request, "viewstudent.html")


def admin_page(request):
    # custom admin page (NOT Django’s /admin/ site)
    return render(request, "admin.html")
