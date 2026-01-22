from dagster import op, OpExecutionContext
from datetime import date, datetime
from database.engine import session_maker
from database.models import RevenueCurrentMonth, Restaurant, RevenueAllRestaurant
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from connection import public_dodo_api


@op
async def current_revenue_op(context: OpExecutionContext):
    date_today = date.today()
    link = 'https://publicapi.dodois.io/ru/api/v1/FinancialMetrics'
    async with session_maker() as session:
        response = await public_dodo_api(link)
        current_year_progressive_total = "{:,}".format(response['response']['current_year_progressive_total']).replace(
            ',', ' ')
        current_month_progressive_total = "{:,}".format(
            response['response']['current_month_progressive_total']).replace(',', ' ')
        stmt = select(RevenueAllRestaurant).where(RevenueAllRestaurant.id == 1)
        answer = await session.execute(stmt)
        revenue = answer.scalars().one_or_none()
        if revenue:
            revenue.current_year_progressive_total = current_year_progressive_total
            revenue.current_month_progressive_total = current_month_progressive_total
            revenue.current_time = datetime.now()
        await session.commit()
    async with session_maker() as session:
        answer = await session.execute(select(Restaurant))
        units = answer.scalars().all()
    async with session_maker() as session:
        for unit in units:
            try:
                link = (f'https://publicapi.dodois.io/ru/api/v1/unitinfo/{unit.id}'
                        f'/monthrevenue/{date_today.year}/{date_today.month}')
                response = await public_dodo_api(link)
                update_params = {
                    'revenue': "{:,}".format(int(response["UnitRevenue"]["Value"])
                                             ).replace(','     , ' '),
                    'year': date_today.year,
                    'month': date_today.month,
                    'restaurant_id': unit.id
                }
                stmt = insert(RevenueCurrentMonth).values(**update_params).on_conflict_do_update(
                    index_elements=['restaurant_id', 'year', 'month'],
                    set_=update_params,
                )
                await session.execute(stmt)
            except Exception:
                pass
        await session.commit()
