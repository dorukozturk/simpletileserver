import click
from server import TileServer

@click.command()
@click.argument('geospatial_file', nargs=1,
                type=click.Path(exists=True, resolve_path=True))
@click.option('-w', '--workers', default=1,
              help="Number of workers (default=1)")
@click.option('-p', '--port', default="8000",
              help="Port to run the application (default=8000)")
@click.option('-r', '--resample', default='near',
              type=click.Choice(['near', 'bilinear', 'cubic', 'cubicspline',
                                 'lanczos', 'average', 'mode', 'max', 'min',
                                 'med', 'q1', 'q3']),
              help="Resampling method (default=near)")
def main(geospatial_file, workers, port, resample):
    """ Starts the tile server """
    options = {
        'bind': '%s:%s' % ('127.0.0.1', port),
        'workers': workers
    }
    TileServer.geospatial_file = geospatial_file
    TileServer.resampling_method = resample
    TileServer(options).run()

