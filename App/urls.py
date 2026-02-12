from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.CheckUserExistView.as_view(), name='empty_link'),
    path('telegram/webhook/', views.webhook, name='webhook'),
    path('loading/', views.CheckUserExistView.as_view(), name='check_user_exist'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('api/profile_photo/', views.GetProfilePhoto.as_view(), name="get_profile_photo"),
    path('api/user_info/', views.GetUserInfo.as_view(), name="get_user_info"),
    path('secure-js/<str:filename>/', views.protected_js, name='protected_js'),
    path('api/update_coin/', views.UpdateCoinView.as_view(), name='update_coin'),
    path('chart/', views.chart, name='chart'),
    path('api/faculty_courses/', views.FacultyCoursesView.as_view(), name='faculty_courses'),
    path('api/current_courses/', views.CurrentCoursesView.as_view(), name='current_courses'),
    path('profile/', views.profile, name='profile'),
    path('update/profile', views.UpdateStudentNameAPIView.as_view(), name="update_profile")
    
]