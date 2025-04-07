from tkinter import *
from tkinter import ttk
from tkinter import font
import random
from tkinter.ttk import Style
from tkinter import messagebox


# Функция бинда на закрытие приложения
def close_window(event):
    root.destroy()


# Функция рисования нейрона
def draw_neuron(canvas, num_inputs):
    body_x, body_y, body_radius = 300, 200, 50

    canvas.create_oval(body_x - body_radius, body_y - body_radius,
                       body_x + body_radius, body_y + body_radius,
                       outline="black", width=2)

    left_x, left_y = body_x - body_radius, body_y
    inputs = [(100, 100 + i * 50) for i in range(num_inputs)]
    synapses = [(200, 130 + i * 25) for i in range(num_inputs)]

    # Нулевой вход (смещение)
    canvas.create_line(100, 50, 200, 100, fill="blue", width=2, dash=(4, 2))
    canvas.create_line(200, 100, left_x, left_y, fill="blue", width=2, dash=(4, 2))
    canvas.create_text(80, 30, text="x₀ (смещение)", fill="blue")

    for i, ((input_x, input_y), (synapse_x, synapse_y)) in enumerate(zip(inputs, synapses)):
        canvas.create_line(input_x, input_y, synapse_x, synapse_y, fill="black", width=2)
        canvas.create_line(synapse_x, synapse_y, left_x, left_y, fill="black", width=2)
        canvas.create_text(input_x - 30, input_y, text=f"x{i + 1}")

    axon_x, axon_y = 450, 200
    canvas.create_line(body_x + body_radius, body_y, axon_x, axon_y, fill="black", width=2)

    output_x, output_y = 500, 200
    canvas.create_oval(output_x - 10, output_y - 10, output_x + 10, output_y + 10, outline="black", width=2)
    canvas.create_line(axon_x, axon_y, output_x, output_y, fill="black", width=2)

    canvas.create_text(80, 80, text="Входы")
    canvas.create_text(body_x, body_y - 80, text="Ядро\nнейрона")
    canvas.create_text(body_x, body_y, text="S = Σ x_i * w_i")
    canvas.create_text(output_x + 50, output_y - 20, text="Выход\n y=f(S)")

    canvas.create_rectangle(body_x - body_radius - 200, body_y - body_radius - 100,
                            body_x + body_radius + 250, body_y + body_radius + 75, outline="black", width=2)


# Функция создания таблиц
def create_table(num_inputs, logic_operation):
    columns = ('RowNumber',) + tuple(f'Enter{i + 1}' for i in range(num_inputs)) + (
        'MathDisperse', 'FactDisperse', 'Status')
    style = Style()
    style.configure('Treeview', rowheight=25)

    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(fill=BOTH, expand=1)
    tree.heading('RowNumber', text='№', anchor=CENTER)
    tree.column('RowNumber', width=30, anchor=CENTER)  # Уменьшил ширину
    for i in range(num_inputs):
        tree.heading(f'Enter{i + 1}', text=f'x{i + 1}', anchor=CENTER)
        tree.column(f'Enter{i + 1}', width=30, anchor=CENTER)  # Уменьшил ширину
    tree.heading('MathDisperse', text='Ожид.', anchor=CENTER)
    tree.column('MathDisperse', width=50, anchor=CENTER)
    tree.heading('FactDisperse', text='Факт.', anchor=CENTER)
    tree.column('FactDisperse', width=50, anchor=CENTER)
    tree.heading('Status', text='Статус', anchor=CENTER)
    tree.column('Status', width=60, anchor=CENTER)

    for i in range(2 ** num_inputs):
        binary_values = format(i, f'0{num_inputs}b')
        conjunction = '1' if (logic_operation == "AND" and all(bit == '1' for bit in binary_values)) or \
                             (logic_operation == "OR" and any(bit == '1' for bit in binary_values)) else '0'
        row_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=(i + 1,) + tuple(binary_values) + (conjunction, '', ''), tags=(row_tag,))

    tree.tag_configure('evenrow', background='#f0f0ff')
    tree.tag_configure('oddrow', background='#ffffff')
    tree.tag_configure('correct', background='#d4edda')
    tree.tag_configure('incorrect', background='#f8d7da')

    return tree


