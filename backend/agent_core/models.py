from django.db import models
import json

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CleaningJob(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logs = models.TextField(default="[]") # JSON list of logs
    
    def add_log(self, message):
        logs_list = json.loads(self.logs)
        logs_list.append(message)
        self.logs = json.dumps(logs_list)
        self.save()

class AnalysisReport(models.Model):
    job = models.OneToOneField(CleaningJob, on_delete=models.CASCADE)
    initial_quality_score = models.FloatField(default=0.0)
    final_quality_score = models.FloatField(default=0.0)
    issues_found = models.JSONField(default=dict)
    actions_taken = models.JSONField(default=list)
    cleaned_file_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
