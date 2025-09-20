from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    ROLES = (
        ('Employer', 'Employer'),
        ('Employee', 'Employee'),
    )
    choice = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.username


# Job Model (Linked to Employer)
class Job(models.Model):
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, limit_choices_to={'choice': 'Employer'})
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    requirments = models.TextField(null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    deadline = models.DateField()

    def __str__(self):
        return self.title or "Untitled Job"


class Application(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="applications")
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} -> {self.job.title}"
