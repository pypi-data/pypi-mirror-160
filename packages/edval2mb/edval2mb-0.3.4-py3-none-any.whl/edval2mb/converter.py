import pandas as pd
import datetime
import click
import os
from edval2mb.cli.cli_help_strings import *


class Slot:
    def __init__(self):
        self._start = None
        self._end = None

    @property
    def start(self):
        return self._start

    def set_start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    def set_end(self, value):
        self._end = value

    def __repr__(self):
        return f'{self._start.hour}:{self._start.minute:02}-{self._end.hour}:{self._end.minute:02}'

    def item(self):
        return (f'{self._start.hour}:{self._start.minute:02}', f'{self._end.hour}:{self._end.minute:02}')


@click.command('to_mb')
@click.option('--academic-year', 'academic_year', default='', help=academic_year_help)
@click.option('--day-start-index', 'day_start_index', default=1, help=day_start_index_help)
@click.option('--period-start-index', 'period_start_index', default=1, help=period_start_help)
@click.option('--day', 'days', default=('Mon', 'Tue', 'Wed', 'Thu', 'Fri'), multiple=True, help=day_help)
@click.option('--output-path', 'output_path', default='managebac_timetable.csv', help=output_path_help)
@click.argument('fields', nargs=-1)
@click.pass_obj
def to_mb(obj, academic_year, day_start_index, period_start_index, days, output_path, fields):
    # By default the keys are the column names foundi in the file
    columns_mapper_default = {
        key.replace('_', ' '): value
        for key, value in 
        dict(Class='Class ID', Year='year', Periods='dayOfWeek', Start_Time='start_time', End_Time='end_time', Room='Location').items()
    }

    # The user can define additional mappings
    user_fields = dict(zip(fields[::2], fields[1::2]))
    # merge dictionaries with user_fields winning conflict
    columns_mapper = {**columns_mapper_default, **user_fields}
    
    # setup a conversion from days to integers, using passed start index
    paired = zip(days, range(day_start_index, day_start_index + len(days)))
    daysOfWeek = dict(paired)

    # readin, and rename columns for our use
    source: pd.DataFrame = pd.read_csv(obj.input_file)
    source.rename(columns=columns_mapper, inplace=True)

    # add day column converting Mon to day_start_index, etc
    source['Rotation Day Number'] = source['dayOfWeek'].apply(daysOfWeek.get)

    def extract_grade(value):
        if value.isdigit():
            return int(value)
        return None

    source['grade'] = source['year'].apply(extract_grade)
    source = source.dropna(subset=['grade'])

    # convert the start and end times in the csv to sequential period numbers
    # get all the unique values from start and end time pair values
    value_set: pd.array = source.set_index(['start_time', 'end_time']).axes[0].unique().values
    slot_objs: list = []
    for value in value_set:
        slot = Slot()
        for index, setter in enumerate([slot.set_start, slot.set_end]):
            # convert the strings to integer by position
            hour, minute = map(int, value[index].split(':'))
            time = datetime.time(hour=hour, minute=minute)
            setter(time)  # set it via slot object method
        slot_objs.append(slot)

    # sort by start time
    slot_objs.sort(key=lambda x: x.start)

    # TODO: Add checker that it's sequential (this.start > that.end) to guarantee sequential order
    # ManageBac programs can have attendance rotation defined differently, what to do in that case?

    # create paired list 
    paired_list = list(enumerate(map(Slot.item, slot_objs), start=period_start_index))

    # Create start and end time columns with period index
    periods = pd.DataFrame.from_dict(dict(paired_list)).T.rename(columns={0: 'start_time', 1: 'end_time'})
    periods.index.names = ['Period Number']

    # create a reverse lookup table from multi-index star/end time => period
    reverse = periods.reset_index().set_index(['start_time', 'end_time'])

    # convert source to use same index as our reverse lookup table
    source.set_index(['start_time', 'end_time'], inplace=True)

    # now execute and match the values across with a join
    matched = source.join(reverse, how='right')

    matched['Academic Year'] = academic_year

    # filter out what we want, and write
    final_columns = ['Class ID', 'Academic Year', 'Rotation Day Number', 'Period Number', 'Location']
    csv = matched.reset_index()[final_columns].sort_values(final_columns)
    csv.to_csv(output_path, index=False)
    rows, columns = csv.shape
    full_path = os.path.abspath(output_path)
    print(f'Saved csv of {rows+1} rows (including header) and {columns} columns to {full_path}')
