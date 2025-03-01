from django.urls import path
from . import views

urlpatterns = [
    path('student_registration/',views.student_register,name='student_registration'),
    path('student_login/',views.student_login,name='student_login'),
    path('student_login/',views.student_logout,name='student_logout'),
    path('',views.student_landing_page,name='student_landing_page'),
    path('student/profile/<str:student_id>/', views.student_profile, name='student_profile'),
]