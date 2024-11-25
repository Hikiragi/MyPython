import networkx as nx
import matplotlib.pyplot as plt


def create_tasks_dict(num_nodes):
    tasks = {}
    for i in range(num_nodes):
        node = chr(ord('A') + i)
        value = input(f"Введите значение на узел {node}: ")
        tasks[node] = int(value)
    return tasks


def create_dependencies_dict(num_nodes):
    dependencies = {}
    for i in range(num_nodes):
        node = chr(ord('A') + i)
        dependencies[node] = []
        while True:
            dependency = input(f"Введите зависимость для узла {node} (или нажмите Enter, чтобы завершить): ").upper()
            if dependency == "":
                break
            if len(dependency) > 1:
                arr = [word.strip() for word in dependency.split(",")]
                dependencies[node] = arr
            else:
                dependencies[node].append(dependency)
    return dependencies


# Функция для вычисления ранних и поздних времен
def calculate_times(G):
    # Инициализация ранних времен
    early_times = {node: 0 for node in G.nodes}

    # Прямой проход для вычисления ранних времен
    for node in nx.topological_sort(G):
        for successor in G.successors(node):
            early_times[successor] = max(early_times[successor], early_times[node] + G.nodes[node]['duration'])

    # Инициализация поздних времен
    late_times = {node: early_times[node] for node in G.nodes}

    # Обратный проход для вычисления поздних времен
    for node in reversed(list(nx.topological_sort(G))):
        for predecessor in G.predecessors(node):
            late_times[predecessor] = min(late_times[predecessor], late_times[node] - G.nodes[node]['duration'])

    return early_times, late_times


# Функция для вычисления отсрочки для узла, введенного пользователем
def calculate_slack(node, early_times, late_times):
    if node == "":
        return 0
    if node in early_times and node in late_times:
        slack = late_times[node] - early_times[node]
        return slack
    else:
        return None


def getTasksAndDependenciems(tas: dict, dep: dict) -> dict:
    for key, val in tas.items():
        print(f"Узел {key} с значением {val}")

    print("/" * 50)
    for key, val in dep.items():
        print(f"Ребро {key} с предыдущей работой от {val}")


# Создаем граф
G = nx.DiGraph()
# Узлы и ребра
num_nodes = int(input("Введите количество узлов: "))
tasks = create_tasks_dict(num_nodes)
dependenciesm = create_dependencies_dict(num_nodes)
getTasksAndDependenciems(tasks, dependenciesm)
# Добавляем узлы в граф
for task in tasks:
    G.add_node(task, duration=tasks[task])

# Добавляем ребра в граф
for task, deps in dependenciesm.items():
    for dep in deps:
        G.add_edge(dep, task)

# Вычисление ранних и поздних времен
early_times, late_times = calculate_times(G)

# Определение критического пути
critical_path = [node for node in G.nodes if early_times[node] == late_times[node]]

# Вывод результатов
print("Минимальное время выполнения проекта:", max(early_times.values()))
print("Работы на критическом пути:", critical_path)
print("Количество работ на критическом пути:", len(critical_path))

# Ввод узла для вычисления отсрочки
user_node = input("Введите узел для вычисления отсрочки: ").upper()
slack = calculate_slack(user_node, early_times, late_times)
if slack is not None:
    print(f"Возможность отсрочки выполнения работы {user_node}: {slack}")
else:
    print(f"Узел {user_node} не найден в графе.")

# Визуализация графа
pos = nx.spring_layout(G)
labels = {node: f"{node}\n{G.nodes[node]['duration']}" for node in G.nodes}
nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
plt.show()
