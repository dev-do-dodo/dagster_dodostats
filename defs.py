from dagster import Definitions
import current_information.definitions as info_defs
import current_revenue.definitions as revenue_defs
import operational_revenue.definitions as operational_defs


all_defs = [
    info_defs.defs,
    revenue_defs.defs,
    operational_defs.defs
]

defs = Definitions.merge(*all_defs)
