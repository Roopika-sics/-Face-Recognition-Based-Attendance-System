from django.urls import path
from . import views


urlpatterns = [
    path('student_registration/',views.student_register,name='student_registration'),
    path('student_login/',views.student_login,name='student_login'),
    path('student_logout/',views.student_logout,name='student_logout'),
    path('',views.student_landing_page,name='student_landing_page'),
    path('student/profile/<str:student_id>/', views.student_profile, name='student_profile'),
    path('forgot-password/', views.forget_password, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.password_reset_sent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.reset_password, name='reset-password'),
    path('calendar/', views.calendar, name='calendar'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('leave_status/', views.leave_status, name='leave_status'),
]






