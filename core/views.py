from django.shortcuts import render

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


def admin_page(request):
    # custom admin page (NOT Django’s /admin/ site)
    return render(request, "admin.html")
