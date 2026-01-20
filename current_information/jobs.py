from dagster import job
from .ops import check_updates_op

@job
def update_information():
    check_updates_op()
