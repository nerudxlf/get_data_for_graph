import re
from collections import Counter

import pandas as pd


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
            result_arr.append("")
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
    result_dict = {}
    new_dict = {}
    result_list_name, result_list_university = [], []
    name_list = df['Авторы'].to_list()
    university = df['Университет'].to_list()
    country = df['Страна'].to_list()
    name_list_set = list(set(name_list))

    for i in name_list_set:
        new_dict |= {i: []}
    for key, item in new_dict.items():
        for i in range(len(name_list)):
            if name_list[i] == key:
                item.append(university[i])

    for key, item in new_dict.items():
        for i in item:
            if i == "Omsk State Tech Univ" and len(set(item)) > 1:
                result_dict |= {key: "Omsk State Tech Univ+"}
                break
            elif i == "Omsk State Tech Univ" and len(set(item)) == 1:
                result_dict |= {key: "Omsk State Tech Univ"}
                break
            else:
                cnt = Counter(item)
                result_dict |= {key: list(cnt.keys())[0] + "+"}
                break

    for key, item in result_dict.items():
        result_list_name.append(key)
        result_list_university.append(item)

    df_name_university = pd.DataFrame({"Автор": result_list_name, "Университет": result_list_university})
    df_country = pd.DataFrame({"Страна": country, "Автор": name_list})
    result_name_university_country = pd.merge(left=df_name_university, right=df_country, left_on="Автор",
                                              right_on="Автор")
    list_new_name = result_name_university_country["Автор"].to_list()
    list_new_country = result_name_university_country["Страна"].to_list()
    list_new_university = result_name_university_country["Университет"].to_list()
    list_new_name = new_name(list_new_name)
    result = pd.DataFrame({"Автор": list_new_name, "Университет": list_new_university, "Страна": list_new_country})
    result = result.drop_duplicates(keep="last")
    result.to_excel("result_new_new.xlsx", index=False)
