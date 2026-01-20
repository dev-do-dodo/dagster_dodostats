from dagster import Definitions
from .jobs import update_operational_revenue
from .schedulers import operational_revenue_scheduler

defs = Definitions(
    jobs=[update_operational_revenue],
    schedules=[operational_revenue_scheduler],
    resources={}
)
