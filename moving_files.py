import os
import shutil
import time

# Путь к папке "Загрузки"
downloads_path = os.path.expanduser("~/Downloads")

# Путь к папке, куда будут перемещаться файлы
target_path = "F:/PyProjects/SiteWIthFlask/data/data_tests"

# Расширение файлов тестов
test_extention = ".json"


def move_files():
    # Найти все файлы с расширением .json в папке "Загрузки"
    test_files = [f for f in os.listdir(downloads_path) if f.endswith(test_extention)]

    # Переместить каждый файл в папку target_path
    for test_file in test_files:
        shutil.move(os.path.join(downloads_path, test_file), target_path)


if __name__ == "__main__":
    # Запускать функцию move_files каждые 10 секунд
    while True:
        move_files()
        time.sleep(10)
