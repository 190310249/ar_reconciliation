from django.urls import path

from .views import (
    WorkflowCreateAPIView,
    WorkflowStatusAPIView
)

urlpatterns = [

    path(
        'submit/',
        WorkflowCreateAPIView.as_view()
    ),

    path(
        '<uuid:workflow_id>/',
        WorkflowStatusAPIView.as_view()
    ),
]