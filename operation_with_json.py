import json, os, datetime
from flask import session

DATA_FILE = 'F:/PyProjects/SiteWIthFlask/data/data_to_flask.json'
TESTS_DIR = 'F:/PyProjects/SiteWithFlask/data/data_tests'


def create_data_file():
    with open(DATA_FILE, 'w', encoding="utf8") as file:
        json.dump({'users': []}, file)


def get_users():
    with open(DATA_FILE, 'r', encoding="utf8") as file:
        data = json.load(file)
        return [
            {'username': user['username'], 'email': user['email'], 'password_hash': user['password_hash'],
             'role': user['role']}
            for user in data['users']
        ]


def save_users(users):
    with open(DATA_FILE, 'w', encoding="utf8") as file:
        json.dump({'users': users}, file)


def user_id_admin(username):
    users = get_users()
    for user in users:
        if user['username'] == username and user['role'] == 'admin':
            return True
    return False


def save_test(name, description, questions):
    tests_dir = 'SiteWithFlask/data/data_tests'  # путь к папке с тестами
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir)  # создать папку, если она не существует
    test_file = os.path.join(tests_dir, f'{name}.json')  # путь к файлу теста
    with open(test_file, 'w', encoding="utf8") as f:
        json.dump({'name': name, 'description': description, 'questions': questions}, f)


def read_test_data(test_name):
    test_file = os.path.join(TESTS_DIR, f'{test_name}.json')
    if not os.path.exists(test_file):
        return None
    with open(test_file, 'r', encoding="utf8") as f:
        return json.load(f)


def save_test_data(test_name, test_data):
    test_file = os.path.join(TESTS_DIR, f'{test_name}.json')
    with open(test_file, 'w', encoding="utf8") as f:
        json.dump(test_data, f)


def save_test_data_to_file(test_name, test_data):
    test_file = os.path.join(TESTS_DIR, f'{test_name}.json')
    with open(test_file, 'w', encoding="utf8") as f:
        json.dump(test_data, f)


def read_tests():
    tests_dir = 'F:/PyProjects/SiteWithFlask/data/data_tests'
    tests = []
    for file in os.listdir(tests_dir):
        if file.endswith('.json'):
            with open(os.path.join(tests_dir, file), 'r', encoding="utf8") as f:
                tests.append(json.load(f))
    return tests


def check_answers(test, answers):
    correct_answers = 0
    for i, question in enumerate(test['questions']):
        if answers[i] == question['correct_answer']:
            correct_answers += 1
    return correct_answers


def save_result(username, test, correct_answers):
    test_name = test['name'].replace(' ', '_')
    date = datetime.datetime.now().strftime('%Y_%m_%d')
    time = datetime.datetime.now().strftime('%H_%M_%S')
    filename = f'{username}-{test_name}-{date}-{time}.json'
    results_dir = 'data/results'
    file_path = os.path.join(results_dir, filename)
    with open(file_path, 'w', encoding="utf8") as f:
        result = {
            'user': username,
            'date': date,
            'time': time,
            'test_name': test['name'],
            'correct_answers': correct_answers
        }
        json.dump(result, f)
    session['results'] = read_results(username)


def read_results(user):
    results_dir = 'F:/PyProjects/SiteWIthFlask/data/results'
    print(f'Results directory: {results_dir}')
    results = []
    for file in os.listdir(results_dir):
        print(f'Reading file: {file}')
        # file_without_spaces = file.replace(' ', '_')

        with open(os.path.abspath(os.path.join(results_dir, file)), 'r', encoding="utf-8") as f:
            result = json.load(f)
            print(f"res_do_filename: {result}")
            result['filename'] = file
            results.append(result)
            print(result)
    return results



