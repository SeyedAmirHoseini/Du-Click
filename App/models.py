from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Faculty(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "دانشکده ها"

    def __str__(self):
        return self.name


class Professor(models.Model):
    name   = models.CharField(max_length=40, null=False, verbose_name="نام درس")
    chance = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="شانش موفقیت",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name_plural = "اساتید"

    def __str__(self):
        return f"استاد {self.name}"


class Course(models.Model):
    faculty      = models.ForeignKey(Faculty,on_delete=models.CASCADE, related_name="courses", db_index=True)
    professors   = models.ManyToManyField(Professor, related_name="professor_courses")
    name         = models.CharField(max_length=50)
    price        = models.IntegerField(default=0)
    credits      = models.PositiveIntegerField(verbose_name="واحد درسی")
    prerequisite = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_courses', verbose_name="پیش نیاز")

    class Meta:
        verbose_name_plural = "کلاس ها"
        
    def __str__(self):
        return self.name


class Student(models.Model):
    telegram_id      = models.CharField(max_length=100, unique=True, verbose_name="آیدی تلگرام", db_index=True)
    name             = models.CharField(max_length=60, verbose_name="نام")
    code             = models.CharField(max_length=9, null=False, unique=True, verbose_name="کد دانشجویی")
    coin             = models.IntegerField(default=0, verbose_name="تعداد سکه")
    term             = models.PositiveIntegerField(default=1, verbose_name="ترم")
    faculty          = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="students", verbose_name="دانشکده")
    last_time_energy = models.DateTimeField(default=timezone.now, verbose_name="زمان آخرین انرژی ثبت شده")
    current_energy   = models.IntegerField(default=0, verbose_name="مقدار انرژی فعلی")

    def max_energy(self):
        return self.term * 1000
    
    # دستی ریست کردن انرژی 
    def reset_energy(self):
        self.current_energy = self.max_energy()
        self.last_time_energy = timezone.now()
        self.save()

    # رفرش دستی انرژی
    def refresh_energy(self):
        now = timezone.now()
        print(f"now: {now}, last time: {self.last_time_energy}")
        elapsed_seconds = (now - self.last_time_energy).total_seconds()

        if elapsed_seconds >= 3600:
            self.current_energy = self.max_energy()

        else:
            energy_rate = self.max_energy() / 3600
            extra_energy = round(elapsed_seconds * energy_rate)
            print(f"enghadr energy gereft: {extra_energy}")
            self.current_energy = min(self.current_energy + extra_energy, self.max_energy()) 
            self.save()

    class Meta:
        verbose_name_plural = "دانشجویان"

    def __str__(self):
        return f"{self.name}({self.code})" 


class StudentCourse(models.Model):
    student   = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="courses")
    course    = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name="student_courses")

    passed  = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "کلاس های دانشجویان"

    def __str__(self):
        return f"{self.student} - {self.course} ({'Passed' if self.passed else 'Current'})"