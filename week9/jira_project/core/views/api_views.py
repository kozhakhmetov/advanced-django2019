from django.http import Http404
from requests import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import Project, Task, TaskComment, TaskDocument
from core.serializers import ProjectSerializer, TaskSerializer, TaskCommentSerializer, TaskDocumentSerializer

import logging

logger = logging.getLogger(__name__)

class ProjectList(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    http_method_names = ['get', 'put', 'delete']

    @staticmethod
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(creator_id=request.user.id, block_id=request.query_params['block_id'])
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(request)
        logger.info(f"{self.request.user} created project")
        logger.warning('HAHAHAHAHA')
        logger.error('AAAAAAAAAAAAAAAAAAAAAA')
        logger.critical('NONONONONONONONONONO')
        return Response(serializer.data)


class TaskCommentAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = TaskComment.objects.filter(creator_id=request.user.id)
        serializer = TaskCommentSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(request)
        return Response(serializer.data)


class TaskDocumentAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = TaskDocument.objects.filter(creator_id=request.user.id)
        serializer = TaskDocumentSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(request)
        return Response(serializer.data)