import click
from aiohttp import web

from views import healthchecker_view, hash_view

app = web.Application()

@click.command()
@click.option('--host', default='0.0.0.0', help='Server host')
@click.option('--port', default=8000, help='Server port')
def run_server(host, port):
    app.add_routes(
        [
            web.get('/healthcheck', healthchecker_view),
            web.post('/hash', hash_view),
        ]
    )
    web.run_app(app, host=host, port=port)

if __name__ == "__main__":
    run_server()