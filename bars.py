import json
from math import sqrt
import os
from sys import argv, exit
import zipfile


def load_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("No such file: {}".format(filepath))
    if zipfile.is_zipfile(filepath):
        with zipfile.ZipFile(filepath, "r") as zip_handler:
            with zip_handler.open(zip_handler.namelist()[0]) as file_handler:
                    file_text = file_handler.read().decode("cp1251")
                    return json.loads(file_text)
    elif filepath.endswith(".json"):
        with open(filepath, "rb") as file_handler:
            file_text = file_handler.read().decode("cp1251")
            return json.loads(file_text)
    else:
        raise FileNotFoundError("Not a json or zip file")


def get_biggest_bar(data):
    return max(data, key=lambda current_bar: current_bar['SeatsCount'])


def get_smallest_bar(data):
    return min(data, key=lambda current_bar: current_bar['SeatsCount'])


def get_closest_bar(data, latitude, longitude):
    return min(data, key=lambda current_bar: sqrt((latitude - float(current_bar["Latitude_WGS84"])) ** 2) +
                                             (longitude - float(current_bar["Longitude_WGS84"])) ** 2)


def get_user_coordinate():
    while True:
        try:
            latitude = float(input("Введите широту: "))
            longitude = float(input("Введите долготу: "))
            break
        except ValueError:
            print("Please input correct number")
    return latitude, longitude


def show_results(smallest_bar, biggest_bar, closest_bar):
    print("Самый маленький бар {} расположен по адресу {}.".format(smallest_bar["Name"], smallest_bar["Address"]))
    print("Самый большой бар {} расположен по адресу {}.".format(biggest_bar["Name"], biggest_bar["Address"]))
    print("Ближайший бар {} расположен по адресу {}.".format(closest_bar["Name"], closest_bar["Address"]))


if __name__ == "__main__":
    if len(argv) != 2:
        print("Ввидите имя загружаемого файла после 'python3 {}'".format(__file__))
        exit()
    if argv[1] == "--help":
        print("Скачайте список московских баров в формате json с сайта http://data.mos.ru/opendata/7710881420-bary.")
        print("Поместите в текущую директорию. Наберите python3 {} <имя файла> и нажмите enter.".format(__file__))
        exit()

    filename = argv[1]
    json_data = load_data(filename)
    smallest_bar = get_smallest_bar(json_data)
    biggest_bar = get_biggest_bar(json_data)
    user_latitude, user_longitude = get_user_coordinate()
    closest_bar = get_closest_bar(json_data, user_latitude, user_longitude)

    show_results(smallest_bar, biggest_bar, closest_bar)
