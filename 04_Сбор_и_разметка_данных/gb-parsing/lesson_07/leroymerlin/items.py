# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Identity, Compose, MapCompose, TakeFirst


def prepare_product_code(code_string: str) -> int:
    """Функция вырезает из строки числовой артикул и конвертирует в число."""
    # На входе: Арт. 90145689
    code = code_string.replace('Арт. ', '')
    try:
        code = int(code)
    except ValueError:
        code = code_string
    return code


def delete_whitespaces(input_string: str) -> str:
    """Функция удаляет пробелы. Это нужно для подготовки чисел,
    в которых пробел разделяет разряды."""
    return input_string.replace(' ', '')


def prepare_price(price_parts: list) -> float:
    """Функция склеивает рубли и копейки из массива и возвращает число."""
    # На входе список из 1-2 строк (рубли всегда, копейки при наличии)
    price_string = '.'.join(price_parts)
    try:
        price = float(price_string)
    except ValueError:
        price = price_string
    return price


def prepare_specification_element(one_cell: str):
    """Функция обрабатывает элемент спецификации (название параметра или значение):
    удаляет пробелы, энтеры и прочий мусор."""
    return one_cell.strip()


def prepare_full_specification(all_specs):
    """Функция собирает характеристики товара в словарь. На входе все пары записаны в список последовательно.
    Значение пробует преобразовать в число (int, float), если это возможно."""
    specification = dict()
    for i in range(0, len(all_specs), 2):
        # Цикл по парам параметр-значение
        param = all_specs[i]
        value = all_specs[i + 1]
        if value.isdigit():
            # значение - это целое число
            try:
                value = int(value)
            except ValueError:
                value = all_specs[i + 1]
        elif value.replace('.', '').isdigit():
            # значение - это вещественное число
            try:
                value = float(value)
            except ValueError:
                value = all_specs[i + 1]
        specification[param] = value
    return specification


# Создаем структуру item-a
class LeroymerlinItem(scrapy.Item):

    # Определяем все поля одного товара (item-а),
    # которые парсим со страницы товара

    # для mongoDB
    _id = scrapy.Field()

    # Ссылка
    url = scrapy.Field(output_processor=TakeFirst())

    # Название товара
    title = scrapy.Field(output_processor=TakeFirst())

    # Цена товара
    price = scrapy.Field(
        input_processor=MapCompose(delete_whitespaces),
        output_processor=Compose(prepare_price)
    )

    # Артикул
    code = scrapy.Field(
        input_processor=MapCompose(prepare_product_code),
        output_processor=TakeFirst()
    )

    # Спецификация товара
    specification = scrapy.Field(
        input_processor=MapCompose(prepare_specification_element),
        output_processor=Compose(prepare_full_specification)
    )

    # Фотографии товара
    images = scrapy.Field()


