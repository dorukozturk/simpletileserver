import click
from dataset import Dataset
from server import TileServer
from client import render_map


@click.command()
@click.argument('geospatial_file', nargs=1,
                type=click.Path(exists=True, resolve_path=True))
@click.option('-w', '--workers', default=1,
              help='Number of workers (default=1)')
@click.option('-p', '--port', default='8000',
              help='Port to run the application (default=8000)')
@click.option('-r', '--resample', default='near',
              type=click.Choice(['near', 'bilinear', 'cubic', 'cubicspline',
                                 'lanczos', 'average', 'mode', 'max', 'min',
                                 'med', 'q1', 'q3']),
              help='Resampling method (default=near)')
@click.option('-m', '--memory', default=1024,
              help='Memory allocated for the warp (default=1024)')
def main(geospatial_file, workers, port, resample, memory):
    """ Starts the tile server """
    options = {
        'bind': '%s:%s' % ('127.0.0.1', port),
        'workers': workers
    }
    dataset = Dataset(geospatial_file, resample, memory)
    TileServer.dataset = dataset
    render_map(dataset.center, dataset.max_zoom_level)
    TileServer(options).run()

