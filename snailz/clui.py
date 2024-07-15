'''Interface for command-line script.'''

import argparse

from .assays import assays
from .db import db
from .genomes import genomes
from .grid import grid
from .mangle import mangle
from .plates import plates
from .samples import samples
from .survey import survey

from .params import export_params


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for sub in (
            _assays_parser,
            _db_parser,
            _genomes_parser,
            _grid_parser,
            _mangle_parser,
            _params_parser,
            _plates_parser,
            _samples_parser,
            _survey_parser,
    ):
        sub(subparsers)
    options = parser.parse_args()
    options.func(options)


def _assays_parser(subparsers):
    parser = subparsers.add_parser('assays', help='construct assays')
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument('--outfile', type=str, default=None, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--samples', type=str, required=True, help='samples file')
    parser.set_defaults(func=assays)


def _db_parser(subparsers):
    parser = subparsers.add_parser('db', help='construct database')
    parser.add_argument('--assays', type=str, required=True, help='assay data file')
    parser.add_argument('--dbfile', type=str, required=True, help='output database file')
    parser.add_argument('--samples', type=str, required=True, help='samples data file')
    parser.add_argument('--sites', type=str, required=True, help='sites parameter file')
    parser.add_argument('--surveys', type=str, required=True, help='surveys parameter file')
    parser.set_defaults(func=db)


def _genomes_parser(subparsers):
    parser = subparsers.add_parser('genomes', help='construct genomes')
    parser.add_argument('--outfile', type=str, default=None, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.set_defaults(func=genomes)


def _grid_parser(subparsers):
    parser = subparsers.add_parser('grid', help='construct survey grid')
    parser.add_argument('--grids', type=str, required=True, help='grid parameter file')
    parser.add_argument('--outdir', type=str, required=True, help='output directory')
    parser.add_argument('--sites', type=str, required=True, help='site parameter file')
    parser.set_defaults(func=grid)


def _mangle_parser(subparsers):
    parser = subparsers.add_parser('mangle', help='mangle readings files')
    parser.add_argument('--dbfile', type=str, required=True, help='database file')
    parser.add_argument('--outdir', type=str, required=True, help='output directory')
    parser.add_argument('--tidy', type=str, required=True, help='input directory')
    parser.set_defaults(func=mangle)


def _params_parser(subparsers):
    parser = subparsers.add_parser('params', help='export parameter files')
    parser.add_argument('--outdir', type=str, required=True, help='output directory')
    parser.set_defaults(func=export_params)


def _plates_parser(subparsers):
    parser = subparsers.add_parser('plates', help='construct plates')
    parser.add_argument('--assays', type=str, required=True, help='assays file')
    parser.add_argument('--designs', type=str, required=True, help='designs directory')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--readings', type=str, required=True, help='readings directory')
    parser.set_defaults(func=plates)


def _samples_parser(subparsers):
    parser = subparsers.add_parser('samples', help='construct samples')
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument('--grids', type=str, required=True, help='grids directory')
    parser.add_argument('--outfile', type=str, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--sites', type=str, required=True, help='sites parameter file')
    parser.add_argument('--surveys', type=str, required=True, help='surveys parameter file')
    parser.set_defaults(func=samples)


def _survey_parser(subparsers):
    parser = subparsers.add_parser('survey', help='construct survey locations')
    parser.add_argument('--outfile', type=str, required=True, help='output file name')
    parser.add_argument('--samples', type=str, required=True, help='samples data file')
    parser.set_defaults(func=survey)
