import flask
from data.users import User, Jobs
from data import db_session


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
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
        return flask.make_response
    except TypeError:
        return flask.make_response(flask.jsonify({'error': 'Not found'}, 404))
