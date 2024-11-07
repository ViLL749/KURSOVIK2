import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


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
                 job_type TEXT,   -- сохраняем пару "тип работы : цена"
                 cost REAL,
                 vin TEXT,
                 phone TEXT,
                 car_color TEXT,
                 license_plate TEXT)''')
    conn.commit()
    conn.close()

# Глобальная переменная для хранения итоговой стоимости
total_cost_global = 0  # Это будет итоговая стоимость, которая будет использована в функции save_data


def open_calculate_cost_window():
    print("open_calculate_cost_window вызвано")

    job_types = entry_job_type.get().split(',')  # Разбиваем строку на типы работ

    if not job_types or job_types == ['']:
        messagebox.showwarning("Ошибка", "Типы работы не были выбраны")
        return

    calculate_window = tk.Toplevel(root)
    calculate_window.title("Рассчитать сумму")

    cost_entries = {}  # Словарь для хранения пар "тип работы : стоимость"

    # Создаем поля для ввода стоимости для каждого типа работы
    row = 0
    for job in job_types:
        job = job.strip()
        if job:
            label = tk.Label(calculate_window, text=f"Стоимость для {job}:")
            label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
            cost_entry = tk.Entry(calculate_window)
            cost_entry.grid(row=row, column=1, padx=5, pady=5, sticky="we")
            cost_entries[job] = cost_entry  # Сохраняем поле ввода для каждого типа работы
            row += 1

    # Функция для расчета итоговой суммы
    def calculate():
        total_cost = 0
        job_cost_pairs = []  # Список для хранения пар "тип работы : стоимость"

        # Суммируем стоимости для каждого типа работы
        for job, entry in cost_entries.items():
            try:
                cost_value = float(entry.get())  # Преобразуем введенную стоимость в число
                total_cost += cost_value
                job_cost_pairs.append(f"{job}:{cost_value:.2f}")  # Добавляем пару "тип работы : стоимость"
            except ValueError:
                pass  # Если введена некорректная стоимость, игнорируем

        entry_total.config(text=f"Итого: {total_cost:.2f}")  # Отображаем итоговую сумму
        global total_cost_global
        total_cost_global = total_cost  # Обновляем глобальную переменную с итоговой суммой

        # Обновляем глобальную переменную job_costs
        global job_costs
        job_costs = job_cost_pairs  # Сохраняем пары "тип работы : стоимость" в глобальную переменную

        calculate_window.destroy()  # Закрываем окно калькулятора

    button_calculate = tk.Button(calculate_window, text="Рассчитать", command=calculate)
    button_calculate.grid(row=row, columnspan=2, padx=5, pady=10)








def save_data():
    global total_cost_global
    print(f"total_cost_global перед сохранением: {total_cost_global}")

    if total_cost_global <= 0:
        messagebox.showwarning("Ошибка", "Сумма не была рассчитана.")
        return

    fio = entry_fio.get()
    date = entry_date.get()
    car_make = combo_car_make.get()
    car_model = combo_car_model.get()
    vin = entry_vin.get()
    phone = entry_phone_number.get()
    car_color = entry_car_color.get()
    license_plate = entry_license_plate.get()

    # Разбиваем типы работ из поля ввода
    job_type = entry_job_type.get()
    job_types = job_type.split(',')

    # Преобразуем типы работ в строку, разделенную запятой
    job_type_str = ', '.join([job.strip() for job in job_types if job.strip()])  # Убираем лишние пробелы

    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        # Сохраняем только типы работ, без стоимости
        c.execute('''INSERT INTO clients (fio, date, car_make, car_model, job_type, cost, vin, phone, car_color, license_plate) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (fio, date, car_make, car_model, job_type_str, total_cost_global, vin, phone, car_color,
                   license_plate))
        conn.commit()
        conn.close()

        print("Данные успешно сохранены в базе данных.")
        update_database_view()

        # Очистка глобальной переменной после сохранения
        total_cost_global = 0  # Сбрасываем итоговую стоимость

    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)

    # Очистка полей после сохранения данных
    entry_fio.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_job_type.delete(0, tk.END)
    combo_car_make.set('')
    combo_car_model.set('')
    entry_vin.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_car_color.delete(0, tk.END)
    entry_license_plate.delete(0, tk.END)
    entry_total.config(text="0")


