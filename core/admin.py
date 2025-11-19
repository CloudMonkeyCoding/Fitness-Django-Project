from django.contrib import admin
from .models import StudentProfile, FitnessTestEntry, Remark

admin.site.register(StudentProfile)
admin.site.register(FitnessTestEntry)
admin.site.register(Remark)