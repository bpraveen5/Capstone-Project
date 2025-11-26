from rest_framework import serializers
from .models import Dataset, CleaningJob, AnalysisReport

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

class AnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = '__all__'

class CleaningJobSerializer(serializers.ModelSerializer):
    report = AnalysisReportSerializer(source='analysisreport', read_only=True)
    
    class Meta:
        model = CleaningJob
        fields = '__all__'
