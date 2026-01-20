from dagster import job
from .ops import operational_revenue_op


@job
def update_operational_revenue():
    operational_revenue_op()
