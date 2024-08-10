'''Generate sample snails with genomes and locations.'''

import json
import math
import numpy as np
from pathlib import Path
import polars as pl
import random
from geopy.distance import lonlat, distance
import sys

from .params import SampleParams, load_params


LON_LAT_PRECISION = 5
READING_PRECISION = 1
SIZE_PRECISION = 1


def samples(options):
    '''Main driver.'''
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(SampleParams, options.params)
    options.surveys = pl.read_csv(options.surveys)
    options.sites = pl.read_csv(options.sites)
    random.seed(options.params.seed)

    genomes = json.loads(Path(options.genomes).read_text())
    grids = _load_grids(options)

    samples = _generate_samples(options, genomes, grids)
    _save(options, samples)


def _generate_samples(options, genomes, grids):
    '''Generate snail samples.

    Snails have mutant phenotype if they have the susceptible gene and
    are in a contaminated location.
    '''

    # Generate.
    samples = []
    for i, seq in enumerate(genomes['individuals']):
        survey_id, point, contaminated = _random_geo(options.sites, options.surveys, grids)
        limit = _size_limit(options, genomes, seq, contaminated)
        size = random.uniform(
            options.params.min_snail_size,
            options.params.min_snail_size + options.params.max_snail_size * limit
        )
        samples.append((i + 1, survey_id, point.longitude, point.latitude, seq, size))

    # Convert to dataframe.
    df = pl.DataFrame(samples, schema=('sample_id', 'survey_id', 'lon', 'lat', 'sequence', 'size'), orient='row')
    return df.with_columns(
        lon=df['lon'].round(LON_LAT_PRECISION),
        lat=df['lat'].round(LON_LAT_PRECISION),
        size=df['size'].round(SIZE_PRECISION),
    )


def _load_grids(options):
    '''Load all grid files.'''
    return {
        s: np.loadtxt(Path(options.grids, f'{s}.csv'), dtype=int, delimiter=',')
        for s in set(options.surveys['site_id'])
    }


def _random_geo(sites, surveys, grids):
    '''Select random (lon, lat) point from a randomly-selected sample grid.'''
    # Get parameters.
    survey_row = random.randrange(surveys.shape[0])
    survey_id = surveys.item(survey_row, 'survey_id')
    spacing = float(surveys.item(survey_row, 'spacing'))
    site_id = surveys.item(survey_row, 'site_id')
    site_row = sites['site_id'].to_list().index(site_id)
    site_lon = sites.item(site_row, 'lon')
    site_lat = sites.item(site_row, 'lat')

    # Get grid information.
    grid = grids[site_id]
    width, height = grid.shape
    rand_x, rand_y = random.randrange(width), random.randrange(height)
    contaminated = bool(grid[rand_x, rand_x] != 0)

    # Generate point.
    corner = lonlat(site_lon, site_lat)
    rand_x *= spacing
    rand_y *= spacing
    dist = math.sqrt(rand_x**2 + rand_y**2)
    bearing = math.degrees(math.atan2(rand_y, rand_x))
    point = distance(meters=dist).destination(corner, bearing=bearing)

    return survey_id, point, contaminated


def _save(options, samples):
    '''Save or show results.'''
    if options.outfile:
        samples.write_csv(Path(options.outfile))
    else:
        samples.write_csv(sys.stdout)


def _size_limit(options, genomes, seq, contaminated):
    '''Calculate upper bound on snail size.'''
    susc_loc = genomes['susceptible_loc']
    susc_base = genomes['susceptible_base']
    if contaminated and (seq[susc_loc] == susc_base):
        return options.params.mutant
    return options.params.normal
