from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import ProjectViewSet
from rest_framework import routers
from core.views.api_views import TaskAPIView, TaskCommentAPIView, ProjectList
from core.views.viewset import BlockViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='core')
router.register(r'tasks', TaskViewSet, base_name='core')
router.register(r'blocks', BlockViewSet, base_name='core')


urlpatterns = [
    # path('tasks/', TaskAPIView.as_view()),
    path('tasks/comment/', TaskCommentAPIView.as_view()),
    # path('projects/', ProjectList.as_view())

] + router.urls





