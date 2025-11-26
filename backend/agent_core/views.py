from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dataset, CleaningJob
from .serializers import DatasetSerializer, CleaningJobSerializer
from .agent_engine import UDAQAgent
import threading

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc() # Print to server console
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CleaningJobViewSet(viewsets.ModelViewSet):
    queryset = CleaningJob.objects.all()
    serializer_class = CleaningJobSerializer

    @action(detail=False, methods=['post'])
    def start_job(self, request):
        dataset_id = request.data.get('dataset_id')
        if not dataset_id:
            return Response({'error': 'dataset_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        
        job = CleaningJob.objects.create(dataset=dataset)
        
        # Run agent in a separate thread to not block the response
        agent = UDAQAgent(job.id)
        thread = threading.Thread(target=agent.run)
        thread.start()
        
        return Response(CleaningJobSerializer(job).data, status=status.HTTP_201_CREATED)
