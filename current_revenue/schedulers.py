from dagster import ScheduleDefinition
from .jobs import update_current_revenue

current_revenue_scheduler = ScheduleDefinition(
    job=update_current_revenue,
    cron_schedule="*/30 * * * *",
    execution_timezone="Europe/Moscow"
)