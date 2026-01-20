from dagster import op, OpExecutionContext
from datetime import date, timedelta, datetime
from database.engine import session_maker
from database.models import Restaurant, Location, WorkingTime, CountRestaurant, CountCity
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from connection import public_dodo_api


def change_name(name):
    name_list = name.lower().replace(" ", "").split('-')
    try:
        number = name_list[-1]
    except IndexError:
        number = ''
    try:
        name = name_list[0]
    except IndexError:
        pass
    chars_dict = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ж": "g", "з": "z", "и": "i", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
        "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
        "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "shch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu",
        "я": "ya", "ё": "e", "й": "i", "0": "0", "1": "1",
        "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
        "7": "7", "8": "8", "9": "9"
    }
    try:
        for char in name:
            if char in chars_dict:
                name = name.replace(char, chars_dict[char])
        return f'{name}-{number}'
    except Exception:
        return name


@op
async def check_updates_op(context: OpExecutionContext):
    date_today = date.today()
    day_dict = {
        0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг',
        4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'
    }
    link_city = f'https://publicapi.dodois.io/ru/api/v1/GetLocalities'
    link = f'https://publicapi.dodois.io/ru/api/v1/unitinfo/all'
    url = f'https://publicapi.dodois.io/ru/api/v1/pizzeriascount/{date_today.year}/{date_today.month}'
    async with session_maker() as session:
        response_city = await public_dodo_api(link_city)
        for city in response_city:
            name = city["Name"]
            result = await session.execute(select(CountCity).filter_by(name=name))
            city = result.scalars().one_or_none()
            if city is None:
                city = CountCity(name=name)
                session.add(city)
        await session.commit()
    async with session_maker() as session:
        response_count = await public_dodo_api(url)
        for count in response_count:
            if count["year"] == date_today.year and count["month"] == date_today.month:
                update_params = {'count': count["count"], 'year': count['year'], 'month': count['month']}
                stmt = insert(CountRestaurant).values(**update_params).on_conflict_do_update(
                    index_elements=['year', 'month'],
                    set_=update_params,
                )
                await session.execute(stmt)
        await session.commit()
    async with session_maker() as session:
        response = await public_dodo_api(link)
        restaurant_ids = await session.execute(select(Restaurant.id))
        restaurant_ids = restaurant_ids.scalars().all()
        restaurant_ids = list(restaurant_ids)
        for unit in response:
            if unit['State'] == 1 and unit["Type"] == 1:
                try:
                    locality_name = unit['AddressDetails']['LocalityName']
                except TypeError:
                    locality_name = ''
                open_date_list = str(unit['BeginDateWork']).split('-')
                open_date = f'{open_date_list[-1]}.{open_date_list[1]}.{open_date_list[0]}'
                if unit['Id'] not in restaurant_ids:
                    unit_object = Restaurant(
                        id=unit['Id'],
                        uuid=unit['UUId'].lower(),
                        name=unit['Name'],
                        latin=change_name(unit['Name']),
                        address=unit['Address'],
                        orientation=unit['Orientation'],
                        city=locality_name,
                        begin_date_work=open_date,
                        begin_date=unit['BeginDateWork']
                    )
                    session.add(unit_object)
                    locality = Location(
                        restaurant=unit_object,
                        latitude=unit['Location']['Latitude'],
                        longitude=unit['Location']['Longitude'],
                        name=unit['Name'],
                        uuid=unit['UUId'].lower()
                    )
                    session.add(locality)
                    for work in unit['RestaurantWeekWorkingTime']:
                        seconds_start = int(timedelta(seconds=work['WorkingTimeStart']).total_seconds())
                        seconds_end = int(timedelta(seconds=work['WorkingTimeEnd']).total_seconds())
                        hours_start = seconds_start // 3600
                        minutes_start = (seconds_start % 60)
                        time_start = f"{hours_start:02}:{minutes_start:02}"
                        hours_end = seconds_end // 3600
                        minutes_end = (seconds_end % 60)
                        time_end = f"{hours_end:02}:{minutes_end:02}"
                        working = WorkingTime(
                            restaurant=unit_object,
                            day_index=day_dict[work['DayIndex']],
                            working_time_start=time_start,
                            working_time_end=time_end,
                            types='Ресторан'
                        )
                        session.add(working)
                    for work in unit['DeliveryWeekWorkingTime']:
                        seconds_start = int(timedelta(seconds=work['WorkingTimeStart']).total_seconds())
                        seconds_end = int(timedelta(seconds=work['WorkingTimeEnd']).total_seconds())
                        hours_start = seconds_start // 3600
                        minutes_start = (seconds_start % 60)
                        time_start = f"{hours_start:02}:{minutes_start:02}"
                        hours_end = seconds_end // 3600
                        minutes_end = (seconds_end % 60)
                        time_end = f"{hours_end:02}:{minutes_end:02}"
                        working = WorkingTime(
                            restaurant=unit_object,
                            day_index=day_dict[work['DayIndex']],
                            working_time_start=time_start,
                            working_time_end=time_end,
                            types='Доставка'
                        )
                        session.add(working)
        await session.commit()
    context.log.info(f"end - {datetime.now()}")
