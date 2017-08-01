import click
from server import TileServer

@click.command()
@click.argument('geospatial_file', nargs=1,
                type=click.Path(exists=True, resolve_path=True))
@click.option('-w', '--workers', default=1,
              help="Number of workers (default=1)")
@click.option('-p', '--port', default="8000",
              help="Port to run the application (default=8000)")
def main(geospatial_file, workers, port):
    """ Starts the tile server """
    options = {
        'bind': '%s:%s' % ('127.0.0.1', port),
        'workers': workers
    }
    TileServer.geospatial_file = geospatial_file
    TileServer(options).run()

