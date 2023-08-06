from dataproc.conf import Config
from dataproc.regions.models import Place
from dataproc.social.twitter.api import Options, TwitterApi
from sqlalchemy import select

_STMT = select(Place)


def load(conf: Config, session):
    topts = Options(
        consumer_key=conf.consumer_key,
        consumer_secret=conf.consumer_secret,
        access_token=conf.access_token,
        access_secret=conf.access_secret
    )
    tw = TwitterApi(topts)

    places = tw.trends_available()
    """{'country': 'Japan',
        'countryCode': 'JP',
        'name': 'Okayama',
        'parentid': 23424856,
        'placeType': {'code': 7, 'name': 'Town'},
        'url': 'http://where.yahooapis.com/v1/place/90036018',
        'woeid': 90036018}
    """
    for p in places:
        pdata = Place(
            woeid=p['woeid'],
            parent_id=p['parentid'],
            name=p['name'].lower(),
            country=p['country'].lower(),
            country_code=p['countryCode'],
            type_code=p['placeType']["code"],
            type_name=p['placeType']["name"],
        )
        session.add(pdata)


def list_all(session):
    result = session.execute(_STMT)
    return result


def list_countries(session, country=None):
    stmt = _STMT.filter_by(type_code=12)
    if country:
        stmt = stmt.where(Place.country==country)
    result = session.execute(stmt).scalars().all()
    return result


def get_places_by_country(session, country):
    search = f"{country}%"
    stmt = _STMT.filter(Place.country.like(search))
    result = session.execute(stmt).all()
    return result


def find_by_woeid(session, woeid):
    stmt = _STMT.filter_by(woeid=woeid)
    results = session.execute(stmt).all()
    return results


def find_by_name(name):
    pass


def find_by_code(code):
    pass
