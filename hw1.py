import csv
from os.path import exists
from sys import path_hooks


class NameError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_info():
    """Функция получения информации от пользователя."""
    while True:
        try:
            first_name = input("Введите имя: ").strip()
            if len(first_name) < 2:
                raise NameError("Имя должно содержать минимум 2 символа.")

            last_name = input("Введите фамилию: ").strip()
            if len(last_name) < 4:
                raise NameError("Фамилия должна содержать минимум 4 символа.")

            phone_number = input("Введите номер телефона: ").strip()
            if len(phone_number) != 11 or not phone_number.isdigit():
                raise NameError("Номер телефона должен содержать ровно 11 цифр.")

        except NameError as e:
            print(e)
        else:
            return first_name, last_name, phone_number


def create_file(file_name):
    """Создание нового CSV-файла с заголовками столбцов."""
    with open(file_name, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['first_name', 'last_name', 'phone_number'])
        writer.writeheader()


def write_to_file(file_name):
    """Запись новой записи в существующий CSV-файл."""
    if not exists(file_name):
        create_file(file_name)

    user_data = get_info()
    new_entry = {
        'first_name': user_data[0],
        'last_name': user_data[1],
        'phone_number': user_data[2]
    }

    with open(file_name, 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['first_name', 'last_name', 'phone_number'])
        writer.writerow(new_entry)


def read_from_file(file_name):
    """Чтение всех записей из CSV-файла."""
    if not exists(file_name):
        print("Файл отсутствует, создайте файл.")
        return []

    with open(file_name, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def delete_row(file_name):
    """Удаление строки из CSV-файла по номеру строки."""
    if not exists(file_name):
        print("Файл отсутствует, создайте файл.")
        return

    rows = read_from_file(file_name)
    row_index = int(input("Введите номер строки для удаления: "))

    if row_index > len(rows) or row_index <= 0:
        print("Некорректный номер строки.")
        return

    rows.pop(row_index - 1)

    with open(file_name, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['first_name', 'last_name', 'phone_number'])
        writer.writeheader()
        writer.writerows(rows)


def copy_data(source_file, target_file):
    """Копирование данных из одного файла в другой."""
    if not exists(source_file):
        print("Исходный файл отсутствует.")
        return

    records = read_from_file(source_file)
    if not records:
        print("Исходный файл пуст.")
        return

    if not exists(target_file):
        create_file(target_file)

    with open(target_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['first_name', 'last_name', 'phone_number'])
        writer.writeheader()
        writer.writerows(records)


def main():
    source_file = 'source_phone.csv'  # исходный файл
    target_file = 'target_phone.csv'  # целевой файл

    while True:
        print("\nДоступные команды:")
        print("w - Записать новую запись")
        print("r - Прочитать все записи")
        print("d - Удалить запись")
        print("c - Копировать данные из одного файла в другой")
        print("q - Выход\n")

        command = input("Введите команду: ").lower().strip()

        if command == 'q':
            break
        elif command == 'w':
            write_to_file(source_file)
        elif command == 'r':
            for entry in read_from_file(source_file):
                print(entry['first_name'], entry['last_name'], entry['phone_number'])
        elif command == 'd':
            delete_row(source_file)
        elif command == 'c':
            copy_data(source_file, target_file)
        else:
            print("Недопустимая команда. Попробуйте снова.")


if __name__ == "__main__":
    main()