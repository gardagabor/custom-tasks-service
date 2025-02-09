from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    def __str__(self):
        return self.title