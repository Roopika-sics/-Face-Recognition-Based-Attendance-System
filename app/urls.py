from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('student_list/', views.student_list, name='student_list'),
    path('students/view/<int:student_id>/', views.view_student, name='view_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),



    #Faculty
    path('faculty_list/', views.faculty_list, name='faculty_list'),
    path('create_faculty/', views.create_faculty, name='create_faculty'),
    path('faculty_login/', views.faculty_login, name='faculty_login'),
    path('faculty_logout/', views.faculty_logout, name='faculty_logout'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('decline_leave/<int:leave_id>/', views.decline_leave, name='decline_leave'),
    path('faculty_calendar/', views.faculty_calendar, name='faculty_calendar'),
    path('get_events/', views.get_events, name='get_events'),
    path("add_event/", views.add_event, name="add_event"),
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"),

]
