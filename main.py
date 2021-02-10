import pandas as pd
import re


def new_name(name_list: list) -> list:
    """
    Функция преобразует Фамилия Имя Отчество к формату фамилия ио
    :param name_list:
    :return:
    """
    result_arr = []
    for i in name_list:
        string_fio = ""
        if isinstance(i, float):
            continue
        if i.find(".,") != -1:
            i = i.replace(".,", ".")
        fio = i.lower().split(" ")
        first_name = re.sub(r'[^A-Za-z]', '', fio[0])
        last_name = fio[1:]
        string_fio += first_name + " "
        if len(last_name) == 1:
            new_io = re.sub(r'[^A-Za-z]', '', last_name[0])
            if new_io != 2 or new_io != 1:
                new_io = new_io[0]
            string_fio += new_io
        elif len(last_name) == 2:
            string_fio += re.sub(r'[^A-Za-z]', '', last_name[0])[0] + re.sub(r'[^A-Za-z]', '', last_name[1])[0]
        elif len(last_name) == 3:
            string_fio += re.sub(r'[^A-Za-z]', '', last_name[1]) + re.sub(r'[^A-Za-z]', '', last_name[2])
        result_arr.append(string_fio)
    return result_arr


def main():
    df = pd.read_excel("data.xlsx")
    name_list = df['Авторы'].to_list()
    new_name(name_list)