def update_data():
    global total_cost_global
    selected_item = tree.selection()[0]
    id = tree.item(selected_item, "values")[0]
    fio = entry_fio.get()
    date = entry_date.get()
    car_make = combo_car_make.get()
    car_model = combo_car_model.get()
    job_type = entry_job_type.get()
    vin = entry_vin.get()
    phone = entry_phone_number.get()
    car_color = entry_car_color.get()
    license_plate = entry_license_plate.get()

    # Разбиваем строку типов работ
    job_types = job_type.split(',')

    # Преобразуем типы работ в строку, разделенную запятой, для сохранения в базе данных
    job_type_str = ', '.join([job.strip() for job in job_types if job.strip()])


    # Обновляем данные в базе данных
    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(
            '''UPDATE clients SET fio=?, date=?, car_make=?, car_model=?, job_type=?, cost=?, vin=?, phone=?, car_color=?, license_plate=? WHERE id=?''',
            (fio, date, car_make, car_model, job_type_str, total_cost_global, vin, phone, car_color, license_plate, id))
        conn.commit()
        conn.close()


        print("Данные успешно обновлены в базе данных.")
        update_database_view()

        # Очистка глобальной переменной после сохранения
        total_cost_global = 0  # Сбрасываем итоговую стоимость

    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)












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

    # Обновление полей с данными из выбранной строки
    entry_fio.delete(0, tk.END)
    entry_fio.insert(0, values[1])
    entry_date.delete(0, tk.END)
    entry_date.insert(0, values[2])
    combo_car_make.set(values[3])
    combo_car_model.set(values[4])
    entry_job_type.delete(0, tk.END)
    entry_job_type.insert(0, values[5])
    entry_vin.delete(0, tk.END)
    entry_vin.insert(0, values[7])
    entry_phone_number.delete(0, tk.END)
    entry_phone_number.insert(0, values[8])
    entry_car_color.delete(0, tk.END)
    entry_car_color.insert(0, values[9])
    entry_license_plate.delete(0, tk.END)
    entry_license_plate.insert(0, values[10])

    # Получаем значение стоимости из 6-го столбца (предположим, что это стоимость)
    cost = values[6]  # 6-й столбец содержит стоимость

    # Обновляем лейбл "Итого"
    entry_total.config(text=f"Итого: {cost}")  # Обновляем текст лейбла



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
    entry_vin.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_car_color.delete(0, tk.END)
    entry_license_plate.delete(0, tk.END)


# Глобальная переменная для отслеживания порядка сортировки
sort_order = 'asc'  # Стандартный порядок - по возрастанию

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
    # Преобразуем значение столбца в правильный тип для сортировки:
    def get_sort_key(values, column_index):
        value = values[column_index]
        # Преобразуем в числа для сортировки по числовым значениям
        try:
            return float(value)
        except ValueError:
            return value  # если не число, то оставляем строку (по алфавиту)

    # Сортируем
    items.sort(key=lambda x: get_sort_key(x[0], column_index), reverse=(sort_order == 'desc'))

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




def open_job_type_window():
    # Создаем новое окно (Toplevel)
    job_window = tk.Toplevel(root)
    job_window.title("Выбор типа работы")

    # Переменные для чекбоксов
    var_work_type1 = tk.BooleanVar()
    var_work_type2 = tk.BooleanVar()
    var_work_type3 = tk.BooleanVar()

    # Чекбоксы для выбора типа работы
    checkbox_job_type1 = tk.Checkbutton(job_window, text="Диагностика", variable=var_work_type1)
    checkbox_job_type1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    checkbox_job_type2 = tk.Checkbutton(job_window, text="Ремонт", variable=var_work_type2)
    checkbox_job_type2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    checkbox_job_type3 = tk.Checkbutton(job_window, text="Обслуживание", variable=var_work_type3)
    checkbox_job_type3.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    # Функция для добавления выбранных типов работы в поле ввода
    def add_selected_jobs():
        selected_jobs = []

        # Проверяем, какие чекбоксы выбраны и добавляем в список
        if var_work_type1.get():
            selected_jobs.append("Диагностика")
        if var_work_type2.get():
            selected_jobs.append("Ремонт")
        if var_work_type3.get():
            selected_jobs.append("Обслуживание")

        # Получаем текущий текст из поля ввода
        current_text = entry_job_type.get()

        # Разделяем текущий текст на отдельные типы работы и удаляем пустые элементы
        existing_jobs = set(current_text.split(",")) if current_text else set()

        # Добавляем только те работы, которые еще не были добавлены
        new_jobs = [job for job in selected_jobs if job not in existing_jobs]

        # Если есть новые работы, обновляем текст
        if new_jobs:
            if current_text:
                current_text += ", " + ", ".join(new_jobs)
            else:
                current_text = ", ".join(new_jobs)

        # Обновляем поле ввода
        entry_job_type.delete(0, tk.END)
        entry_job_type.insert(0, current_text)

        # Закрываем окно Toplevel
        job_window.destroy()

    # Кнопка для сохранения выбора
    save_button = tk.Button(job_window, text="Сохранить", command=add_selected_jobs)
    save_button.grid(row=3, column=0, padx=5, pady=5)











