from django.contrib import admin
from .models import Dataset, CleaningJob, AnalysisReport

admin.site.register(Dataset)
admin.site.register(CleaningJob)
admin.site.register(AnalysisReport)
