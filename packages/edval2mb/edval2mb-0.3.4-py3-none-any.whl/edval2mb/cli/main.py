import click
import click_config_file
from edval2mb.converter import to_mb


class ContextObject():
    def __init__(self, input_file):
        self.input_file = input_file


@click.group()
@click.argument('input_file', type=click.File('rb'))
@click.pass_context
@click_config_file.configuration_option()
def main(ctx, input_file):
    ctx.obj = ContextObject(input_file)


main.add_command( to_mb )