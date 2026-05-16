from django.contrib import admin

from .models import (
    Workflow,
    StageExecution,
)


class StageExecutionInline(
    admin.TabularInline
):

    model = StageExecution

    extra = 0

    readonly_fields = (

        "stage",

        "status",

        "error",

        "started_at",

        "completed_at",
    )


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):

    list_display = (

        "workflow_id",

        "external_id",

        "status",

        "current_stage",

        "retry_count",

        "created_at",
    )

    list_filter = (

        "status",

        "current_stage",
    )

    search_fields = (

        "workflow_id",

        "external_id",
    )

    readonly_fields = (

        "workflow_id",

        "created_at",

        "updated_at",
    )

    ordering = ("-created_at",)

    inlines = [
        StageExecutionInline
    ]


@admin.register(StageExecution)
class StageExecutionAdmin(
    admin.ModelAdmin
):

    list_display = (

        "workflow",

        "stage",

        "status",

        "started_at",

        "completed_at",
    )

    list_filter = (

        "stage",

        "status",
    )

    search_fields = (

        "workflow__external_id",
    )

    readonly_fields = (

        "started_at",

        "completed_at",
    )