
# import os
import subprocess

import click


@click.command()
@click.option("--store", "-s", default="/tmp/plasma", help="Path where plasma will be intialized")
@click.option("--mem-size", "-m", default="1", help="Size of the store in GB")
def plasma(store, mem_size):
    """
    plasma_store  -m 1000000000 -s /tmp/plasma
    """
    bytes_ = 1000000000
    mem = str(bytes_ * int(mem_size))
    subprocess.run(["plasma_store", "-s", store, "-m", mem], check=True)
