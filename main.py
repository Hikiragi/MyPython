import json
import os
import subprocess
import time
from threading import Thread
from flask import Flask, render_template, redirect, url_for, flash, abort, request, session, jsonify
from flask_login import login_user, login_required, logout_user, LoginManager, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
# Импорт из отдельного файла
from operation_with_json import create_data_file, get_users, DATA_FILE, user_id_admin, save_test, read_tests, \
    check_answers, save_result, read_results, read_test_data, save_test_data, save_test_data_to_file

app = Flask(__name__)
app.config['TESTS_FOLDER'] = 'data/data_tests'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['LOGIN_VIEW'] = 'login'
app.config['LOGIN_MESSAGE'] = 'Please log in to access this page'
login_manager = LoginManager()
UPLOAD_FOLDER = 'F:/PyProjects/SiteWIthFlask/data/data_materials'


class User(UserMixin):
    def __init__(self, username, email, password_hash, role):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_admin = False
        if self.role == 'admin':
            self.is_admin = True

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


if not os.path.exists(DATA_FILE):
    create_data_file()


@login_manager.user_loader
def load_user(user_id):
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
    for user in data['users']:
        if user['username'] == user_id:
            user.pop('is_admin', None)
            return User(**user)
    return None


# ФОРМЫ
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

    def validate_login(self, user, password):
        users = get_users()
        for u in users:
            if u['Логин'] == user and check_password_hash(u['password_hash'], password) and u['role'] == 'admin':
                return True
        return False


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')


class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(min=1, max=500)])
    correct_answer = StringField('Correct Answer', validators=[DataRequired(), Length(min=1, max=500)])
    choices = []

    def add_choice(self):
        choice = StringField('Choice', validators=[DataRequired(), Length(min=1, max=500)])
        self.choices.append(choice)

    def validate(self):
        if not super().validate():
            return False
        if self.choices and self.correct_answer.data not in [choice.data for choice in self.choices]:
            self.correct_answer.errors.append('You must select one of the choices as the correct answer.')
            return False
        return True


class CreateTestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=500)])
    question_type = SelectField('Question Type', choices=[('text', 'Text'), ('multiple_choice', 'Multiple_choice')])
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField('Create test')


class EditTestForm(FlaskForm):
    name = StringField('Name')
    description = StringField('Description')
    # Add fields for editing questions and options here
    submit = SubmitField('Сохранить изменения')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = get_users()
        for user in users:
            if user['username'] == form.username.data and \
                    check_password_hash(user['password_hash'], form.password.data):
                login_user(User(**user))
                if user['role'] == 'admin':
                    print(f"User {user['username']} logged in as {user['role']}")
                    print(f'Curren_user: {current_user}, Current_user_Role: {current_user.role}')
                    return redirect(url_for('admin_dashboard'))
                elif user['role'] == 'user':
                    print(f"User {user['username']} logged in as {user['role']}")
                    print(f'Curren_user: {current_user}, Current_user_Role: {current_user.role}')
                    return redirect(url_for('view_results'))
    else:
        flash('Login unsuccessful. Please check your username and password.')
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Чтение существующих данных из json-файла
        try:
            with open(DATA_FILE, 'r') as f:
                users_data = json.load(f)
        except FileNotFoundError:
            users_data = {'users': []}
        # Проверка на дублирование username и email
        for user in users_data['users']:
            if user['username'] == form.username.data or user['email'] == form.email.data:
                flash('Username or email already exists. Please choose a different one.')
                return redirect(url_for('register'))

        # Создание нового пользователя и сохранение его данных в json-файл
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role='user'
        )
        users_data['users'].append({
            'username': new_user.username,
            'email': new_user.email,
            'password_hash': new_user.password_hash,
            'role': new_user.role,
            'is_admin': new_user.is_admin
        })
        with open(DATA_FILE, 'w') as file:
            json.dump(users_data, file, indent=4)

        # Вход для нового пользователя
        login_user(new_user)
        flash('Registration successful. You have been logged in.')
        return redirect(url_for('view_results'))
    return render_template('register.html', form=form)


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    is_admin = user_id_admin(current_user.username)
    if is_admin:
        session['is_admin'] = True
        return render_template('admin_dashboard.html')
    else:
        return 'You are not authorized to access the admin dashboard'


@app.route('/create_test', methods=['GET', 'POST'])
@login_required
def create_test():
    print('create_test func called')
    if session.get('is_admin') is None or not session.get('is_admin'):
        return redirect(url_for('login'))
    form = CreateTestForm()
    form.questions.append_entry()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        question_type = form.question_type.data
        return redirect(url_for('admin_dashboard'))
    return render_template('create_test.html', title='Create Test', form=form)


@app.route('/move_files')
def move_files_endpoint():
    def start_move_files():
        time.sleep(15)
        subprocess.run(['python', '/SiteWIthFlask/moving_files.py'])

    Thread(target=start_move_files).start()
    return 'Success', 200


@app.route('/edit_test', methods=['GET', 'POST'])
@login_required
def edit_test():
    print('edit_test func called')
    if session.get('is_admin') is None or not session.get('is_admin'):
        return redirect(url_for('login'))
    form = EditTestForm()
    if not read_tests():
        return render_template('edit_test.html', form=form, message='No tests found. Create a test.',
                               button_text='Create Test', button_link=url_for('create_test'))
    else:
        return render_template('edit_test.html', form=form, tests=read_tests())


