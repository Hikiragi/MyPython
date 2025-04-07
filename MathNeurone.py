from tkinter import *
from tkinter import ttk
from tkinter import font
import random
from tkinter.ttk import Style
from tkinter import messagebox

def close_window(event):
    root.destroy()

def draw_neuron(canvas, num_inputs):
    body_x, body_y, body_radius = 300, 200, 50

    canvas.create_oval(body_x - body_radius, body_y - body_radius,
                       body_x + body_radius, body_y + body_radius,
                       outline="black", width=2)

    left_x, left_y = body_x - body_radius, body_y
    inputs = [(100, 100 + i * 50) for i in range(num_inputs)]
    synapses = [(200, 130 + i * 25) for i in range(num_inputs)]

    for (input_x, input_y), (synapse_x, synapse_y) in zip(inputs, synapses):
        canvas.create_line(input_x, input_y, synapse_x, synapse_y, fill="black", width=2)
        canvas.create_line(synapse_x, synapse_y, left_x, left_y, fill="black", width=2)

    axon_x, axon_y = 450, 200
    canvas.create_line(body_x + body_radius, body_y, axon_x, axon_y, fill="black", width=2)

    output_x, output_y = 500, 200
    canvas.create_oval(output_x - 10, output_y - 10, output_x + 10, output_y + 10, outline="black", width=2)
    canvas.create_line(axon_x, axon_y, output_x, output_y, fill="black", width=2)

    canvas.create_text(80, 80, text="Входы")
    # canvas.create_text(200, 80, text="Синапсы")
    canvas.create_text(body_x, body_y - 80, text="Ячейка\nнейрона")
    canvas.create_text(body_x, body_y, text="S = Σ x_i * w_i")
    # canvas.create_text(450, 180, text="Аксон")
    canvas.create_text(output_x + 50, output_y - 20, text="Выход\n y=f(S)")

    canvas.create_rectangle(body_x - body_radius - 200, body_y - body_radius - 100,
                            body_x + body_radius + 250, body_y + body_radius + 75, outline="black", width=2)

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
    tree.column('RowNumber', width=50, anchor=CENTER)
    for i in range(num_inputs):
        tree.heading(f'Enter{i + 1}', text=f'Вход{i + 1}', anchor=CENTER)
        tree.column(f'Enter{i + 1}', anchor=CENTER)
    tree.heading('MathDisperse', text='Ожидаемый выход', anchor=CENTER)
    tree.column('MathDisperse', anchor=CENTER)
    tree.heading('FactDisperse', text='Фактический выход', anchor=CENTER)
    tree.column('FactDisperse', anchor=CENTER)
    tree.heading('Status', text='Статус', anchor=CENTER)
    tree.column('Status', anchor=CENTER)

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

def update_neuron_and_table():
    canvas.delete("all")
    draw_neuron(canvas, num_inputs)
    for widget in table_frame.winfo_children():
        widget.destroy()
    global tree
    tree = create_table(num_inputs, logic_operation)

def add_input():
    global num_inputs
    if num_inputs < 5:
        num_inputs += 1
        update_neuron_and_table()

def remove_input():
    global num_inputs
    if num_inputs > 1:
        num_inputs -= 1
        update_neuron_and_table()

def toggle_logic_operation():
    global logic_operation
    logic_operation = "OR" if logic_operation == "AND" else "AND"
    logic_label.config(text=f'Текущая логика: {logic_operation}')
    if logic_operation == 'AND':
        enter_w.delete(0, END)
        enter_w.insert(0, '1')
        enter_t.delete(0, END)
        enter_t.insert(0, '3')
    else:
        enter_w.delete(0, END)
        enter_w.insert(0, '1')
        enter_t.delete(0, END)
        enter_t.insert(0, '1')

    update_neuron_and_table()

def randomize_weights():
    enter_w.delete(0, END)
    enter_w.insert(0, str(random.uniform(0, 1)))

def randomize_threshold():
    enter_t.delete(0, END)
    enter_t.insert(0, str(random.uniform(0, 1)))

def reset_values():
    enter_w.delete(0, END)
    enter_t.delete(0, END)
    status_label.config(text="")

def enter_values(event=None):
    weight = enter_w.get()
    threshold = enter_t.get()

    if not weight or not threshold:
        messagebox.showerror("ERROR: Пустой вес/порог", "Пожалуйста, заполните значения веса и порога активации.")
        return

    try:
        weight = float(weight)
        threshold = float(threshold)
    except ValueError:
        messagebox.showerror("ERROR: неверный тип данных", "Пожалуйста, введите корректные числовые значения.")
        return

    all_correct = True
    for item in tree.get_children():
        values = tree.item(item, 'values')
        binary_values = values[1:1 + num_inputs]
        math_disp = values[1 + num_inputs]

        fact_disp = 1 if sum(int(bit) * weight for bit in binary_values) >= threshold else 0
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

    status_label.config(text="Значения оптимальны" if all_correct else "Значения не оптимальны")

root = Tk()
root.title("Математическая модель нейрона")
root.attributes('-fullscreen', True)
root.bind('<Escape>', close_window)

num_inputs = 3
logic_operation = "AND"

enter_w_label = Label(root, text='Значение веса для входов', font=font.Font(size=14))
enter_w = Entry(root, font=font.Font(size=16))
enter_w.insert(0, '1')

enter_t_label = Label(root, text='Порог активации', font=font.Font(size=14))
enter_t = Entry(root, font=font.Font(size=16))
enter_t.insert(1, '3')

btn_refresh = Button(root, text='Сбросить', width=12, height=4, font=font.Font(size=16), command=reset_values)
btn_enter = Button(root, text='Внести', width=12, height=4, font=font.Font(size=16), command=enter_values)

root.bind('<Return>', enter_values)

btn_add_column = Button(root, text='+', font=font.Font(size=18), command=add_input)
btn_delete_column = Button(root, text='-', font=font.Font(size=20), command=remove_input)

btn_toggle_logic = Button(root, text='Переключить логику', font=font.Font(size=16), command=toggle_logic_operation)
btn_randomize_weights = Button(root, text='Случайный вес', font=font.Font(size=16), command=randomize_weights)
btn_randomize_threshold = Button(root, text='Случайный порог', font=font.Font(size=16), command=randomize_threshold)

logic_label = Label(root, text=f'Текущая логика: {logic_operation}', font=font.Font(size=16))
status_label = Label(root, text="", font=font.Font(size=16))

table_frame = Frame(root)
table_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

canvas = Canvas(root, width=600, height=350)
canvas.pack(side=LEFT, anchor='nw')

draw_neuron(canvas, num_inputs)
tree = create_table(num_inputs, logic_operation)

btn_add_column.place(x=400, y=350)
btn_delete_column.place(x=1450, y=350)
enter_w_label.place(x=815, y=350)
enter_w.place(x=810, y=375)
enter_t_label.place(x=1630, y=250)
enter_t.place(x=1590, y=275)
btn_refresh.place(x=400, y=680)
btn_enter.place(x=625, y=680)
btn_toggle_logic.place(x=1330, y=675)
btn_randomize_weights.place(x=1180, y=350)
btn_randomize_threshold.place(x=1600, y=310)
logic_label.place(x=500, y=365)
status_label.place(x=1330, y=750)

root.mainloop()
