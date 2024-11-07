import tkinter as tk
from tkinter import ttk
import random
import sqlite3
import string
from datetime import datetime, timedelta

# Заполнение рандомом
# def add_sample_records():
#     for record in records:
#         try:
#             conn = sqlite3.connect('data.db')
#             c = conn.cursor()
#
#             # Генерация случайной даты и типа работы
#             random_date = generate_random_date()
#             random_job_type = generate_job_type()
#
#             c.execute('''INSERT INTO clients (fio, date, car_make, car_model, job_type, cost, vin, phone, car_color, license_plate)
#                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                          (record['name'],
#                           random_date,  # Используем случайную дату
#                           random.choice(["Toyota", "Honda", "BMW"]),
#                           random.choice(["Corolla", "Camry", "Rav4", "Civic", "Accord", "CR-V", "3 Series", "5 Series", "X5"]),
#                           random_job_type,  # Используем случайный тип работы
#                           random.randint(1000, 10000),  # Примерная стоимость
#                           ''.join(random.choices(string.ascii_uppercase + string.digits, k=17)),  # Генерация случайного VIN
#                           record['phone'],
#                           random.choice(["Красный", "Черный", "Белый", "Синий"]),
#                           record['gov_number']))
#             conn.commit()
#             conn.close()
#             print(f"Запись {record['name']} добавлена в базу данных.")
#         except sqlite3.Error as e:
#             print("Ошибка при добавлении записи в базу данных:", e)
#
#
# # Возможные буквы для гос. номера
# gov_number_letters = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
#
# def generate_gov_number():
#     # Формат X000XX00
#     first_letter = random.choice(gov_number_letters)  # случайная буква из указанного набора
#     middle_numbers = random.randint(100, 999)  # три цифры
#     second_letter = random.choice(gov_number_letters)  # случайная буква из указанного набора
#     last_numbers = random.randint(10, 99)  # две цифры
#     return f"{first_letter}{middle_numbers}{second_letter}{last_numbers}"
#
#
#
# def generate_phone_number():
#     return f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
#
#
# def generate_name():
#     first_names = ['Алексей', 'Дмитрий', 'Екатерина', 'Мария', 'Иван', 'Светлана', 'Ольга', 'Максим', 'Анастасия',
#                    'Петр']
#     last_names = ['Иванов', 'Петров', 'Сидоров', 'Михайлов', 'Кузнецов', 'Новиков', 'Козлов', 'Попов', 'Смирнов',
#                   'Федоров']
#     patronymics = ['Алексеевич', 'Дмитриевич', 'Иванович', 'Михайлович', 'Петрович', 'Сергеевич', 'Анатольевич',
#                    'Федорович', 'Владимирович', 'Станиславович']
#
#     first_name = random.choice(first_names)
#     last_name = random.choice(last_names)
#     patronymic = random.choice(patronymics)
#
#     return f"{first_name} {last_name} {patronymic}"
#
# # Генерация случайной даты
# def generate_random_date(start_year=2000, end_year=2024):
#     start_date = datetime(start_year, 1, 1)
#     end_date = datetime(end_year, 12, 31)
#     delta = end_date - start_date
#     random_day = start_date + timedelta(days=random.randint(0, delta.days))
#     return random_day.strftime('%d.%m.%Y')
#
# # Генерация случайного типа работы
# job_types = ['Ремонт двигателя', 'Замена тормозных колодок', 'Замена масла', 'Диагностика подвески', 'Ремонт трансмиссии', 'Ремонт кузова', 'Шиномонтаж']
#
# def generate_job_type():
#     return random.choice(job_types)



















