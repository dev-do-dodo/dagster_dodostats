from dagster import ScheduleDefinition
from .jobs import update_operational_revenue

operational_revenue_scheduler = ScheduleDefinition(
    job=update_operational_revenue,
    cron_schedule="*/30 * * * *",
    execution_timezone="Europe/Moscow"
)
