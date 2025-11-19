from django.core.checks import messages
from django.shortcuts import render, redirect
from core.models import AdminAccount


# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")


def signup(request):
    return render(request, "signup.html")


def personal_progress(request):
    return render(request, "personalprogress.html")


def class_analytics(request):
    return render(request, "classanalytics.html")


def pre_test_form(request):
    return render(request, "pre-testform.html")


def pretest_entry(request):
    return render(request, "pretest-entry.html")


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


def custom_admin_page(request):
    # custom admin page (NOT Django’s /admin/ site)
    return render(request, "admin.html")


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'login.html')

        try:
            # Try to get the admin account
            admin = AdminAccount.objects.get(username=username)

            # Check if password matches
            if admin.password == password:
                # Login successful
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                return redirect('admin_page')
            else:
                messages.error(request, 'Invalid password')
                return render(request, 'login.html')

        except AdminAccount.DoesNotExist:
            messages.error(request, 'Username does not exist')
            return render(request, 'login.html')

    return render(request, 'login.html')
def admin_page(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')
    return render(request, 'admin_page.html')