# Функция для создания таблицы, если она не существует
def initialize_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 fio TEXT, 
                 date TEXT, 
                 car_make TEXT, 
                 car_model TEXT, 
                 job_type TEXT, 
                 cost REAL,
                 vin TEXT,
                 phone TEXT,
                 car_color TEXT,
                 license_plate TEXT)''')
    conn.commit()
    conn.close()

# Функция для сохранения данных
def save_data():
    fio = entry_fio.get()
    date = entry_date.get()
    car_make = combo_car_make.get()
    car_model = combo_car_model.get()
    job_type = entry_job_type.get()
    cost = entry_cost.get()
    vin = entry_vin.get()
    phone = entry_phone_number.get()
    car_color = entry_car_color.get()
    license_plate = entry_license_plate.get()

    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO clients (fio, date, car_make, car_model, job_type, cost, vin, phone, car_color, license_plate) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (fio, date, car_make, car_model, job_type, cost, vin, phone, car_color, license_plate))
        conn.commit()
        conn.close()
        print("Данные успешно сохранены в базе данных.")
        update_database_view()
    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)

    entry_fio.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_job_type.delete(0, tk.END)
    entry_cost.delete(0, tk.END)
    combo_car_make.set('')
    combo_car_model.set('')
    entry_vin.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_car_color.delete(0, tk.END)
    entry_license_plate.delete(0, tk.END)

def update_car_models(event):
    selected_make = combo_car_make.get()
    models = car_models.get(selected_make, [])
    combo_car_model['values'] = models

def update_database_view():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close()

def select_item(event):
    item = tree.selection()[0]
    values = tree.item(item, "values")
    entry_fio.delete(0, tk.END)
    entry_fio.insert(0, values[1])
    entry_date.delete(0, tk.END)
    entry_date.insert(0, values[2])
    combo_car_make.set(values[3])
    combo_car_model.set(values[4])
    entry_job_type.delete(0, tk.END)
    entry_job_type.insert(0, values[5])
    entry_cost.delete(0, tk.END)
    entry_cost.insert(0, values[6])
    entry_vin.delete(0, tk.END)
    entry_vin.insert(0, values[7])
    entry_phone_number.delete(0, tk.END)
    entry_phone_number.insert(0, values[8])
    entry_car_color.delete(0, tk.END)
    entry_car_color.insert(0, values[9])
    entry_license_plate.delete(0, tk.END)
    entry_license_plate.insert(0, values[10])

def update_data():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item, "values")[0]
    fio = entry_fio.get()
    date = entry_date.get()
    car_make = combo_car_make.get()
    car_model = combo_car_model.get()
    job_type = entry_job_type.get()
    cost = entry_cost.get()
    vin = entry_vin.get()
    phone = entry_phone_number.get()
    car_color = entry_car_color.get()
    license_plate = entry_license_plate.get()

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''UPDATE clients SET fio=?, date=?, car_make=?, car_model=?, job_type=?, cost=?, vin=?, phone=?, car_color=?, license_plate=? WHERE id=?''',
              (fio, date, car_make, car_model, job_type, cost, vin, phone, car_color, license_plate, id))
    conn.commit()
    conn.close()

    update_database_view()

