from flask import Flask, render_template, request, make_response, session, redirect
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.users import User, Jobs




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
    if session.get('name'):
        return render_template('main.html')
    else:
        return 'Вам сюда нельзя'


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
        return render_template('auto_answer.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('auto_answer.html', title='Авторизация', form=form)


@app.route('/registration')
def registration():
    form = Form


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
