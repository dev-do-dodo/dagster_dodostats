from dagster import job
from .ops import current_revenue_op

@job
def update_current_revenue():
    current_revenue_op()
