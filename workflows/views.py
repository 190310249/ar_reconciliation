from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Workflow
from .serializers import WorkflowSerializer

from .tasks import ingestion_task


class WorkflowCreateAPIView(APIView):

    def post(self, request):

        external_id = request.data.get(
            "external_id"
        )

        workflow, created = Workflow.objects.get_or_create(
            external_id=external_id,
            defaults={
                "payload": request.data
            }
        )

        if created:

            ingestion_task.delay(
                str(workflow.workflow_id)
            )

        serializer = WorkflowSerializer(
            workflow
        )

        return Response(serializer.data)


class WorkflowStatusAPIView(APIView):

    def get(self, request, workflow_id):

        workflow = Workflow.objects.get(
            workflow_id=workflow_id
        )

        serializer = WorkflowSerializer(
            workflow
        )

        return Response(serializer.data)