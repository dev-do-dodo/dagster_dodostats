from dagster import ScheduleDefinition
from .jobs import update_information

update_information_scheduler = ScheduleDefinition(
    job=update_information,
    cron_schedule="*/30 * * * *",
    execution_timezone="Europe/Moscow"
)
