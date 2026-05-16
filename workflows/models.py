import uuid

from django.db import models


class Workflow(models.Model):

    class Status(models.TextChoices):

        PENDING = "PENDING"

        RUNNING = "RUNNING"

        FAILED = "FAILED"

        COMPLETED = "COMPLETED"

    class Stage(models.TextChoices):

        INGESTION = "INGESTION"

        MATCHING = "MATCHING"

        VALIDATION = "VALIDATION"

        DECISION = "DECISION"

        DONE = "DONE"

    workflow_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    external_id = models.CharField(
        max_length=255,
        unique=True
    )

    payload = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    current_stage = models.CharField(
        max_length=30,
        choices=Stage.choices,
        default=Stage.INGESTION
    )

    retry_count = models.IntegerField(
        default=0
    )

    error_message = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.external_id}"
            f" - {self.status}"
        )


class StageExecution(models.Model):

    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="executions"
    )

    stage = models.CharField(
        max_length=50
    )

    status = models.CharField(
        max_length=20
    )

    error = models.TextField(
        null=True,
        blank=True
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return (
            f"{self.workflow.external_id}"
            f" - {self.stage}"
        )