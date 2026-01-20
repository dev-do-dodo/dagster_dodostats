from dagster import Definitions
from .jobs import update_information
from .schedulers import update_information_scheduler

defs = Definitions(
    jobs=[update_information],
    schedules=[update_information_scheduler],
    resources={}
)
