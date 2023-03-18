import pandas as pd
from pathlib import Path
import numpy as np
import os


pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)


def read_data(columns, dates) -> tuple:
    data, numbers = {}, set()
    for date, i in zip(dates, range(sum(1 for x in Path('xlsx_files').iterdir()))):
        data[date] = pd.read_excel(Path(f"xlsx_files/Аудит заявок РФ_{dates[i]}.xlsx"), usecols=columns)
        numbers = numbers | set(data[date]['Номер заявки'].values)
    return data, numbers


def return_value(msg, type, check=None) -> [int, str]:
    while True:
        try:
            value = type(input(msg))
        except Exception:
            print('Неккоректный ввод!')
            continue
        if check == None:
            break
        if value in check:
            break
        print('Некорректный ввод!')
    return value


def form_date(dates) -> tuple:

    start_day: int
    end_day: int
    month: str
    year: str

    days, monthes, years = [], set(), set()
    for day, month, year in [elem.split('.') for elem in dates]:
        days.append(int(day))
        monthes.add(month)
        years.add(year)

    # Выбор месяца
    while True:
        month = '03'  # return_value('Введите месяц > ', int)
        if month in monthes:
            break
        print('Неккоректный ввод!')

    # Выбор года
    while True:
        year = '23'  # return_value('Введите год > ', int)
        if month in monthes:
            break
        print('Неккоректный ввод!')

    # Проверка корректности ввода и ввод дней
    try:
        while True:
            while True:
                start_day = return_value('Введите начальный день > ', int)
                if 0 < start_day < 31:
                    break
                print('Неккоректный день!')
                continue
            while True:
                end_day = return_value('Введите конечный день > ', int)
                if 0 < end_day < 31 and end_day >= start_day:
                    break
                print('Неккоректный день!')
                continue
            for elem in days:
                if elem in range(start_day, end_day):
                    raise Exception
                else:
                    print('По данному периоду нет данных!')
                    break
    except Exception:
        pass

    start_day = '0' + str(start_day) if start_day < 10 else str(start_day)
    end_day = '0' + str(end_day) if end_day < 10 else str(end_day)

    return (f"{start_day}.{month}.{year}", f"{end_day}.{month}.{year}")


def selection_of_period(date_slice, dates) -> tuple:

    days = [int(elem.split('.')[0]) for elem in date_slice]
    monthes = list(set(int(elem.split('.')[1]) for elem in date_slice))
    years = list(set(int(elem.split('.')[2]) for elem in date_slice))
    result = []

    for year in range(years[0], years[-1] + 1):
        for month in range(monthes[0], monthes[-1] + 1):
            for day in range(days[0], days[-1] + 1):
                year_ = '0' + str(year) if int(year) < 10 else str(year)
                month_ = '0' + str(month) if int(month) < 10 else str(month)
                day_ = '0' + str(day) if int(day) < 10 else str(day)
                date = f"{day_}.{month_}.{year_}"
                if date in dates:
                    result.append(date)

    return result


def dates_read_from_files() -> tuple:
    content = os.listdir(Path("xlsx_files"))
    return tuple(data[data.index('_') + 1:data.index('.xlsx')] for data in content)


if __name__ == "__main__":

    columns: tuple = ('Номер заявки', 'Клиент*' ,'Статус', 'Услуга', 'Дата регистрации заявки')
    dates: tuple = dates_read_from_files()  # написать функцию считывающие с файлов дату
    # print(dates)

    files_data, numbers = read_data(columns, dates)# , applyment_number)
    print(files_data)

    date_slice: tuple = form_date(dates)
    print(date_slice)
    selected_period: tuple = selection_of_period(date_slice, dates)
    print(selected_period)

    print(files_data[dates[0]]['Номер заявки'].value_counts()[:5], '\n')  # топ 5 значений по повторам в первом файле

    applyment_number = return_value('Введите номер заявки > ', np.int64, numbers)

    print(
        *(files_data[data].loc[files_data[data]['Номер заявки'] == applyment] for data in selected_period), sep='\n'
    )