# Функция изменения рисунка и таблицы
def update_neuron_and_table():
    canvas.delete("all")
    draw_neuron(canvas, num_inputs)
    for widget in table_frame.winfo_children():
        widget.destroy()
    global tree
    tree = create_table(num_inputs, logic_operation)
    update_weight_entries()
    clear_calculations()


def update_weight_entries():
    # Удаляем старые поля ввода весов
    for widget in weight_frame.winfo_children():
        widget.destroy()

    # Создаем новые поля ввода для каждого входа
    global weight_entries
    weight_entries = []
    Label(weight_frame, text='Веса входов:', font=font.Font(size=14)).pack(side=LEFT, padx=5)

    # Вес смещения (w0)
    frame = Frame(weight_frame)
    frame.pack(side=LEFT, padx=5)
    Label(frame, text='w₀ (смещение):', font=font.Font(size=12)).pack(side=LEFT)
    entry = Entry(frame, font=font.Font(size=12), width=5)
    entry.pack(side=LEFT)
    entry.insert(0, f'-{float(num_inputs - 0.5 if logic_operation == "AND" else 0.5)}')
    weight_entries.append(entry)

    # Веса входов (w1, w2, ...)
    for i in range(num_inputs):
        frame = Frame(weight_frame)
        frame.pack(side=LEFT, padx=5)
        Label(frame, text=f'w{i + 1}:', font=font.Font(size=12)).pack(side=LEFT)
        entry = Entry(frame, font=font.Font(size=12), width=5)
        entry.pack(side=LEFT)
        entry.insert(0, '1' if i == 0 else '0')  # Первый вес 1, остальные 0 по умолчанию
        weight_entries.append(entry)


# Функция добавления входа
def add_input():
    global num_inputs
    if num_inputs < 5:
        num_inputs += 1
        update_neuron_and_table()


# Функция удаления входа
def remove_input():
    global num_inputs
    if num_inputs > 1:
        num_inputs -= 1
        update_neuron_and_table()


# Функция изменения логики построения таблицы
def toggle_logic_operation():
    global logic_operation
    logic_operation = "OR" if logic_operation == "AND" else "AND"
    logic_label.config(text=f'Текущая логика: {logic_operation}')
    update_neuron_and_table()
    # Обновляем значение w0 при смене логики
    weight_entries[0].delete(0, END)
    weight_entries[0].insert(0, f'-{float(num_inputs - 0.5 if logic_operation == "AND" else 0.5)}')


# Функция задания случайных весов
def randomize_weights():
    for entry in weight_entries:
        entry.delete(0, END)
        entry.insert(0, str(round(random.uniform(-1, 1), 2)))


# Функция сброса значений
def reset_values():
    global logic_operation
    for entry in weight_entries:
        entry.delete(0, END)
    status_label.config(text="")
    clear_calculations()
    # Устанавливаем значения по умолчанию
    weight_entries[0].insert(0, f'-{float(num_inputs - 0.5 if logic_operation == "AND" else 0.5)}')  # Смещение/порог
    for i in range(1, len(weight_entries)):
        weight_entries[i].insert(0, '1' if i == 1 else '0')  # Первый вес 1, остальные 0


# Функция очистки области расчетов
def clear_calculations():
    for widget in calculation_frame.winfo_children():
        widget.destroy()
    Label(calculation_frame, text="Расчеты будут отображаться здесь после нажатия кнопки 'Внести'",
          font=font.Font(size=12), fg="gray").pack(pady=20)


