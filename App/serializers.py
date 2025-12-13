from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *

class TelegramAuthSerializer(serializers.Serializer):
    init_data   = serializers.CharField()
    telegram_id = serializers.CharField()
    auth_date   = serializers.IntegerField()
    hash        = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'credits']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']


class UserInfoSerializer(serializers.ModelSerializer):
    passed_course = CourseSerializer(many=True, read_only=True)  
    faculty = FacultySerializer(read_only=True)         

    class Meta:
        model = Student
        fields = ['name', 'code', 'coin', 'term', 'passed_course', 'faculty', 'last_time_energy', 'current_energy']


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    telegram_id = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(), required=True)
    
    class Meta:
        model = Student
        fields = ['name', 'telegram_id', 'code', 'faculty']


    def validate_code(self, value):
        # بررسی که کد دانشجویی قبلاً ثبت شده یا نه
        if Student.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                "کد دانشجویی از قبل در دیتابیس ما ثبت شده است."
            )

        if len(value) < 9 or len(value) > 10:
            raise serializers.ValidationError("کد دانشجویی باید یا 9 یا 10 کاراکتر باشد.")
        
        return value

    def validate_faculty(self, value):
        # چک کردن اینکه دانشکده وجود دارد یا نه
        if not Faculty.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("دانشکده انتخاب شده وجود ندارد.")
        
        return value
    
    def create(self, validated_data):
        try:
            name = validated_data['name']
            telegram_id = validated_data['telegram_id']
            code = validated_data['code']
            faculty = validated_data['faculty']

            student = Student.objects.create(
                name=name,
                telegram_id=telegram_id,
                code=code,
                faculty=faculty
            )

            return student
        except Exception as e:
            raise ValidationError(f"خطا در ایجاد دانشجو: {str(e)}")
        
        
class UpdateCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['coin', 'last_time_energy', 'current_energy']


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'name', 'chance']

class CourseSerializer(serializers.ModelSerializer):
    professors = ProfessorSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'credits', 'price', 'prerequisite', 'professors', 'status']

    def get_status(self, course):
        student = self.context.get("student")

        if "passed_units_counter" not in self.context:
            self.context["passed_units_counter"] = 0

        sc = StudentCourse.objects.filter(student=student, course=course).first()

        # هنوز برنداشته
        if not sc:
            return {
                "passed": "❌",
                "professor": None
            }

        # برداشته ولی پاس نکرده
        if not sc.passed:
            return {
                "passed": "❔",
                "professor": ProfessorSerializer(sc.professor).data
            }

        #تعداد واحد های پاس شده
        self.context["passed_units_counter"] += course.credits

        #پاس شده
        return {
            "passed": "✅",
            "professor": ProfessorSerializer(sc.professor).data
        }


class CurrentCourseSerializer(serializers.Serializer):
    course       = serializers.CharField()
    credit       = serializers.IntegerField()
    prerequisite = serializers.CharField(allow_null=True)
    professor    = serializers.CharField()