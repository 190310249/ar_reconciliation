from celery import shared_task
from .models import Workflow, StageExecution

from reconciliation.matcher import match_record
from reconciliation.validator import validate_record
from reconciliation.router import route_decision
from reconciliation.utils import simulate_random_failure


@shared_task(bind=True, max_retries=3)
def ingestion_task(self, workflow_id):

    workflow = Workflow.objects.get(
        workflow_id=workflow_id
    )

    execution = StageExecution.objects.create(

        workflow=workflow,

        stage="INGESTION",

        status="RUNNING"
    )

    try:

        simulate_random_failure()

        workflow.status = "RUNNING"

        workflow.current_stage = "MATCHING"

        workflow.save()

        execution.status = "SUCCESS"

        execution.save()

        matching_task.delay(
            str(workflow.workflow_id)
        )

    except Exception as exc:

        execution.status = "FAILED"

        execution.error = str(exc)

        execution.save()

        workflow.retry_count += 1

        workflow.error_message = str(exc)

        workflow.save()

        raise self.retry(
            exc=exc,
            countdown=2
        )

@shared_task(bind=True, max_retries=3)
def matching_task(self, workflow_id):

    workflow = Workflow.objects.get(
        workflow_id=workflow_id
    )

    execution = StageExecution.objects.create(

        workflow=workflow,

        stage="MATCHING",

        status="RUNNING"
    )

    try:

        simulate_random_failure()

        matched = match_record(
            workflow.payload
        )

        workflow.payload["matched"] = matched

        workflow.current_stage = "VALIDATION"

        workflow.save()

        execution.status = "SUCCESS"

        execution.save()

        validation_task.delay(
            str(workflow.workflow_id)
        )

    except Exception as exc:

        execution.status = "FAILED"

        execution.error = str(exc)

        execution.save()

        workflow.retry_count += 1

        workflow.error_message = str(exc)

        workflow.save()

        raise self.retry(
            exc=exc,
            countdown=2
        )

@shared_task(bind=True, max_retries=3)
def validation_task(self, workflow_id):

    workflow = Workflow.objects.get(
        workflow_id=workflow_id
    )

    execution = StageExecution.objects.create(

        workflow=workflow,

        stage="VALIDATION",

        status="RUNNING"
    )

    try:

        simulate_random_failure()

        validated = validate_record(
            workflow.payload
        )

        workflow.payload["validated"] = validated

        workflow.current_stage = "DECISION"

        workflow.save()

        execution.status = "SUCCESS"

        execution.save()

        decision_task.delay(
            str(workflow.workflow_id)
        )

    except Exception as exc:

        execution.status = "FAILED"

        execution.error = str(exc)

        execution.save()

        workflow.retry_count += 1

        workflow.error_message = str(exc)

        workflow.save()

        raise self.retry(
            exc=exc,
            countdown=2
        )

@shared_task(bind=True, max_retries=3)
def decision_task(self, workflow_id):

    workflow = Workflow.objects.get(
        workflow_id=workflow_id
    )

    execution = StageExecution.objects.create(

        workflow=workflow,

        stage="DECISION",

        status="RUNNING"
    )

    try:

        simulate_random_failure()

        decision = route_decision(

            workflow.payload.get("matched"),

            workflow.payload.get("validated")
        )

        workflow.payload["decision"] = decision

        workflow.current_stage = "DONE"

        workflow.status = "COMPLETED"

        workflow.save()

        execution.status = "SUCCESS"

        execution.save()

    except Exception as exc:

        execution.status = "FAILED"

        execution.error = str(exc)

        execution.save()

        workflow.retry_count += 1

        workflow.error_message = str(exc)

        workflow.status = "FAILED"

        workflow.save()

        raise self.retry(
            exc=exc,
            countdown=2
        )

    workflow = Workflow.objects.get(
        workflow_id=workflow_id
    )

    try:

        simulate_random_failure()

        decision = route_decision(
            workflow.payload.get("matched"),
            workflow.payload.get("validated")
        )

        workflow.payload["decision"] = decision

        workflow.current_stage = "DONE"

        workflow.status = "COMPLETED"

        workflow.save()

    except Exception as exc:

        workflow.retry_count += 1

        workflow.error_message = str(exc)

        workflow.status = "FAILED"

        workflow.save()

        raise self.retry(
            exc=exc,
            countdown=2
        )