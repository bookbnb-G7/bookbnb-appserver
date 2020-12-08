import app.errors.auth_error as ae
from app.services.authsender import AuthSender


def check_token(token):
    if not token:
        raise ae.MissingTokenError()

    if not AuthSender.token_is_valid(token):
        raise ae.MissingTokenError()


"""
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message': 'Missing user token!'}, 400)

        if not AuthSender.is_valid_token(token):
            return make_response({'message': 'Token is invalid!'}, 401)

        return f(*args, **kwargs)

    return decorated

def check_token_and_get_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message' : "Missing user's token."}, 400)

        user_data = auth_service.verify_id_token(token)
        user = User.query.filter_by(email=user_data['email']).first()
        return f(user, *args, **kwargs)
    return decorated

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message' : "Missing user's token."}, 400)

        auth_service.verify_id_token(token)
        return f(*args, **kwargs)
    return decorated
"""