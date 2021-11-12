from functools import reduce
from collections import Counter
from datetime import datetime, timedelta


def get_lodges_per_year(lodges_list):
    lodges = [lodge.first_checkin.year for lodge in lodges_list]
    years = Counter(lodges).keys()  # equals to list(set(words))
    ocurrences = Counter(lodges).values()  # counts the elements' frequency

    return {"years": list(years), "ocurrences": list(ocurrences)}


def get_revenues(forecasts, concept):

    filtered_forecast = filter(lambda x: x["concept"] == concept, forecasts)

    list_accommodations = list(filtered_forecast)

    forecast_count = reduce(lambda x, y: x + y["count"], list_accommodations, 0)
    forecast_income = reduce(lambda x, y: x + y["net_amount"], list_accommodations, 0)
    forecast_avg = reduce(
        lambda x, y: (x + y["avg_income"] / len(list_accommodations)),
        list_accommodations,
        0,
    )

    result = {
        "count": forecast_count,
        "total": forecast_income,
        "avg": forecast_avg,
    }

    return result


def remove_duplicates(list):
    list_without_duplicates = []
    for item in list:
        if item not in list_without_duplicates:
            list_without_duplicates.append(item)

    return list_without_duplicates


def validate_most_used_room_type(room_list):
    try:
        return room_list[0]["_id"][0]
    except TypeError:
        return room_list[0]["_id"]


def calculate_customer_age(birthdate):
    age = (datetime.utcnow() - datetime.strptime(birthdate, "%Y-%m-%d")) / timedelta(
        days=365.2425
    )
    return age
