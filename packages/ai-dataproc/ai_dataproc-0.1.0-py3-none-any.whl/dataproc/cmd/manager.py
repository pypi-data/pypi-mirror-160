import click
from dataproc.conf import Config
from dataproc.content.models import (ContentBucketModel, FeedInstanceModel,
                                     FeedSpecModel)
from dataproc.crawlers.models import (CrawlerBucketModel, DataPagesTaskModel,
                                      DataRoots2TaskModel, DataRootsTaskModel,
                                      PageModel, SiteLabelModel, SiteModel,
                                      URLModel)
from dataproc.datasets.models import (DatasetModel, TableModel, TagModel,
                                      datasets_tags)
from dataproc.regions.models import Place
from dataproc.social.models import (GoogleTrendTask, TweetTrendModel,
                                    TweetTrendTask)
from dataproc.workflows.models import HistoryModel, ScheduleModel
from db.sync import SQL


@click.command()
@click.option('--sql', "-s",
              default=Config.SQL,
              help="SQL Database")
@click.argument('action', type=click.Choice([
    'createdb', 'dropdb']))
def manager(sql, action):
    """ Create or Drop all the tables in database
    """
    db = SQL(sql)
    if action == "createdb":
        db.create_all()
        click.echo("Created...")
    elif action == "dropdb":
        db.drop_all()
        click.echo("Droped...")
    else:
        click.echo("Wrong param...")
