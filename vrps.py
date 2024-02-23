import requests
from datetime import datetime, timedelta

START_DATE = datetime(2023, 12, 28)


def get_data():

    # Calculate the number of 28-day periods that have passed
    current_date = datetime.now()
    days_passed = (current_date - START_DATE).days
    periods_passed = days_passed // 28
    new_date = START_DATE + timedelta(days=(28*periods_passed))
    date_object = datetime.strptime(str(new_date), "%Y-%m-%d %H:%M:%S")

    # Format datetime object into new format
    airac = date_object.strftime("%Y_%m_%d")

    file_name = f"VRP_list_{airac}_CRC_20CA7F00.csv"
    url = f"https://nats-uk.ead-it.com/cms-nats/opencms/en/Publications/digital-datasets/vrp/{file_name}"
    response = requests.get(url)
    return response.content.decode()


def dms_to_dec(lat, lng):
    lat_deg, lat_min, lat_sec, _ = split_coordinates_lat(lat)
    lng_deg, lng_min, lng_sec, lng_dir = split_coordinates_lng(lng)

    lat_decimal = float(lat_deg) + (float(lat_min) / 60) + \
        (float(lat_sec)/3600)
    lng_decimal = float(lng_deg) + (float(lng_min) / 60) + \
        (float(lng_sec)/3600)
    if lng_dir == "W":
        lng_decimal *= -1

    return round(lat_decimal, 6), round(lng_decimal, 6)


def split_coordinates_lng(coord):
    direction = coord[-1]
    coord = coord[:-1]  # remove the direction

    return coord[:3], coord[3:5], coord[5:], direction


def split_coordinates_lat(coord):
    direction = coord[-1]
    coord = coord[:-1]  # remove the direction

    return coord[:2], coord[2:4], coord[4:], direction


def check_if_airac_day():
    given_date = datetime(2023, 12, 29)
    current_date = datetime.now()
    difference = current_date - given_date

    return difference.days % 28


def main():

    if check_if_airac_day() != 0:
        return

    data = get_data().splitlines()

    data.pop(0)
    data = [d.split(",")for d in data if d]

    with open("vrps.csv", "w", encoding="utf-8")as out_file:
        for d in data:
            lat, lng = dms_to_dec(d[1], d[2])

            string_ = f"VRP,{d[0]},{d[0]},{lat},{lng}\n"

            out_file.write(string_)
    print("CSV Generated")


if __name__ == "__main__":
    main()
