import os
import csv

# Класс коллекции посещений
class VisitCollection:

    # Конструктор класса
    def __init__(self):
        # Список посещений
        self.visits = []

    # Перегрузка функции len()
    def __len__(self):
        return len(self.visits)

    # Метод добавления новой записи
    def add_new_visit(self):

        # Генерация нового номера записи
        if len(self.visits) > 0:
            number = max(visit.number for visit in self.visits) + 1
        else:
            number = 1

        print(f"Номер: {number}")

        # Ввод данных пользователя
        print("Введите ФИО пациента:")
        patient = input()

        print("Введите ФИО врача:")
        doctor = input()

        print("Введите причину обращения:")
        reason = input()

        print("Введите длительность:")
        duration = input_int()

        # Создание объекта посещения
        visit = ClinicVisit(
            number,
            patient,
            doctor,
            reason,
            duration
        )

        # Добавление объекта в коллекцию
        self.add_visit(visit)

    # Метод добавления объекта в список
    def add_visit(self, visit):
        self.visits.append(visit)

    # Перегрузка доступа по индексу
    def __getitem__(self, index):
        return self.visits[index]

    # Итератор для работы с циклом for
    def __iter__(self):
        return iter(self.visits)

    # Генератор фильтрации по длительности
    def filter_by_duration(self, min_duration):

        # Перебор всех записей
        for visit in self.visits:

            # Проверка длительности
            if visit.duration > min_duration:

                # Возврат объекта через генератор
                yield visit

    # Метод загрузки данных из CSV файла
    def load_from_csv(self, filename):

        # Открытие файла для чтения
        with open(filename, "r", encoding="utf-8") as file:

            # Создание объекта чтения CSV
            reader = csv.DictReader(file)

            # Чтение строк файла
            for row in reader:

                # Создание объекта из словаря
                visit = ClinicVisit.from_dict(row)

                # Добавление объекта в коллекцию
                self.visits.append(visit)

    # Метод сохранения данных в CSV файл
    def save_to_csv(self, filename):

        # Открытие файла для записи
        with open(filename, "w", encoding="utf-8", newline="") as file:

            # Список названий столбцов
            fieldnames = ["number", "patient", "doctor", "reason", "duration"]

            # Создание объекта записи CSV
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Запись заголовков
            writer.writeheader()

            # Запись строк в файл
            for visit in self.visits:
                writer.writerow(visit.to_dict())

        return True

    # Метод сортировки по пациенту
    def sort_by_patient(self):

        # Сортировка списка по полю patient
        return sorted(self.visits, key=lambda visit: visit.patient)

    # Метод сортировки по длительности
    def sort_by_duration(self):

        # Сортировка списка по полю duration
        return sorted(self.visits, key=lambda visit: visit.duration)


# Базовый класс медицинской записи
class MedicalRecord:

    # Конструктор класса
    def __init__(self, number):

        # Запись значения через setattr
        setattr(self, "number", number)


# Класс посещения поликлиники
class ClinicVisit(MedicalRecord):

    # Конструктор класса
    def __init__(self, number, patient, doctor, reason, duration):

        # Вызов конструктора родительского класса
        super().__init__(number)

        # Запись свойств объекта через setattr
        setattr(self, "patient", patient)
        setattr(self, "doctor", doctor)
        setattr(self, "reason", reason)
        setattr(self, "duration", duration)

    # Перегрузка строкового представления объекта
    def __repr__(self):

        return f"№{self.number}: {self.patient}, врач: {self.doctor}, причина: {self.reason}, длительность: {self.duration}"

    # Статический метод создания объекта из словаря
    @staticmethod
    def from_dict(row):

        return ClinicVisit(
            int(row["number"]),
            row["patient"],
            row["doctor"],
            row["reason"],
            int(row["duration"])
        )

    # Метод преобразования объекта в словарь
    def to_dict(self):

        return {
            "number": self.number,
            "patient": self.patient,
            "doctor": self.doctor,
            "reason": self.reason,
            "duration": self.duration
        }


# Функция ввода целого числа
def input_int():

    while True:
        try:

            # Ввод числа
            size = int(input())

            # Проверка числа
            if size > 0:
                return size
            else:
                print("Число должно быть больше 0")

        # Обработка ошибки ввода
        except ValueError:
            print("Ошибка: нужно ввести целое число")


# Функция меню
def choose_action(filename):

    # Создание коллекции
    collection = VisitCollection()

    # Загрузка данных из файла
    collection.load_from_csv(filename)

    while True:

        # Вывод меню
        print("\nВыберите действие:")
        print("1 - Отобразить список")
        print("2 - Сортировка по пациентам")
        print("3 - Сортировка по длительности")
        print("4 - Фильтр по длительности")
        print("5 - Добавить запись")
        print("6 - Выход")
        print("7 - Вывод первого элемента списка")

        # Ввод выбора пользователя
        i = input_int()

        # Вывод списка
        if i == 1:

            print(f"Количество записей: {len(collection)}")

            for visit in collection:
                print(visit)

        # Сортировка по пациентам
        elif i == 2:

            print(f"Количество записей: {len(collection)}")
            print("Сортировка по пациентам:")

            sorted_visits = collection.sort_by_patient()

            for visit in sorted_visits:
                print(visit)

        # Сортировка по длительности
        elif i == 3:

            print(f"Количество записей: {len(collection)}")

            sorted_visits = collection.sort_by_duration()

            for visit in sorted_visits:
                print(visit)

        # Фильтр по длительности
        elif i == 4:

            print("Введите минимальную длительность:")
            min_duration = input_int()

            print("Фильтр по длительности:")

            for visit in collection.filter_by_duration(min_duration):
                print(visit)

        # Добавление записи
        elif i == 5:

            # Добавление новой записи
            collection.add_new_visit()

            # Сохранение данных
            if collection.save_to_csv(filename):
                print("\nДанные сохранены\n")
            else:
                print("\nОшибка сохранения\n")

        # Выход из программы
        elif i == 6:
            break

        # Вывод первого элемента списка (для задания)
        elif i == 7:
            print(collection[0])

        # Обработка неверного ввода
        else:
            print("Неправильно")


# Главная функция программы
def main():

    # Путь к CSV файлу
    filename = "C:\\Users\\Home\\Desktop\\University\\4th_semester\\Разработка профессиональных приложений\\Labs\\Lab4\\root\\data.csv"

    # Запуск меню
    choose_action(filename)

    # Коммент для проверки Git
    # Коммент для feature ветки


# Точка входа в программу
main()