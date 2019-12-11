from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from core.models import Project, Block
from core.serializers import ProjectSerializer, BlockSerializer


class ProjectListViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.filter(creator=self.request.user)
        return queryset

    @action(methods=['GET'], detail=False)
    def my(self, request):
        projects = Project.objects.filter(creator=self.request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def tasks(self, request, pk):
        # project = get_object_or_404(Project, id=pk)

        # try:
        #     project = Project.objects.get(id=pk)
        # except Project.DoesNotExist:
        #     raise Http404

        instance = self.get_object()
        res = f'{instance.name}: tasks'

        return Response(res)


class BlockViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Block.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BlockSerializer

    def perform_create(self, serializer):
        return serializer.save(name=self.request.data['name'],
                               status=self.request.data['status'],
                               project_id=self.request.data['project_id'])

    def get_queryset(self):
        return self.queryset.all()







