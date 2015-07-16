from unarea_core.build import create_app
server = create_app()

server.run(host='127.0.0.1', port=1234)

def run_local():
    server.run(host='localhost', port=5555)
