"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),  # Django's built-in admin

    # Your app pages:
    path("", views.signup, name="signup"),
    path("student-dashboard", views.dashboard, name="dashboard"),  # homepage
    path("personal-progress/", views.personal_progress, name="personal_progress"),
    path("class-analytics/", views.class_analytics, name="class_analytics"),
    path("pre-test-form/", views.pre_test_form, name="pre_test_form"),
    path("posttest/", views.post_test_entry, name="posttest"),
    path("student-management/", views.student_management, name="student_management"),
    path("student-progress/", views.student_progress, name="student_progress"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("update-profile-posttest/", views.update_profile_posttest, name="update_profile_posttest"),
    path("view-student/", views.view_student, name="view_student"),
    path("custom-admin/", views.admin_page, name="custom_admin_page"),  # your admin.html
    path('login/', views.admin_login, name='admin_login'),
    path('admin/', views.admin_page, name='admin_page'),
]
