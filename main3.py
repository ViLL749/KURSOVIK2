import tkinter as tk

# Основное окно
root = tk.Tk()
root.title("Тестирование расчетов стоимости")

# Переменная для ввода выбранных типов работы
entry_job_type = tk.Entry(root, width=50)
entry_job_type.pack(pady=10)

# Словарь для хранения стоимости, чтобы можно было редактировать
saved_costs = {}

# Функция для создания окна с выбором типа работы
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

# Функция для создания окна с расчетом стоимости
def open_calculate_cost_window():
    # Создаем новое окно
    cost_window = tk.Toplevel(root)
    cost_window.title("Расчет стоимости")

    # Получаем выбранные типы работ из поля ввода
    job_types = entry_job_type.get().split(", ")

    # Если список пуст, показываем сообщение
    if not job_types[0]:
        job_types = []

    # Словарь для хранения ввода стоимости для каждого типа работы
    job_costs = {}

    # Если нет выбранных работ
    if not job_types:
        tk.Label(cost_window, text="Выберите работы для расчета стоимости").grid(row=0, column=0, padx=5, pady=5)
        return

    # Создаем строки для каждого типа работы
    for idx, job in enumerate(job_types):
        tk.Label(cost_window, text=job).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        cost_entry = tk.Entry(cost_window)
        cost_entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        job_costs[job] = cost_entry  # Сохраняем ссылку на поле ввода для дальнейшего доступа

    # Функция для расчета стоимости
    def calculate_cost():
        total_cost = 0
        for job, entry in job_costs.items():
            try:
                cost = float(entry.get())  # Получаем стоимость из поля ввода
                saved_costs[job] = cost  # Запоминаем стоимость для редактирования
                total_cost += cost
            except ValueError:
                pass  # Игнорируем пустые или неправильные значения

        # Обновляем метку общей стоимости
        update_total_cost_label(total_cost)

    # Кнопка для расчета
    calculate_button = tk.Button(cost_window, text="Рассчитать", command=calculate_cost)
    calculate_button.grid(row=len(job_types), column=0, columnspan=2, pady=10)

    # Метка для отображения общей стоимости
    result_label = tk.Label(cost_window, text="Общая стоимость: 0.00 руб.")
    result_label.grid(row=len(job_types) + 1, column=0, columnspan=2, pady=5)

    # Кнопка для закрытия окна
    close_button = tk.Button(cost_window, text="Закрыть", command=cost_window.destroy)
    close_button.grid(row=len(job_types) + 2, column=0, columnspan=2, pady=5)

    # Обновление общей стоимости в главном окне
    def update_total_cost_label(total_cost):
        result_label.config(text=f"Общая стоимость: {total_cost:.2f} руб.")

# Кнопка для открытия окна с выбором типа работы
open_job_button = tk.Button(root, text="Выбрать типы работ", command=open_job_type_window)
open_job_button.pack(pady=10)

# Кнопка для открытия окна с расчетом стоимости
calculate_button = tk.Button(root, text="Рассчитать стоимость", command=open_calculate_cost_window)
calculate_button.pack(pady=20)

# Запуск основного цикла
root.mainloop()