def delete_data():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item, "values")[0]

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''DELETE FROM clients WHERE id=?''', (id,))
    conn.commit()
    conn.close()

    update_database_view()

def add_new_record():
    entry_fio.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    combo_car_make.set('')
    combo_car_model.set('')
    entry_job_type.delete(0, tk.END)
    entry_cost.delete(0, tk.END)
    entry_vin.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_car_color.delete(0, tk.END)
    entry_license_plate.delete(0, tk.END)


sort_order = 'asc'  # Глобальная переменная для отслеживания порядка сортировки


# Функция для сортировки по столбцу
sort_order = 'asc'  # Глобальная переменная для отслеживания порядка сортировки


# Функция для сортировки по столбцу
def sort_by_column(event, column_index):
    global sort_order

    # Сначала убираем стрелочки с заголовков всех столбцов
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Изменяем порядок сортировки при каждом клике
    if sort_order == 'asc':
        sort_order = 'desc'
        tree.heading(tree["columns"][column_index],
                     text=tree.heading(tree["columns"][column_index])['text'].split(' ')[0] + ' ↓')
    else:
        sort_order = 'asc'
        tree.heading(tree["columns"][column_index],
                     text=tree.heading(tree["columns"][column_index])['text'].split(' ')[0] + ' ↑')

    # Получаем все элементы дерева
    items = [(tree.item(item)['values'], item) for item in tree.get_children()]

    # Сортируем элементы в зависимости от выбранного порядка
    items.sort(key=lambda x: x[0][column_index], reverse=(sort_order == 'desc'))

    # Очистим и вставим отсортированные данные
    for item in tree.get_children():
        tree.delete(item)

    for values, item in items:
        tree.insert('', 'end', iid=item, values=values)


# Функция для открытия окна с деталями записи
def open_details_window(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, "values")

    # Создаем новое окно
    details_window = tk.Toplevel(root)
    details_window.title("Детали записи")

    # Поля для отображения деталей записи
    tk.Label(details_window, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[0]).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="ФИО:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[1]).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Дата поступления:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[2]).grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Марка автомобиля:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[3]).grid(row=3, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Модель автомобиля:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[4]).grid(row=4, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Тип работы:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[5]).grid(row=5, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Стоимость:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[6]).grid(row=6, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="VIN:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[7]).grid(row=7, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Номер телефона:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[8]).grid(row=8, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Цвет автомобиля:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[9]).grid(row=9, column=1, padx=5, pady=5, sticky="w")

    tk.Label(details_window, text="Гос номер:").grid(row=10, column=0, padx=5, pady=5, sticky="e")
    tk.Label(details_window, text=values[10]).grid(row=10, column=1, padx=5, pady=5, sticky="w")

    # Сбрасываем фокус с записи
    tree.selection_remove(tree.selection())

root = tk.Tk()
root.title("Автосервис")

root.grid_rowconfigure(11, weight=0)
root.grid_rowconfigure(12, weight=1)
root.grid_columnconfigure(1, weight=1)



# Поля ввода
label_fio = tk.Label(root, text="ФИО:")
label_fio.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_fio = tk.Entry(root)
entry_fio.grid(row=0, column=1, padx=5, pady=5, sticky="we")

label_date = tk.Label(root, text="Дата поступления:")
label_date.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_date = tk.Entry(root)
entry_date.grid(row=1, column=1, padx=5, pady=5, sticky="we")

label_car_make = tk.Label(root, text="Марка автомобиля:")
label_car_make.grid(row=2, column=0, padx=5, pady=5, sticky="e")
car_makes = ["Toyota", "Honda", "BMW"]
combo_car_make = ttk.Combobox(root, values=car_makes)
combo_car_make.grid(row=2, column=1, padx=5, pady=5, sticky="we")
combo_car_make.bind("<<ComboboxSelected>>", update_car_models)

label_car_model = tk.Label(root, text="Модель автомобиля:")
label_car_model.grid(row=3, column=0, padx=5, pady=5, sticky="e")
car_models = {"Toyota": ["Corolla", "Camry", "Rav4"],
              "Honda": ["Civic", "Accord", "CR-V"],
              "BMW": ["3 Series", "5 Series", "X5"]}
combo_car_model = ttk.Combobox(root, values=[])
combo_car_model.grid(row=3, column=1, padx=5, pady=5, sticky="we")

label_job_type = tk.Label(root, text="Тип работы:")
label_job_type.grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_job_type = tk.Entry(root)
entry_job_type.grid(row=4, column=1, padx=5, pady=5, sticky="we")

label_cost = tk.Label(root, text="Рассчетная стоимость:")
label_cost.grid(row=5, column=0, padx=5, pady=5, sticky="e")
entry_cost = tk.Entry(root)
entry_cost.grid(row=5, column=1, padx=5, pady=5, sticky="we")

label_vin = tk.Label(root, text="VIN номер:")
label_vin.grid(row=6, column=0, padx=5, pady=5, sticky="e")
entry_vin = tk.Entry(root)
entry_vin.grid(row=6, column=1, padx=5, pady=5, sticky="we")

label_phone_number = tk.Label(root, text="Номер телефона:")
label_phone_number.grid(row=7, column=0, padx=5, pady=5, sticky="e")
entry_phone_number = tk.Entry(root)
entry_phone_number.grid(row=7, column=1, padx=5, pady=5, sticky="we")

label_car_color = tk.Label(root, text="Цвет автомобиля:")
label_car_color.grid(row=8, column=0, padx=5, pady=5, sticky="e")
entry_car_color = tk.Entry(root)
entry_car_color.grid(row=8, column=1, padx=5, pady=5, sticky="we")

label_license_plate = tk.Label(root, text="Гос номер машины:")
label_license_plate.grid(row=9, column=0, padx=5, pady=5, sticky="e")
entry_license_plate = tk.Entry(root)
entry_license_plate.grid(row=9, column=1, padx=5, pady=5, sticky="we")

# Кнопки
button_save = tk.Button(root, text="Сохранить", command=save_data)
button_save.grid(row=10, column=1, padx=5, pady=5, sticky="we")

button_update = tk.Button(root, text="Изменить", command=update_data)
button_update.grid(row=10, column=0, padx=5, pady=10, sticky="we")

button_delete = tk.Button(root, text="Удалить", command=delete_data)
button_delete.grid(row=11, column=1, padx=5, pady=5, sticky="we")

button_new_record = tk.Button(root, text="Добавить новую запись", command=add_new_record)
button_new_record.grid(row=11, column=0, padx=5, pady=5, sticky="we")

# Просмотр базы данных
tree = ttk.Treeview(root, columns=('ID', 'ФИО', 'Дата поступления', 'Марка', 'Модель', 'Тип работы', 'Стоимость', 'VIN', 'Телефон', 'Цвет автомобиля', 'Гос номер'), show='headings')
# tree.heading('ID', text='ID')
# tree.heading('ФИО', text='ФИО')
# tree.heading('Дата поступления', text='Дата поступления')
# tree.heading('Марка', text='Марка')
# tree.heading('Модель', text='Модель')
# tree.heading('Тип работы', text='Тип работы')
# tree.heading('Стоимость', text='Стоимость')
# tree.heading('VIN', text='VIN')
# tree.heading('Телефон', text='Телефон')
# tree.heading('Цвет автомобиля', text='Цвет автомобиля')
# tree.heading('Гос номер', text='Гос номер')

tree.heading('ID', text='ID')
tree.heading('ФИО', text='ФИО', command=lambda: sort_by_column(None, 1))
tree.heading('Дата поступления', text='Дата поступления', command=lambda: sort_by_column(None, 2))
tree.heading('Марка', text='Марка', command=lambda: sort_by_column(None, 3))
tree.heading('Модель', text='Модель', command=lambda: sort_by_column(None, 4))
tree.heading('Тип работы', text='Тип работы', command=lambda: sort_by_column(None, 5))
tree.heading('Стоимость', text='Стоимость', command=lambda: sort_by_column(None, 6))
tree.heading('VIN', text='VIN', command=lambda: sort_by_column(None, 7))
tree.heading('Телефон', text='Телефон', command=lambda: sort_by_column(None, 8))
tree.heading('Цвет автомобиля', text='Цвет автомобиля', command=lambda: sort_by_column(None, 9))
tree.heading('Гос номер', text='Гос номер', command=lambda: sort_by_column(None, 10))


tree.column("ID", width=30)
tree.column("ФИО", width=150)
tree.column("Дата поступления", width=100)
tree.column("Марка", width=100)
tree.column("Модель", width=100)
tree.column("Тип работы", width=150)
tree.column("Стоимость", width=100)
tree.column("VIN", width=150)
tree.column("Телефон", width=100)
tree.column("Цвет автомобиля", width=100)
tree.column("Гос номер", width=100)


tree.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

tree.bind("<Double-1>", open_details_window)
tree.bind("<ButtonRelease-1>", select_item)


initialize_database()



# Заполнение рандомом
# # Создание 50 записей
# records = []
#
# for _ in range(50):
#     record = {
#         'name': generate_name(),
#         'phone': generate_phone_number(),
#         'gov_number': generate_gov_number(),
#         'address': f"{random.randint(1, 100)} {random.choice(['ул.', 'пр.', 'пл.'])} {random.choice(['Ленина', 'Советская', 'Маяковского', 'Пушкина', 'Чкалова'])}",
#         'email': f"{random.choice(['ivan', 'dmitry', 'maxim', 'olga', 'svetlana', 'anastasia', 'petra'])}{random.randint(100, 999)}@example.com"
#     }
#     records.append(record)
# # Добавляем сгенерированные записи в базу
# add_sample_records()
update_database_view()

root.mainloop()
