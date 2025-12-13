from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "telegram_id", "coin", "term", "faculty", "current_energy")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("faculty", "get_professors", "name", "price", "credits", "prerequisite")

    def get_professors(self, obj):
        return ", ".join([p.name for p in obj.professors.all()])

    get_professors.short_description = "Professors"

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("name", "chance")

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "professor", "passed")

