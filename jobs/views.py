from rest_framework import viewsets, filters, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage jobs with filtering capabilities.
    """
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Enable filtering by status, category, client, freelancer, and is_active
    filterset_fields = ['status', 'category', 'client', 'freelancer', 'is_active']

    # Enable search functionality (title & description)
    search_fields = ['title', 'description']

    # Enable ordering (e.g., ?ordering=budget or ?ordering=-budget for descending)
    ordering_fields = ['created_at', 'budget']

    def perform_create(self, serializer):
        """ Assign the logged-in user as the client when creating a job """
        serializer.save(client=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """ Soft delete instead of permanent delete """
        job = self.get_object()
        job.is_active = False
        job.save()
        return Response({"message": "Job deactivated"}, status=204)

    @action(detail=True, methods=['POST'])
    def assign_freelancer(self, request, pk=None):
        """ Assign a freelancer to a job """
        job = self.get_object()
        freelancer = request.user
        if job.freelancer:
            return Response({"error": "Job already assigned"}, status=400)
        job.freelancer = freelancer
        job.status = "in_progress"
        job.save()
        return Response({"message": "Freelancer assigned successfully"})

class JobListCreateView(generics.ListCreateAPIView):
    """List all jobs or create a new job (Client only)"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)  # Assign job to the logged-in client

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific job"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]