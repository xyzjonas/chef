from app.main import bp


@bp.route('/', methods=['GET'])
def root():
    return "Hello world!", 200
