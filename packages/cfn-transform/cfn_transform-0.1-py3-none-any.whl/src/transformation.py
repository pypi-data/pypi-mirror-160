import click
import json

from cfnlint import decode
from cfnlint import Transform

# CLI for transforming SAM Templates
@click.command()
@click.option('-f','--file', 'output_file', help='Ouput result to specified file')
@click.argument('input')
def cli(input, output_file):
    (json_file, errors) = decode.decode(input)
    if errors:
        for match in errors:
            click.echo(match, err=True)
        exit(1)
    transformer = Transform(input, json_file, 'us-east-1')
    transformer.transform_template()
    if output_file:
        with click.open_file(output_file,'w') as output:
            output.write(json.dumps(transformer.template(), indent=2)+'\n')
    else:
        click.echo(json.dumps(transformer.template(), indent=2))
