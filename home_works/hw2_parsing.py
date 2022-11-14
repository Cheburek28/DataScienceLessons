from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver



# Функция собирающая статистику со страницы преподователя
def get_teacher(text: str) -> dict:
    soap = text
    try:
        full_name = soap.find(id="firstHeading").text                                         # Имя преподователя
        print(full_name)
    except:
        full_name = ""
    try:
        birth_day = soap.find("th", string="Дата рождения\n").find_next_sibling().text[:-1]   # Дата рождения преподователя
        print(birth_day)
    except:
        birth_day = ""
    try:
        teach_place = soap.find("th", string="Работает\n").find_next_sibling().text[1:-1]     # Кафедра преподователя
        print(teach_place)
    except:
        teach_place = ""
    try:
        degree = soap.find("th", string="Учёная степень\n").find_next_sibling().text[:-1]     # Ученая степень преподователя
        print(degree)
    except:
        degree = ""
    stars = soap.find_all(class_="ratingsinfo-avg")
    knowledge = stars[0].text[:4]                                                             # Оценка знаний
    print(knowledge)
    teaching_skill = stars[1].text[:4]                                                        # Оценка умения преподавать
    print(teaching_skill)
    commication_skill = stars[2].text[:4]                                                     # Оценка умения общаться
    print(commication_skill)
    easy_exam = stars[3].text[:4]                                                             # Оценка легкости экзамена
    print(easy_exam)
    overall_score = stars[4].text[:4]                                                         # Общая средняя оценка
    print(overall_score)
    teacher_dict = {                                                                          # Собираем все данные в словарь
        "full_name": full_name,
        "birth_day": birth_day,
        "teach_place": teach_place,
        "degree": degree,
        "knowledge": knowledge,
        "teaching_skill": teaching_skill,
        "commication_skill": commication_skill,
        "easy_exam": easy_exam,
        "overall_score": overall_score
    }
    return teacher_dict                                                                       # Возвращаем словарь


def homework():
    df_rows = []                                                                              # Пустой датафрейм
    driver = webdriver.Chrome()
    driver.get(url="http://wikimipt.org/wiki/")
    soap = BeautifulSoup(driver.page_source, "lxml")                                          # Получение кода с главной страницы
    all_pages = soap.find(style="column-count: auto; column-width: 21rem;").find_all('a')     # Нахождение всех кафедр
    for page in all_pages:
        page_url = "http://wikimipt.org/wiki" + page.get('href')[10:]                         # Ссылка на кафедры
        driver.get(url=page_url)
        soap_category = BeautifulSoup(driver.page_source, "lxml")                             # Получение кода со страницы кафедры
        try:                                                                                                                   # Случай для кафедр , где нет фотографий преподователей
            maxpage = soap_category.find(style="-moz-column-count:3; column-count:3; -webkit-column-count:3").find_all( 'a')   # Нахождение всех преподователей
            for page_1 in maxpage:                                                                                             # Перебор всех преподователей
                page_1_url = "http://wikimipt.org/wiki" + page_1.get('href')[10:]                                              # Ссылка на преподователя
                driver.get(url=page_1_url)
                time.sleep(2)                                                                                                  # 2 сек пауза, чтобы успели прогрузиться "звездочки"
                soap_teacher = BeautifulSoup(driver.page_source, "lxml")                                                       # Получение кода страницы преподователя
                teacher_dict = get_teacher(soap_teacher)                                                                       # Вызов функции, которая получает данные преподователя
                if teacher_dict:
                    df_rows.append(teacher_dict)                                                                               # Добавление преподователя в словарь
                else:
                    print('ошибка')
        except:
            try:                                                                                                               # Случай для кафедр , где есть фотографии преподователей
                maxpage = soap_category.find_all(class_="gallerytext")                                                         # Нахождение всех преподователей
                for page_1 in maxpage:                                                                                         # Перебор всех преподователей
                    page_1_url = "http://wikimipt.org/wiki" + page_1.find("a").get('href')[10:]                                # Ссылка на преподователя
                    driver.get(url=page_1_url)
                    time.sleep(2)                                                                                              # 2 сек пауза, чтобы успели прогрузиться "звездочки"
                    soap_teacher = BeautifulSoup(driver.page_source, "lxml")                                                   # Получение кода страницы преподователя
                    teacher_dict = get_teacher(soap_teacher)                                                                   # Вызов функции, которая получает данные преподователя
                    if teacher_dict:
                        df_rows.append(teacher_dict)                                                                           # Добавление преподователя в словарь
                    else:
                        print('ошибка')


            except AttributeError as error:
                print('AttributeError', error)
    df = pd.DataFrame().from_dict(df_rows)                                                                                     # Создание датафрейма из словаря преподователей
    df.to_csv("dataframe.csv")                                                                                                 # Преобразовение датафрейма в .csv


if __name__ == "__main__":
    homework()                                                                                                                 # запуск программы
