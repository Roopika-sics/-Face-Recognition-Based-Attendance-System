from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=20, null=False, unique=True)
    password = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty_subject = models.CharField(max_length=20, null=False)
    faculty_email = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return f"{self.faculty_subject} - {self.user.first_name} {self.user.last_name}"
    


class Face(models.Model):
    face_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Assuming User model exists
    image_path = models.CharField(max_length=320, null=False)
    face_encoding = models.BinaryField(null=False)

    def __str__(self):
        return f"Face ID: {self.face_id} - User ID: {self.user.user_id}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    attendance_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateField(null=False)
    time_in = models.TimeField(null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)


    def __str__(self):
        return f"Attendance ID: {self.attendance_id} - User ID: {self.user.user_id} - Status: {self.status}"