# Функция отображения расчетов
def show_calculations(weights):
    # Очищаем предыдущие расчеты
    for widget in calculation_frame.winfo_children():
        widget.destroy()

    # Создаем контейнер для canvas и scrollbar
    container = Frame(calculation_frame)
    container.pack(fill=BOTH, expand=True)

    # Создаем canvas с двумя scrollbar
    calc_canvas = Canvas(container, width=550, height=200)
    h_scrollbar = Scrollbar(container, orient="horizontal", command=calc_canvas.xview)
    v_scrollbar = Scrollbar(container, orient="vertical", command=calc_canvas.yview)

    scrollable_frame = Frame(calc_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: calc_canvas.configure(
            scrollregion=calc_canvas.bbox("all")
        )
    )

    calc_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    calc_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

    # Размещаем элементы
    h_scrollbar.pack(side=BOTTOM, fill=X)
    v_scrollbar.pack(side=RIGHT, fill=Y)
    calc_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Создаем фрейм для заголовков
    header_frame = Frame(scrollable_frame)
    header_frame.pack(fill=X)

    # Заголовки таблицы
    columns = [
        ("№", 30),  # Номер строки
        *[(f"x{i + 1}", 30) for i in range(num_inputs)],  # Входные значения
        ("x₀", 30),  # Смещение (всегда 1)
        *[(f"w{i}", 50) for i in range(num_inputs + 1)],  # Веса (включая w0)
        ("Σ", 60), ("Выход", 60)
    ]

    # Отображаем заголовки
    for i, (text, width) in enumerate(columns):
        frame = Frame(header_frame, width=width, height=25)
        frame.pack_propagate(0)
        frame.pack(side=LEFT, padx=1)
        Label(frame, text=text, font=font.Font(size=10, weight='bold'),
              anchor='center').pack(fill=BOTH, expand=1)

        # Добавляем разделитель после всех входов (после x₀)
        if i == 2 + num_inputs:  # Это позиция после x₀
            separator = Frame(header_frame, width=2, bg='gray')
            separator.pack(side=LEFT, padx=2, fill=Y)

    # Добавляем разделительную линию под заголовками
    separator = Frame(scrollable_frame, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, pady=2)

    # Добавляем расчеты для каждой строки
    for item in tree.get_children():
        values = tree.item(item, 'values')
        binary_values = values[1:1 + num_inputs]
        math_disp = values[1 + num_inputs]

        # Создаем фрейм для строки расчетов
        row_frame = Frame(scrollable_frame)
        row_frame.pack(fill=X)

        # Номер строки
        frame = Frame(row_frame, width=30, height=25)
        frame.pack_propagate(0)
        frame.pack(side=LEFT, padx=1)
        Label(frame, text=values[0], anchor='center').pack(fill=BOTH, expand=1)

        # Входные значения (x1, x2, ...)
        for val in binary_values:
            frame = Frame(row_frame, width=30, height=25)
            frame.pack_propagate(0)
            frame.pack(side=LEFT, padx=1)
            Label(frame, text=val, anchor='center').pack(fill=BOTH, expand=1)

        # Смещение (x0) - всегда 1
        frame = Frame(row_frame, width=30, height=25)
        frame.pack_propagate(0)
        frame.pack(side=LEFT, padx=1)
        Label(frame, text="1", anchor='center').pack(fill=BOTH, expand=1)

        # Веса (w0, w1, w2, ...)
        for i in range(num_inputs + 1):
            frame = Frame(row_frame, width=50, height=25)
            frame.pack_propagate(0)
            frame.pack(side=LEFT, padx=1)
            Label(frame, text=f"{weights[i]:.2f}", anchor='center').pack(fill=BOTH, expand=1)

        # Разделитель между весами и суммой
        separator = Frame(row_frame, width=2, bg='gray')
        separator.pack(side=LEFT, padx=2, fill=Y)

        # Вычисляем сумму (включая смещение)
        total = weights[0] * 1  # x0 всегда 1 (смещение)
        for i in range(num_inputs):
            total += int(binary_values[i]) * weights[i + 1]

        # Сумма
        frame = Frame(row_frame, width=60, height=25)
        frame.pack_propagate(0)
        frame.pack(side=LEFT, padx=1)
        Label(frame, text=f"{total:.2f}", anchor='center').pack(fill=BOTH, expand=1)

        # Выход (активация)
        output = 1 if total >= 0 else 0
        frame = Frame(row_frame, width=60, height=25)
        frame.pack_propagate(0)
        frame.pack(side=LEFT, padx=1)
        bg_color = '#d4edda' if output == int(math_disp) else '#f8d7da'
        Label(frame, text=output, anchor='center', bg=bg_color).pack(fill=BOTH, expand=1)

    # Устанавливаем минимальную ширину для корректного отображения
    calc_canvas.config(scrollregion=calc_canvas.bbox("all"))
    calc_canvas.xview_moveto(0)
    calc_canvas.yview_moveto(0)


