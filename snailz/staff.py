'''Generate staff.'''

import faker
from pathlib import Path
import polars as pl
import random
import sys

from .params import StaffParams, load_params


def staff(options):
    '''Main driver.'''
    options.params = load_params(StaffParams, options.params)
    random.seed(options.params.seed)
    faker.Faker.seed(options.params.seed)
    fake = faker.Faker(options.params.locale)
    people = _make_people(options.params, fake)
    _save(options, people)


def _make_people(params, fake):
    '''Create people.'''
    people = [(i+1, fake.first_name(), fake.last_name()) for i in range(params.num)]
    return pl.DataFrame(people, schema=('staff_id', 'personal', 'family'), orient='row')


def _save(options, people):
    '''Save or show results.'''
    if options.outfile:
        people.write_csv(Path(options.outfile))
    else:
        people.write_csv(sys.stdout)