@app.route('/edit_test/<test_name>', methods=['GET', 'POST'])
@login_required
def edit_specific_test(test_name):
    print(f'edit_specific_test func called for test: {test_name}')
    if session.get('is_admin') is None or not session.get('is_admin'):
        return redirect(url_for('login'))

    # Read the test data from the JSON file
    test_data = read_test_data(test_name)
    if not test_data:
        return render_template('edit_test.html', message=f'Test "{test_name}" not found.')

    form = EditTestForm(obj=test_data)
    if form.validate_on_submit() and 'save_changes' in request.form:
        # Update the test data with the form data
        test_data['name'] = form.name.data
        test_data['description'] = form.description.data

        # Save the updated test data to the JSON file
        save_test_data_to_file(test_name, test_data)
        return redirect(url_for('edit_specific_test', test_name=test_name))

    if request.method == 'POST':
        # Add the new question to the test data
        new_question = request.get_json()['question']
        test_data['questions'].append(new_question)

        # Save the updated test data to the JSON file
        save_test_data(test_name, test_data)
        return '', 204

    return render_template('edit_specific_test.html', form=form, test_name=test_name, test_data=test_data)


@app.route('/save_test_data', methods=['POST'])
def save_test_data():
    test_name = request.form.get('test_name')
    test_description = request.form.get('test_description')
    questions = request.form.getlist('question[]')

    # Преобразуем строки вождения в списки словарей
    questions_list = []
    for question in questions:
        question_dict = json.loads(question)
        questions_list.append(question_dict)

    test_data = {
        'name': test_name,
        'description': test_description,
        'questions': questions_list,
    }

    save_test_data(test_name, test_data)

    return jsonify({'message': 'Test data saved successfully.'})


def check_answers(test, answers):
    correct_answers = 0
    results = []
    for i, question in enumerate(test['questions']):
        if question['type'] == 'short-answer':
            if answers[i] == question['correct_answer']:
                correct_answers += 1
                results.append({'question': question['text'], 'answer': answers[i], 'correct': True,
                                'explanation': question['explanation']})
            else:
                results.append({'question': question['text'], 'answer': answers[i], 'correct': False,
                                'explanation': question['explanation']})
        elif question['type'] == 'multiple-choice':
            selected_option = next((option for option in question['options'] if option['text'] == answers[i]), None)
            if selected_option and selected_option['correct']:
                correct_answers += 1
                results.append({'question': question['text'], 'answer': answers[i], 'correct': True,
                                'explanation': question['explanation']})
            else:
                results.append({'question': question['text'], 'answer': answers[i], 'correct': False,
                                'explanation': question['explanation']})
    return correct_answers, results


@app.route('/view_tests', methods=['GET', 'POST'])
@login_required
def view_results():
    tests = read_tests()
    all_results = read_results(current_user.username)
    print(f'All_res: {all_results}')
    print(f'User: {current_user.username}')
    if request.method == 'POST':
        test_name = request.form.get('test_name')
        test = next((t for t in tests if t['name'] == test_name), None)
        if test:
            answers = []
            for question in test['questions']:
                answer = request.form.get(f'answer{question["index"]}')
                answers.append(answer)
            correct_answers, results_with_explanations = check_answers(test, answers)
            save_result(current_user.username.replace(' ', '_'), test, correct_answers)
            flash(f'You scored {correct_answers}/{len(test["questions"])} correct answers.')
            results = read_results(current_user.username)
            session['correct_answers'] = correct_answers
            session['results_with_explanations'] = results_with_explanations
            session['results'] = results
            return redirect(url_for('view_results'))
    correct_answers = session.get('correct_answers', 0)
    results_with_explanations = session.get('results_with_explanations', [])
    results = session.get('results', [])
    session.pop('correct_answers', None)
    results_with_explanations = session.pop('results_with_explanations', None)
    return render_template('view_tests.html', tests=tests, results=results, all_results=all_results,
                           results_with_explanations=results_with_explanations,
                           correct_answers=correct_answers)


@app.route("/post_material")
def post_material_page():
    return render_template('post_material.html')


@app.route('/upload_material', methods=['POST'])
def upload_material():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return 'File successfully uploaded', 200


@app.route('/materials')
def materials():
    # Получите список файлов из UPLOAD_FOLDER

    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]

    # Создайте список ссылок для скачивания
    download_links = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        download_link = url_for('download_file', filename=file, _external=True)
        download_links.append((file_path, download_link))

    # Верните список ссылок для скачивания в формате JSON
    import json
    return json.dumps(download_links)


@app.route('/download/<filename>')
def download_file(filename):
    # Верните файл для скачивания
    import os
    from flask import send_from_directory
    return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename, as_attachment=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('is_admin', None)
    return redirect(url_for('login'))


@app.route('/api/save_test', methods=['POST'])
@login_required
def save_test():
    if session.get('is_admin') is None or not session.get('is_admin'):
        return abort(403)
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    questions = data.get('questions')
    if not name or not description or not questions:
        return abort(400)
    save_test(name, description, questions)
    return {'status': 'success', 'message': 'Test saved successfully.'}, 200


login_manager.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
