from dagster import OpExecutionContext, op
from database.models import Restaurant, OperationalStatistics
from database.engine import session_maker
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
from connection import public_dodo_api


@op
async def operational_revenue_op(context: OpExecutionContext):
    async with session_maker() as session:
        answer = await session.execute(select(Restaurant))
        units = answer.scalars().all()
    async with session_maker() as session:
        for unit in units:
            link = f'https://publicapi.dodois.io/ru/api/v1/OperationalStatisticsForTodayAndWeekBefore/{unit.id}'
            response = await public_dodo_api(link)
            try:
                today_stationary_revenue = "{:,}".format(int(response["today"]["stationaryRevenue"])).replace(',', ' ')
                today_stationary_order_count = "{:,}".format(int(response["today"]["stationaryOrderCount"])).replace(',',
                                                                                                                     ' ')
            except Exception:
                today_stationary_revenue = '0'
                today_stationary_order_count = '0'
            try:
                today_delivery_revenue = "{:,}".format(int(response["today"]["deliveryRevenue"])).replace(',', ' ')
                today_delivery_order_count = "{:,}".format(int(response["today"]["deliveryOrderCount"])).replace(',', ' ')
            except Exception:
                today_delivery_revenue = '0'
                today_delivery_order_count = '0'

            try:
                today_revenue = "{:,}".format(int(response["today"]["revenue"])).replace(',', ' ')
                today_order_count = "{:,}".format(int(response["today"]["orderCount"])).replace(',', ' ')
            except Exception:
                today_revenue = '0'
                today_order_count = '0'

            try:
                week_before_stationary_revenue = "{:,}".format(int(response["weekBefore"]["stationaryRevenue"])).replace(
                    ',', ' ')
                week_before_stationary_order_count = "{:,}".format(
                    int(response["weekBefore"]["stationaryOrderCount"])).replace(',', ' ')
            except Exception:
                week_before_stationary_revenue = '0'
                week_before_stationary_order_count = '0'
            try:
                week_before_delivery_revenue = "{:,}".format(int(response["weekBefore"]["deliveryRevenue"])).replace(',',
                                                                                                                     ' ')
                week_before_delivery_order_count = "{:,}".format(int(response["weekBefore"]["deliveryOrderCount"])).replace(
                    ',', ' ')
            except Exception:
                week_before_delivery_revenue = '0'
                week_before_delivery_order_count = '0'
            try:
                week_before_revenue = "{:,}".format(int(response["weekBefore"]["revenue"])).replace(',', ' ')
                week_before_order_count = "{:,}".format(int(response["weekBefore"]["orderCount"])).replace(',', ' ')
            except Exception:
                week_before_revenue = '0'
                week_before_order_count = '0'

            try:
                yesterday_to_this_time_stationary_revenue = "{:,}".format(int(response["yesterdayToThisTime"]
                                                                              ["stationaryRevenue"])).replace(' ', '')
                yesterday_to_this_time_stationary_order_count = "{:,}".format(int(response["yesterdayToThisTime"]
                                                                                  ["stationaryOrderCount"])).replace(',',
                                                                                                                     ' ')
            except Exception:
                yesterday_to_this_time_stationary_revenue = '0'
                yesterday_to_this_time_stationary_order_count = '0'
            try:
                yesterday_to_this_time_delivery_revenue = "{:,}".format(int(response["yesterdayToThisTime"]
                                                                            ["deliveryRevenue"])).replace(' ', '')
                yesterday_to_this_time_delivery_order_count = "{:,}".format(int(response["yesterdayToThisTime"]
                                                                                ["deliveryOrderCount"])).replace(',',
                                                                                                                 ' ')
            except Exception:
                yesterday_to_this_time_delivery_revenue = '0'
                yesterday_to_this_time_delivery_order_count = '0'
            try:
                yesterday_to_this_time_revenue = "{:,}".format(int(response["yesterdayToThisTime"]["revenue"])).replace(' ',
                                                                                                                        '')
                yesterday_to_this_time_order_count = "{:,}".format(
                    int(response["yesterdayToThisTime"]["orderCount"])).replace(',',
                                                                                ' ')
            except Exception:
                yesterday_to_this_time_revenue = '0'
                yesterday_to_this_time_order_count = '0'

            try:
                week_before_to_this_time_stationary_revenue = "{:,}".format(
                    int(response["weekBeforeToThisTime"]["stationaryRevenue"])).replace(',', ' ')
                week_before_to_this_time_stationary_order_count = "{:,}".format(
                    int(response["weekBeforeToThisTime"]["stationaryOrderCount"])).replace(',', ' ')
            except Exception:
                week_before_to_this_time_stationary_revenue = '0'
                week_before_to_this_time_stationary_order_count = '0'
            try:
                week_before_to_this_time_delivery_revenue = "{:,}".format(
                    int(response["weekBeforeToThisTime"]["deliveryRevenue"])).replace(',', ' ')
                week_before_to_this_time_delivery_order_count = "{:,}".format(
                    int(response["weekBeforeToThisTime"]["deliveryOrderCount"])).replace(',', ' ')
            except Exception:
                week_before_to_this_time_delivery_revenue = '0'
                week_before_to_this_time_delivery_order_count = '0'
            try:
                week_before_to_this_time_revenue = "{:,}".format(
                    int(response["weekBeforeToThisTime"]["revenue"])).replace(',', ' ')
                week_before_to_this_time_order_count = "{:,}".format(
                    int(response["weekBeforeToThisTime"]["orderCount"])).replace(',', ' ')
            except Exception:
                week_before_to_this_time_revenue = '0'
                week_before_to_this_time_order_count = '0'
            update_params = {
                'restaurant_id': unit.id,
                'date': datetime.now(),
                'today_stationary_revenue': today_stationary_revenue,
                'today_stationary_order_count': today_stationary_order_count,
                'today_delivery_revenue': today_delivery_revenue,
                'today_delivery_order_count': today_delivery_order_count,
                'today_revenue': today_revenue,
                'today_order_count': today_order_count,

                'week_before_stationary_revenue': week_before_stationary_revenue,
                'week_before_stationary_order_count': week_before_stationary_order_count,
                'week_before_delivery_revenue': week_before_delivery_revenue,
                'week_before_delivery_order_count': week_before_delivery_order_count,
                'week_before_revenue': week_before_revenue,
                'week_before_order_count': week_before_order_count,

                'yesterday_to_this_time_stationary_revenue': yesterday_to_this_time_stationary_revenue.replace(',', ' '),
                'yesterday_to_this_time_stationary_order_count': yesterday_to_this_time_stationary_order_count,
                'yesterday_to_this_time_delivery_revenue': yesterday_to_this_time_delivery_revenue.replace(',', ' '),
                'yesterday_to_this_time_delivery_order_count': yesterday_to_this_time_delivery_order_count,
                'yesterday_to_this_time_revenue': yesterday_to_this_time_revenue.replace(',', ' '),
                'yesterday_to_this_time_order_count': yesterday_to_this_time_order_count,

                'week_before_to_this_time_stationary_revenue': week_before_to_this_time_stationary_revenue,
                'week_before_to_this_time_stationary_order_count': week_before_to_this_time_stationary_order_count,
                'week_before_to_this_time_delivery_revenue': week_before_to_this_time_delivery_revenue,
                'week_before_to_this_time_delivery_order_count': week_before_to_this_time_delivery_order_count,
                'week_before_to_this_time_revenue': week_before_to_this_time_revenue,
                'week_before_to_this_time_order_count': week_before_to_this_time_order_count}
            stmt = insert(OperationalStatistics).values(**update_params).on_conflict_do_update(
                index_elements=['restaurant_id'],
                set_=update_params
            )
            await session.execute(stmt)
        await session.commit()
