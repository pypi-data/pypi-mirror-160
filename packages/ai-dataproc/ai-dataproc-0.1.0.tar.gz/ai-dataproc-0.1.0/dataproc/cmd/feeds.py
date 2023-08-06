import click
import requests
import toml
from dataproc.conf import Config


def _open_toml(from_file: str):
    with open(from_file, "r") as f:
        tf = f.read()

    tomconf = toml.loads(tf)
    return tomconf


@click.command()
@click.option('--from-file', "-f", default=None,
              help="toml file with the configuration")
@click.option('--web', default=Config.CRAWLER_SERVICE, help="Web server")
def feeds(from_file, web):
    """ update site """

    data = _open_toml(from_file)
    _feeds = data["feed"]
    for feed_data in _feeds:
        if feed_data["update"]:
            rsp = requests.put(f"{web}/content/feed-task",
                               json=feed_data["data"])
            created_or_updated = "updated"
        else:
            rsp = requests.post(
                f"{web}/content/feed-task", json=feed_data["data"])
            created_or_updated = "created"
        click.echo(
            f"{feed_data['data']['name']} {created_or_updated}. Status {rsp.status_code}")
