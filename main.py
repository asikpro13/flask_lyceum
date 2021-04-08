from flask import Flask, render_template, request, make_response, session, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.users import User, Jobs
from sqlalchemy import exc


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Местоположение', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobForm(FlaskForm):
    job_title = StringField('Описание работы')
    team_leader_id = IntegerField('Айди лидера')
    work_size = IntegerField('Продолжительность работы')
    collaborators = StringField('Список айди команды')
    is_finished = BooleanField('Работа выполнена?')
    submit = SubmitField('Создать работу')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/mars_explorer.db')
db_sess = db_session.create_session()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    try:
        if session['name']:
            spisok = {}
            try:
                for job in db_sess.query(Jobs).all():
                    spisok[str(job.id)] = {}
                    spisok[str(job.id)]['job'] = str(job.job)
                    team_lead = db_sess.query(User).filter(User.id == job.team_leader).first()
                    spisok[str(job.id)]['team_leader'] = str(team_lead.name + ' ' + team_lead.surname)
                    spisok[str(job.id)]['work_size'] = str(job.work_size) + ' hours'
                    spisok[str(job.id)]['collaborators'] = str(job.collaborators)
                    spisok[str(job.id)]['is_finished'] = job.is_finished
                return render_template('main.html', name=session['name'], form=spisok)
            except exc.InvalidRequestError:
                return redirect('/')
        else:
            return render_template('error.html', error="""
            Вы не прошли авторизацию.
            """)
    except KeyError:
        session['name'] = None
        return


@app.route('/addJobs', methods=['GET', 'POST'])
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        job_form = Jobs()
        job_form.team_leader = form.team_leader_id.data
        job_form.job = form.job_title.data
        job_form.work_size = form.work_size.data
        job_form.collaborators = form.collaborators.data
        job_form.is_finished = form.is_finished.data
        db_sess.add(job_form)
        db_sess.commit()
        return redirect('/')
    return render_template('add_jobs.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            session['name'] = user.surname + ' ' + user.name
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.email = form.email.data
        user.hashed_password = user.set_password(form.email.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        db_sess.add(user)
        db_sess.commit()
        session['name'] = form.surname.data + ' ' + form.name.data
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    session['name'] = None
    return redirect("/")


@app.route('/del_user/<int:del_id>', methods=['GET'])
def del_user(del_id):
    print(del_id)
    db_sess.query(Jobs).filter(Jobs.id == del_id).delete()
    db_sess.commit()
    return jsonify({'result': True}, 200)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
