import flask
from data.users import User, Jobs
from data import db_session

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/', methods=['GET', 'POST'])
def get_jobs():
    db_sess = db_session.create_session()
    if flask.request.method == 'GET':
        jobs = db_sess.query(Jobs).all()
        return flask.jsonify(
            {
                'jobs':
                    [item.to_dict()
                     for item in jobs]
            }
        )
    elif flask.request.method == 'POST':
        job = Jobs(team_leader=flask.request.json['team_leader'],
                   job=flask.request.json['job'],
                   work_size=flask.request.json['work_size'],
                   collaborators=flask.request.json['collaborators'],
                   is_finished=flask.request.json['is_finished'],
                   id_creator=flask.request.json['id_creator'])
        db_sess.add(job)
        db_sess.commit()
        return flask.make_response(flask.jsonify({'Created': 'True'}), 201)


@blueprint.route('/api/jobs/<job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    try:
        return flask.jsonify(
            {
                'jobs':
                    [jobs.to_dict()]
            }
        )
    except AttributeError:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    except TypeError:
        return flask.make_response(flask.jsonify({'error': 'Error id'}, 404))


@blueprint.route('/api/users/', methods=['GET', 'POST'])
def get_users():
    db_sess = db_session.create_session()
    if flask.request.method == 'GET':
        users = db_sess.query(User).all()
        return flask.jsonify(
            {
                'jobs':
                    [item.to_dict()
                     for item in users]
            }
        )
    elif flask.request.method == 'POST':
        user = User(surname=flask.request.json['surname'],
                    name=flask.request.json['name'],
                    age=flask.request.json['age'],
                    speciality=flask.request.json['speciality'],
                    address=flask.request.json['address'],
                    id_creator=flask.request.json['id_creator'])
        db_sess.add(user)
        db_sess.commit()
        return flask.make_response(flask.jsonify({'Created': 'True'}), 201)


@blueprint.route('/api/users/<int:id_user>', methods=['GET', 'POST', 'DELETE'])
def get_one_users(id_user):  # Получение пользователя
    db_sess = db_session.create_session()
    if flask.request.method == 'GET':
        try:
            user = db_sess.query(User).filter(User.id == id_user).first()
            return flask.jsonify(
                {
                    'jobs':
                        [user.to_dict()]
                }
            )
        except AttributeError:
            return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    elif flask.request.method == 'POST':  # Редактирование пользователя
        editUser = db_sess.query(User).filter(User.id == id_user).first()
        editUser.surname = flask.request.json['surname']
        editUser.name = flask.request.json['name']
        editUser.age = flask.request.json['age']
        editUser.speciality = flask.request.json['speciality']
        editUser.address = flask.request.json['address']
        editUser.id_creator = flask.request.json['id_creator']
        db_sess.add(editUser)
        db_sess.commit()
        return flask.make_response(flask.jsonify({'Accepted': 'True'}), 202)
    elif flask.request.method == 'DELETE':  # Удаление пользователя
        db_sess.query(User).filter(User.id == id_user).first().delete()
        return flask.make_response(flask.jsonify({'OK': 'True'}), 200)
