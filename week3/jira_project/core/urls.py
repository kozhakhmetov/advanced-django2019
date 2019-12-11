from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import ProjectViewSet
from rest_framework import routers
from core.views.api_views import TaskAPIView, TaskCommentAPIView
from core.views.viewset import BlockViewSet

router = DefaultRouter()
urlpatterns = [
    path('tasks/', TaskAPIView.as_view()),
    path('tasks/comment/', TaskCommentAPIView.as_view())

] + router.urls

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, base_name='core')
router.register(r'blocks', BlockViewSet, base_name='core')



