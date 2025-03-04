from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('student_registration/',views.student_register,name='student_registration'),
    path('student_login/',views.student_login,name='student_login'),
    path('student_logout/',views.student_logout,name='student_logout'),
    path('',views.student_landing_page,name='student_landing_page'),
    path('student/profile/<str:student_id>/', views.student_profile, name='student_profile'),
    path('forgot-password/', views.forget_password, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.password_reset_sent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.reset_password, name='reset-password'),
]






