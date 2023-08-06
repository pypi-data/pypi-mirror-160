from flask import request
from contextlib import suppress
from functools import wraps


def call_func(route_acepts=[], args_acepts=[]):
    def capture_func(f):
        @wraps(f)
        def capture_args(*args, **kw):
            try:
                if request.is_json:
                    data = dict(request.json)
                else:
                    data = {**dict(request.form), **dict(request.files)}
            except:
                data = {}
            with suppress(Exception):
                for key, value in request.args.items():
                    if key in args_acepts:
                        data[key] = value
            data = kw.get('data') or data
            for key, value in kw.items():
                if key in route_acepts:
                    data[key] = value
            return f(data=data)
        return capture_args
    return capture_func

if __name__ == '__main__':
    from flask import Flask

    app = Flask(__name__)

    @app.route('/<id>/',methods=['GET','POST'])
    @call_func(route_acepts=['id'],args_acepts=['teste'])
    def index(data):
        return {
            "id":data.get('id'),
            "usuario":"silvio",
            "senha": data.get('teste')
            },400