from dagster import Definitions
from .jobs import update_current_revenue
from .schedulers import current_revenue_scheduler

defs = Definitions(
    jobs=[update_current_revenue],
    schedules=[current_revenue_scheduler],
    resources={}
)
