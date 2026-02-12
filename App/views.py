from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings
from .models import *
from .serializers import *
from .utils import *
from .bot import *
import json, os


class TelegramAuthClass:
    def validate_telegram_request(self, request_data):
        init_data = request_data.get('init_data')
        telegram_id = request_data.get('telegram_id')
        auth_date = request_data.get('auth_date')
        telegram_hash = request_data.get('hash')

        if not telegram_id or not telegram_hash or not auth_date:
            return False, Response({"status": "error", "message": "Invalid data"}, status=400)

        if not validate_telegram_hash(init_data):
            return False, Response({"status": "error", "message": "Unauthorized request"}, status=403)

        if not is_recent_auth(auth_date):
            return False, Response({"status": "error", "message": "Request expired"}, status=403)

        return True, telegram_id


@csrf_exempt
async def webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            update = Update.de_json(data, None)

            if 'message' in data:
                message = data['message']
                print(f"Message received: {message['text']}")
                
                if message['text'] == '/start':
                    await handle_start_command(update)
                    return JsonResponse({"status": "success", "message": "Start command executed"})
                else:
                    await handle_unknown_command(update)
                    return JsonResponse({"status": "success", "message": "Unknown command handled"})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "ignored", "message": "Method not allowed, request ignored"}, status=405)


def protected_js(request, filename):
    # گرفتن Referer از هدر HTTP
    referer = request.META.get('HTTP_REFERER', '')
    current_host = request.get_host()

    # بررسی اینکه آیا درخواست از سایت خودمون اومده
    if not referer or (current_host not in referer):
        return HttpResponse("Forbidden", status=403)

    # مسیر فایل در سیستم فایل
    file_path = os.path.join(settings.BASE_DIR, 'App/protected_js', filename)

    if not os.path.isfile(file_path):
        raise Http404("File not found")

    with open(file_path, 'rb') as file:
        return HttpResponse(file.read(), content_type='application/javascript')


#فرستادن پروفایل کاربر 
class GetProfilePhoto(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")

        if not telegram_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            picture_url = async_to_sync(get_profile_picture)(telegram_id)

            if picture_url == None:
                picture_url = request.data.get("photo_url")

            return Response({"photo_url": picture_url}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "No profile photo found"}, status=status.HTTP_404_NOT_FOUND)


# گرفتن اطلاعات کاربر
class GetUserInfo(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")

        if not telegram_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)     
        try:
            student = Student.objects.get(telegram_id=telegram_id)
            student.refresh_energy()
            student.refresh_from_db()   # چون دوباره سیو میشه اطلاعات جدید رو بگیره
            serialized_data = UserInfoSerializer(student).data

            picture_url = async_to_sync(get_profile_picture)(telegram_id)
            
            if picture_url == None:
                picture_url = request.data.get("photo_url")
            # اضافه کردن عکس پروفایل به داده‌های پاسخ
            serialized_data["picture"] = picture_url
            print(serialized_data)
            return Response(data=serialized_data, status=status.HTTP_200_OK)
        
        except Student.DoesNotExist:
            return Response({"error": "Profile not found!"}, status=status.HTTP_404_NOT_FOUND)



class CheckUserExistView(APIView, TelegramAuthClass):
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        is_valid, result = self.validate_telegram_request(request.data)
        if not is_valid:
            return result  # در این حالت result خود Response با ارور هست

        telegram_id = result

        student_exists = Student.objects.filter(telegram_id=telegram_id).exists()
        if student_exists:
            return Response({"status": "exists", "redirect_url": "/home/"})
        else:
            return Response({"status": "not_exists", "redirect_url": "/login/"})

    def get(self, request):
        return render(request, 'loading.html')

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        context = {
            'faculties': serializer.data
        }
        return render(request, 'login.html', context)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            student.refresh_energy()
            student_info = UserInfoSerializer(student).data
            return Response(student_info, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    token = settings.COIN_TOKEN
    context = {
        "coin_token": token
    }
    return render(request, 'home.html', context)


class UpdateCoinView(APIView, TelegramAuthClass):
    def post(self, request):
        is_valid, result = self.validate_telegram_request(request.data)
        if not is_valid:
            return result  # Response with error

        telegram_id = result
        data = request.data

        # استفاده از سریالایزر برای بررسی صحت داده‌ها
        serializer = UpdateCoinSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": "Invalid data", "details": serializer.errors}, status=400)

        try:
            student = Student.objects.get(telegram_id=telegram_id)
            
            sv = serializer.validated_data
            student.coin = sv.get('coin', student.coin)
            student.last_time_energy = sv.get('last_time_energy', student.last_time_energy)
            student.current_energy = sv.get('current_energy', student.current_energy)
            student.save()

            return Response({"message": "Coin updated successfully"}, status=200)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)


def chart(request):
    return render(request, 'chart.html')


class FacultyCoursesView(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")

        if not telegram_id:
            return Response({"error": "telegram_id الزامی است."}, status=400)

        try:
            student = Student.objects.get(telegram_id=telegram_id)
        except Student.DoesNotExist:
            return Response({"error": "دانشجو پیدا نشد"}, status=404)

        courses = Course.objects.filter(faculty=student.faculty).prefetch_related("professors")

        serializer = CourseSerializer(
            courses,
            many=True,
            context={"student": student}
        )

        passed_units_total = serializer.context.get("passed_units_counter", 0)

        response = {
            "courses": serializer.data,
            "passed_units": passed_units_total
        }
        return Response(response)


class CurrentCoursesView(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")

        if not telegram_id:
            return Response({"error": "telegram_id الزامی است."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = Student.objects.get(telegram_id=telegram_id)
        except Student.DoesNotExist:
            return Response({"error": "دانشجو پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
        
        current_courses = StudentCourse.objects.filter(student=student, passed=False)

        data = []
        for sc in current_courses:
            data.append({
                "course": sc.course.name,
                "credit": sc.course.credits,
                "prerequisite": sc.course.prerequisite.name if sc.course.prerequisite else None,
                "professor": sc.professor.name,
            })
        serializer = CurrentCourseSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


def profile(request):
    return render(request, 'profile.html')


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentNameUpdateSerializer

class UpdateStudentNameAPIView(APIView):

    def post(self, request):
        telegram_id = request.data.get("telegram_id")

        if not telegram_id:
            return Response(
                {"error": "telegram_id ارسال نشده"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = Student.objects.get(telegram_id=telegram_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "دانشجو پیدا نشد"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentNameUpdateSerializer(
            student,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "نام تغییر کرد"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