root = tk.Tk()
root.title("Автосервис")




root.grid_rowconfigure(14, weight=0)
root.grid_rowconfigure(15, weight=1)
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

# Лейбл для итоговой суммы
label_total = tk.Label(root, text="Итого: ")
label_total.grid(row=7, column=0, padx=5, pady=5, sticky="e")
entry_total = tk.Label(root, text="0")  # Изначально сумма 0
entry_total.grid(row=7, column=1, padx=5, pady=5, sticky="we")

label_vin = tk.Label(root, text="VIN номер:")
label_vin.grid(row=8, column=0, padx=5, pady=5, sticky="e")
entry_vin = tk.Entry(root)
entry_vin.grid(row=8, column=1, padx=5, pady=5, sticky="we")

label_phone_number = tk.Label(root, text="Номер телефона:")
label_phone_number.grid(row=9, column=0, padx=5, pady=5, sticky="e")
entry_phone_number = tk.Entry(root)
entry_phone_number.grid(row=9, column=1, padx=5, pady=5, sticky="we")

label_car_color = tk.Label(root, text="Цвет автомобиля:")
label_car_color.grid(row=10, column=0, padx=5, pady=5, sticky="e")
entry_car_color = tk.Entry(root)
entry_car_color.grid(row=10, column=1, padx=5, pady=5, sticky="we")

label_license_plate = tk.Label(root, text="Гос номер машины:")
label_license_plate.grid(row=11, column=0, padx=5, pady=5, sticky="e")
entry_license_plate = tk.Entry(root)
entry_license_plate.grid(row=11, column=1, padx=5, pady=5, sticky="we")

# Кнопки
button_calculate_cost = tk.Button(root, text="Рассчитать сумму", command=open_calculate_cost_window)
button_calculate_cost.grid(row=6, column=1, padx=5, pady=5, sticky="we")

button_select_job_type = tk.Button(root, text="Выбрать тип работы", command=open_job_type_window)
button_select_job_type.grid(row=5, column=1, padx=5, pady=5, sticky="we")

button_save = tk.Button(root, text="Сохранить", command=save_data)
button_save.grid(row=12, column=1, padx=5, pady=5, sticky="we")

button_update = tk.Button(root, text="Изменить", command=update_data)
button_update.grid(row=12, column=0, padx=5, pady=10, sticky="we")

button_delete = tk.Button(root, text="Удалить", command=delete_data)
button_delete.grid(row=13, column=1, padx=5, pady=5, sticky="we")

button_new_record = tk.Button(root, text="Добавить новую запись", command=add_new_record)
button_new_record.grid(row=13, column=0, padx=5, pady=5, sticky="we")



# Просмотр базы данных
tree = ttk.Treeview(root, columns=('ID', 'ФИО', 'Дата поступления', 'Марка', 'Модель', 'Тип работы', 'Стоимость', 'VIN', 'Телефон', 'Цвет автомобиля', 'Гос номер'), show='headings')


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


tree.grid(row=15, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

tree.bind("<Double-1>", open_details_window)
tree.bind("<ButtonRelease-1>", select_item)


initialize_database()




update_database_view()

root.mainloop()
