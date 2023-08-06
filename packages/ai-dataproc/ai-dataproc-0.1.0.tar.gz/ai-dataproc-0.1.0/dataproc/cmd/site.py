import concurrent.futures

import click
import toml
from dataproc.conf import Config
from dataproc.crawlers.managers.site import RootSave, SiteManager
from dataproc.crawlers.parsers.url import url2docid
from dataproc.crawlers.root import CrawlRootTask, crawl_root2, register_site
from db.sync import SQL
from tabulate import tabulate

# def _same_root(root: RootSave, crt: CrawlRootTask):
#    should_update = False
#    if root.bucket.namespace != crt.ns:
#        should_update = True
#    if root.country != crt.country:
#        should_update = True
#


def wrapper_register_site(data):
    db = SQL(Config.SQL)
    Session = db.sessionmaker()
    crt = data["crt"]
    with Session() as session:
        rsp = register_site(session, crt, update_site=data["update"])

    if not rsp:
        print(f"{crt.url} Already  registered")


def _open_toml(from_file: str):
    with open(from_file, "r") as f:
        tf = f.read()

    tomconf = toml.loads(tf)
    return tomconf


def batch_process(from_file, workers, update):
    tomconf = _open_toml(from_file)

    tasks = []
    for batch in tomconf["batch_sites"]:
        for s in batch["sites"]:
            opts = dict(**batch)
            del(opts["sites"])
            opts["url"] = s
            crt = CrawlRootTask(**opts)
            print(f"Adding {crt.url}")
            data = {"crt": crt, "update": update}
            tasks.append(data)

    if workers > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(
                wrapper_register_site, t): t for t in tasks}
            for f in concurrent.futures.as_completed(futures):
                result = futures[f]
                try:
                    f.result()
                except Exception as exc:
                    print("error", result, exc)
                else:
                    print(result["crt"].url, " finished...")
    else:
        for t in tasks:
            wrapper_register_site(t)


@click.command()
@click.option('--from-file', "-f", default=None,
              help="toml file with the configuration")
@click.option('--workers', default=5, help="workers to run in parallel")
@click.option('--test-site', "-T", default=None, help="Test site")
@click.option('--delete-site', "-D", default=None, help="Delete site based on siteid")
@click.option('--update', "-u", default=False, is_flag=True, help="Update site if any change is found")
def site(from_file, workers, test_site, delete_site, update):
    """ update site """

    if from_file and not test_site:
        batch_process(from_file, workers, update)
    elif test_site and not from_file:
        crt = CrawlRootTask(url=test_site)
        rsp = crawl_root2(crt)
        print("\n--------------------------------------------")
        print("URL: ", crt.url)
        print("Lang: ", rsp.root.web.html_lang)
        print("Socials: ")
        print(tabulate({"social urls": rsp.root.social},  tablefmt="pasql"))
        print("Sources: ", list(rsp.df.source.unique()))
        print("Total urls: ", rsp.df.basename.count())

    elif delete_site:
        url = url2docid(delete_site)
        db = SQL(Config.SQL)
        Session = db.sessionmaker()
        with Session() as session:
            SiteManager.delete_root(session, siteid=url.key)
            session.commit()
        print(f"Site {delete_site}, deleted")

    else:
        print("Please provide a config file or a url for testing")
