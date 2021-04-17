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
    print(jobs)
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


@blueprint.route('/api/users/', methods=['GET', 'POSTS'])
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


@blueprint.route('/api/users/<int:id_user>', methods=['GET'])
def get_one_users(id_user):
    db_sess = db_session.create_session()
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
