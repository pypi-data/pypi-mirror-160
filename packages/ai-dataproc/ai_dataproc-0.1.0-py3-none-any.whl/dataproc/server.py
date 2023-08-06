from contextvars import ContextVar

import aioredis
from db.nosync import AsyncSQL
from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend

from dataproc.conf import Config
from dataproc.crawlers.http_client import AIOFetch
# from dataproc.news.web import news_bp
# from dataproc.workflows.web import workflows_bp
# from dataproc.crawlers.web import sites_bp
from dataproc.words.utils import get_locale

app = Sanic("crawler")

# app.blueprint(news_bp)
# app.blueprint(sites_bp)
# app.blueprint(workflows_bp)

app.config.CORS_ORIGINS = "*"
Extend(app)

locale_opts = get_locale(Config.LOCALE)


db = AsyncSQL(Config.ASQL)
_base_model_session_ctx = ContextVar("session")


def _parse_page_limit(request, def_pg="1", def_lt="100"):
    strpage = request.args.get("page", [def_pg])
    strlimit = request.args.get("limit", [def_lt])
    page = int(strpage[0])
    limit = int(strlimit[0])

    return page, limit


@app.listener("before_server_start")
async def startserver(current_app, loop):
    if Config.WEB_REDIS:
        current_app.ctx.redis = \
            aioredis.from_url(Config.WEB_REDIS,
                              decode_responses=True)
    current_app.ctx.db = db
    await current_app.ctx.db.init()

    current_app.ctx.fetch = AIOFetch()


@app.listener("after_server_stop")
async def shutdown(current_app, loop):
    await current_app.ctx.db.engine.dispose()
    await current_app.ctx.redis.close()


@app.middleware("request")
async def inject_session(request):
    current_app = Sanic.get_app("crawler")
    request.ctx.fetch = current_app.ctx.fetch
    request.ctx.session = app.ctx.db.sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(
        request.ctx.session)

    request.ctx.dbconn = db.engine


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


@app.get("/status")
async def status_handler(request):
    # current_app = Sanic.get_app("MyHelloWorldApp")
    return json(dict(msg="We are ok"))
