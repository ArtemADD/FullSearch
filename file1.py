import sys
from io import BytesIO
from DeltaFinding import delta_finding
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
# toponym_to_find = " ".join(sys.argv[1:])
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coordinates = toponym["Point"]["pos"]
# Долгота и широта:
size_object = toponym['boundedBy']['Envelope']
lower_corner = size_object['lowerCorner'].split()
upper_corner = size_object['upperCorner'].split()
toponym_longitude, toponym_lattitude = toponym_coordinates.split()
delta = delta_finding(upper_corner, lower_corner)
# print(toponym_coordinates)
# print(lower_corner)
# print(upper_corner)
# print(delta)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": delta,
    "l": "map",
    'pt': f'{toponym_longitude},{toponym_lattitude},pm2rdm'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
if not response:
    raise 'gg'
Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
