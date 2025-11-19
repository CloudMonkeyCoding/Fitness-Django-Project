from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    """
    Extra info for a student linked to Django's built-in User.
    Login/auth uses User (username / password), this stores fitness info.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    section = models.CharField(max_length=50)

    # Optional: cache last update time for quick display in tables
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.section})"


class FitnessTestEntry(models.Model):
    """
    One row = one test (pre or post) for one student.
    Used for pre-test entry, post-test update, personal dashboard,
    and class analytics.
    """
    PRETEST = "pre"
    POSTTEST = "post"
    TEST_TYPE_CHOICES = [
        (PRETEST, "Pre-test"),
        (POSTTEST, "Post-test"),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="tests")
    test_type = models.CharField(max_length=4, choices=TEST_TYPE_CHOICES)

    # Raw physical values (these feed your charts)
    bmi = models.DecimalField(max_digits=5, decimal_places=2)
    vo2_max = models.DecimalField(max_digits=5, decimal_places=2)
    flexibility = models.DecimalField(max_digits=5, decimal_places=2)
    strength = models.DecimalField(max_digits=5, decimal_places=2)
    agility = models.DecimalField(max_digits=5, decimal_places=2)
    speed = models.DecimalField(max_digits=5, decimal_places=2)
    endurance = models.DecimalField(max_digits=5, decimal_places=2)

    # When this test was taken / last edited
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} - {self.get_test_type_display()} ({self.created_at.date()})"


class Remark(models.Model):
    """
    Teacher/admin remarks history log for a student.
    Shown in personal progress dashboard + teacher view.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="remarks")
    # Optional link to a specific test entry
    fitness_test = models.ForeignKey(
        FitnessTestEntry, on_delete=models.SET_NULL, null=True, blank=True, related_name="remarks"
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        who = self.author.username if self.author else "System"
        return f"Remark for {self.student} by {who} on {self.created_at.date()}"

from django.db import models

class AdminAccount(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # You can hash it later if needed

    def __str__(self):
        return self.username
