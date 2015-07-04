from werkzeug.serving import run_simple

from unarea_core.factory import create_app

application = create_app('unarea_server')

def run():
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)

if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)