# Функция внесения значений
def enter_values(event=None):
    try:
        weights = [float(entry.get()) for entry in weight_entries]
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для всех весов.")
        return

    all_correct = True
    for item in tree.get_children():
        values = tree.item(item, 'values')
        binary_values = values[1:1 + num_inputs]
        math_disp = values[1 + num_inputs]

        # Вычисляем сумму (включая смещение)
        total = weights[0] * 1  # x0 всегда 1 (смещение)
        for i in range(num_inputs):
            total += int(binary_values[i]) * weights[i + 1]

        fact_disp = 1 if total >= 0 else 0
        tree.set(item, 'FactDisperse', fact_disp)
        status = "верно" if math_disp == str(fact_disp) else "неверно"
        tree.set(item, 'Status', status)

        new_tags = list(tree.item(item, 'tags'))
        if status == "верно":
            new_tags.append('correct')
        else:
            new_tags.append('incorrect')
            all_correct = False
        tree.item(item, tags=new_tags)

    status_label.config(text="Нейрон обучен" if all_correct else "Нейрон не обучен")

    # Показываем расчеты
    show_calculations(weights)


root = Tk()
root.title("Математическая модель нейрона")
root.attributes('-fullscreen', True)
root.bind('<Escape>', close_window)

num_inputs = 3
logic_operation = "AND"
weight_entries = []

# Основной интерфейс
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)

# Левая панель (нейрон и расчеты)
left_panel = Frame(main_frame)
left_panel.pack(side=LEFT, fill=BOTH, padx=10, pady=10)

# Верхняя часть левой панели (рисунок нейрона)
neuron_frame = Frame(left_panel)
neuron_frame.pack(fill=X)

canvas = Canvas(neuron_frame, width=600, height=350)
canvas.pack()

# Нижняя часть левой панели (расчеты)
calculation_frame = Frame(left_panel, bd=2, relief=GROOVE, padx=5, pady=5, height=200)
calculation_frame.pack(fill=BOTH, expand=False, pady=(10, 0))
calculation_frame.pack_propagate(0)

# Добавляем заглушку для расчетов
Label(calculation_frame, text="Расчеты будут отображаться здесь после нажатия кнопки 'Внести'",
      font=font.Font(size=12), fg="gray").pack(pady=20)

# Правая панель (управление)
right_panel = Frame(main_frame)
right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

# Панель управления входами
input_control_frame = Frame(right_panel)
input_control_frame.pack(fill=X, pady=5)

btn_add_column = Button(input_control_frame, text='+', font=font.Font(size=18), command=add_input)
btn_add_column.pack(side=LEFT, padx=5)

btn_delete_column = Button(input_control_frame, text='-', font=font.Font(size=18), command=remove_input)
btn_delete_column.pack(side=LEFT, padx=5)

logic_label = Label(input_control_frame, text=f'Текущая логика: {logic_operation}', font=font.Font(size=16))
logic_label.pack(side=LEFT, padx=20)

btn_toggle_logic = Button(input_control_frame, text='Переключить логику', font=font.Font(size=16),
                          command=toggle_logic_operation)
btn_toggle_logic.pack(side=LEFT, padx=5)

# Панель весов
weight_frame = Frame(right_panel)
weight_frame.pack(fill=X, pady=10)

btn_randomize_weights = Button(weight_frame, text='Случайные веса', font=font.Font(size=14), command=randomize_weights)
btn_randomize_weights.pack(side=LEFT, padx=10)

# Таблица
table_frame = Frame(right_panel)
table_frame.pack(fill=BOTH, expand=True, pady=10)

# Кнопки ввода
button_frame = Frame(right_panel)
button_frame.pack(fill=X, pady=10)

btn_refresh = Button(button_frame, text='Сбросить', width=12, height=2, font=font.Font(size=16), command=reset_values)
btn_refresh.pack(side=LEFT, padx=10)

btn_enter = Button(button_frame, text='Внести', width=12, height=2, font=font.Font(size=16), command=enter_values)
btn_enter.pack(side=LEFT, padx=10)

status_label = Label(right_panel, text="", font=font.Font(size=16))
status_label.pack(side=LEFT, pady=6, padx=3)

root.bind('<Return>', enter_values)

# Инициализация
update_neuron_and_table()
reset_values()  # Установка значений по умолчанию

root.mainloop()
