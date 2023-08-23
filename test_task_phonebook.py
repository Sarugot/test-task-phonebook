import pandas as pd


def correct_number(number):
    '''
    Проверка, что ввод содержит только целочисленные значения.
    '''
    return number[0:].isdigit()


def correct_page(num_of_pages):
    '''
    Проверка на то, что номер страницы соответствует возможному диапазону.
    '''
    page = input("\nВаш ввод: ")
    while True:
        if page[0:].isdigit() and 0 < int(page) <= num_of_pages:
            return int(page)
        print('Некорректный ввод!')
        page = input("\nВаш ввод: ")


def correct_name(name):
    '''
    Проверка, что ввод содержит только буквы.
    '''
    return name.isalpha()


def return_organisation(organisation):
    '''
    Возвращает True при налиичии ввода организации.
    '''
    return organisation


DICT = {"Surname": ['фамилию', correct_name],
        "Name": ['имя', correct_name],
        "Patronymic": ['отчество', correct_name],
        "Organisation": ['название организации', return_organisation],
        "Work_phone": [
            'рабочий телефон (вводите только цифры без пробелов)',
            correct_number
            ],
        "Personal_phone": [
            'персональный телефон (вводите только цифры без пробелов)',
            correct_number
            ]}


def filter_rows(dict):
    '''
    Фильтрация записей по заданным пользователем параметрам.
    Если параметр был введён, он проверятся на соответствие полю, после чего
    добавляется в словарь, из которого потом берутся данные для фильтра.
    '''
    df = pd.read_csv('phonebook.csv', dtype=str)
    search = {}
    for key, value in dict.items():
        print(f"\nВведите для поиска частично или полностью {value[0]} или"
              f" нажмите Enter для пропуска параметра.")
        param = input("\nВаш ввод: ")
        while param and not value[1](param):
            print('Некорректный ввод!')
            param = input("\nВаш ввод: ")
        if param:
            search[key] = param
    for key, value in search.items():
        df = df[df[key].str.contains(value)]
    representation(df)
    return end_commands()


def change_row(dict):
    '''
    Измение записи по её индексу в текстовом файле и заданным параметрам.
    Если параметр был введён, он проверятся на соответствие полю, после чего
    добавляется в словарь, из которого потом берутся данные для изменения
    записи.
    '''
    df = pd.read_csv('phonebook.csv', dtype=str)
    print('Введите номер записи, которую хотите изменить')
    id = input("\nВаш ввод: ")
    while not correct_number(id) or not 0 <= int(id) <= len(df.index)-1:
        print('Некорректный ввод!')
        id = input("\nВаш ввод: ")
    change = {}
    for key, value in dict.items():
        print(f"\nВведите для изменения {value[0]} или"
              f" нажмите Enter для пропуска параметра.")
        change_attribute = input("\nВаш ввод: ")
        while change_attribute and not value[1](change_attribute):
            print('Некорректный ввод!')
            change_attribute = input("\nВаш ввод: ")
        if change_attribute:
            change[key] = change_attribute.capitalize()
    id = int(id)
    for key, value in change.items():
        df.loc[[id], key] = [value]
    df.to_csv('phonebook.csv', index=False, header=True)
    print("\nИзменения сохранены!")
    return end_commands()


def add_row(dict):
    '''
    Добавление новой записи в конец справочника. Пользователь последовательно
    вводит поля, которые проверяются на соответствие.
    '''
    new_row = {}
    for key, value in dict.items():
        print(f"\nВведите {value[0]}.")
        new_attribute = input("\nВаш ввод: ")
        while not value[1](new_attribute):
            print('Некорректный ввод!')
            new_attribute = input("\nВаш ввод: ")
        new_row[key] = new_attribute.capitalize()
    df = pd.DataFrame.from_dict([new_row])
    df.to_csv('phonebook.csv', mode='a', index=False, header=False)
    print("\nЗапись сделана!")
    representation(pd.read_csv('phonebook.csv', dtype=str).tail(1))
    return end_commands()


