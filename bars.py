import json
from math import sqrt
import os
from sys import argv, exit
import zipfile


def load_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("No such file: {}".format(filepath))
    if zipfile.is_zipfile(filepath):
        with zipfile.ZipFile(filepath, "r") as this_zip:
            with this_zip.open(this_zip.namelist()[0]) as fd:
                    text = fd.read().decode("cp1251")
                    return json.loads(text)
    elif filepath.endswith(".json"):
        with open(filepath, "rb") as fd:
            text = fd.read().decode("cp1251")
            return json.loads(text)
    else:
        raise FileNotFoundError("Not a json or zip file")


def get_biggest_bar(data):
    return max(data, key=lambda bar: bar['SeatsCount'])


def get_smallest_bar(data):
    return min(data, key=lambda bar: bar['SeatsCount'])


def get_closest_bar(data, longitude, latitude):
    return min(data, key=lambda bar: sqrt((longitude - float(bar["Longitude_WGS84"])) ** 2 +
                                          (latitude - float(bar["Latitude_WGS84"])) ** 2))


if __name__ == "__main__":
    if len(argv) != 2:
        print("Ввидите имя загружаемого файла после 'python {}'".format(__file__))
        exit()

    data = load_data(argv[1])
    smallest = get_smallest_bar(data)
    biggest = get_biggest_bar(data)
    print("Самый маленький бар - {}, расположенный по адресу {}.".format(smallest["Name"], smallest["Address"]))
    print("Самый большой бар - {}, расположенный по адресу {}.".format(biggest["Name"], biggest["Address"]))
    while True:
        try:
            lat = float(input("Введите широту: "))
            lon = float(input("Введите долготу: "))
            break
        except ValueError:
            print("Please input correct number")
    closest = get_closest_bar(data, lat, lon)
    print("Ближайший бар - {}, расположенный по адресу {}.".format(closest["Name"], closest["Address"]))
