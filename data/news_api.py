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
    if flask.request.method == 'GET':
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return flask.jsonify(
            {
                'jobs':
                    [item.to_dict()
                     for item in jobs]
            }
        )
    elif flask.request.method == 'POST':
        db_sess = db_session.create_session()
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