def choose_page():
    '''
    Функция выбора конкретной страницы для отображения. В ней ведётся подсчёт
    общего числа страниц и ввод номера страницы для последующей передачи в
    функцию отображения записей на странице.
    '''
    df = pd.read_csv('phonebook.csv')
    num_of_pages = df.count()[0] // 10 + 1
    print(f"\nВведите номер страницы. (число страниц: {num_of_pages})")
    page = correct_page(num_of_pages)
    return next_page(df, page, num_of_pages)


def next_page(df, page, num_of_pages):
    '''
    Функция отображений записей на странице. Принимает датафрейм справочника,
    номер страницы, общее число страниц, после чего передаёт данные в функцию
    отображения записей.
    '''
    print(f"\nНомер страницы: {page}")
    representation(df[0+10*(page - 1):10+10*(page - 1)])
    command_list = ["3", "0", "4"]
    if page > 1:
        print("\nДля просмотра предыдущей страницы введите 1")
        command_list.append("1")
    if page <= num_of_pages - 1:
        print("\nДля просмотра следующей страницы введите 2")
        command_list.append("2")
    print(
        "\nДля выбора страницы по номеру введите 3"
        "\n\nДля возврата в главное меню введите 4"
        "\n\nДля выхода из программы введите 0"
        )
    command = input("\nВаш ввод: ")
    while command not in command_list:
        print('Некорректный ввод!')
        command = input("\nВаш ввод: ")
    if command == '4':
        return main_menu()
    elif command == '3':
        return choose_page()
    elif command == '1' and page > 1:
        return next_page(df, page-1, num_of_pages)
    elif command == '2' and page <= num_of_pages - 1:
        return next_page(df, page+1, num_of_pages)
    print("\nВыход из программы.")
    raise SystemExit


def representation(df):
    '''
    Функция отображений записей в удобной для пользователя форме.
    В качестве аргумента принимает датафрейм, в котором находятся нужные
    записи.
    '''
    for ind in df.index:
        print(f"\nНомер записи: {ind}"
              f"\nФамилия: {df['Surname'][ind]}"
              f"\nИмя: {df['Name'][ind]}"
              f"\nОтчество: {df['Patronymic'][ind]}"
              f"\nНазвание организации: {df['Organisation'][ind]}"
              f"\nРабочий телефон: {df['Work_phone'][ind]}"
              f"\nПерсональный телефон: {df['Personal_phone'][ind]}")
    return


def end_commands():
    '''
    Команды для возвращения в главное меню или выхода.
    '''
    print(
        "\nДля возврата в главное меню введите 1"
        "\n\nДля выхода из программы введите 0"
        )
    command = input("\nВаш ввод: ")
    command_list = ["1", "0"]
    while command not in command_list:
        print('Некорректный ввод!')
        command = input("\nВаш ввод: ")
    if command == '1':
        return main_menu()
    print("\nВыход из программы.")
    raise SystemExit


def main_menu():
    '''
    Отображение главного меню со списком команд.
    '''
    print("\nДоступные команды:"
          "\n\nДобавить новую запись — 1"
          "\n\nИзменить существующую запись — 2"
          "\n\nПоиск записи по заданным параметрам — 3"
          "\n\nПросмотреть записи по страницам — 4"
          "\n\nВыйти из программы — 0")
    command = input("\nВаш ввод: ")
    command_list = ["1", "2", "3", "4", "0"]
    while command not in command_list:
        print('Некорректный ввод!')
        command = input("\nВаш ввод: ")
    if command == '1':
        return add_row(DICT)
    elif command == '2':
        return change_row(DICT)
    elif command == '3':
        return filter_rows(DICT)
    elif command == '4':
        return choose_page()
    print("\nВыход из программы.")
    raise SystemExit


def main():
    '''
    Основная функция. Проверяет, есть ли файл справочника, если нет, то
    создаёт, после чего открывает главное меню.
    '''
    try:
        open("phonebook.csv")
    except FileNotFoundError:
        header_list = DICT.keys()
        df = pd.DataFrame(columns=header_list)
        df.to_csv('phonebook.csv', mode='a', index=False, header=True)
        return main_menu()
    else:
        return main_menu()


if __name__ == '__main__':
    main()
