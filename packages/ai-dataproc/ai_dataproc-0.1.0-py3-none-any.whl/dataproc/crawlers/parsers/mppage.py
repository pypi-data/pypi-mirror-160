import json
import multiprocessing as mp
from typing import List

from dataproc.clients import plasma_lib
from dataproc.conf import Config
from dataproc.crawlers.parsers.page import (Page, get_description, get_ld,
                                            text_to_predict2)
from dataproc.crawlers.parsers.url import URL
from dataproc.utils import mem
from dataproc.words.ml_models import WordActor, create_word_actor
from dataproc.zio.workers import LocalActorModel
from langdetect import detect as lang_detect


def choose_title(title: str, heads: List[str], words: WordActor, barrier=0.92):
    try:
        h1 = heads[0]
        confidence = words.similarity(title, h1)
        # confidence = self.wv.similarity(title, h1)
        if confidence >= barrier:
            title = h1
    except IndexError:
        pass

    return title


def page_ml3(words: WordActor,
             page: Page):
    """ Augment page with machine learning """

    title = choose_title(page.web.title, page.web.content.h1, words=words)
    article = page.article_data()

    txt_predict = text_to_predict2(page)
    desc, _ = get_description(page)
    _lang = lang_detect(txt_predict)

    if txt_predict:
        main_entities = [keys[0] for keys in words.keywords(txt_predict, 5)]
        # if locale_opts.get("section_model"):
        #    _section = news_actor.section_rank(txt_predict)[0]
        #    section = _section[0]
        #    section_proba = _section[1]
    elif article.text:
        main_entities = [keys[0] for keys in words.keywords(article.text, 5)]
    else:
        main_entities = None

    try:
        content_date = page.get_date(article).isoformat()
    except:
        content_date = None

    return dict(
        # fullurl=url.fullurl,
        lang=_lang,
        html_lang=page.web.html_lang,
        # url=url.url,
        entities=main_entities,
        section=None,
        section_proba=None,
        text=txt_predict,
        title=title,
        desc=desc,
        article_data=article.text,
        authors=get_ld(page, "author"),
        img=page.web.find_og_property("image"),
        content_date=content_date,
        keywords=get_ld(page, "keywords")
    )


class PageActor(LocalActorModel):

    def init_model(self, *args, **kwargs):
        print("ARGS: ", args)
        print("ARGS 0: ", args[0])
        print("type: ", type(args[0]))
        self.model = create_word_actor(
            Config.BASE_PATH, args[0], with_nlp=True, nlp_rank=True)

    def execute(self, model, msg):
        # data = json.loads(msg)
        id_ = msg.decode()
        client = plasma_lib.init()

        table = client.get(id_)
        dft = table.to_pandas()
        for x in dft.index:
            p = self.apply_ml(model, dft.iloc[x].to_dict())
            if p:
                return p
            else:
                print("Failed: ", dft.iloc[x].fullurl)

        client.close()

        mem()

    @staticmethod
    def apply_ml(words_actor, data):
        docid = data["docid"]
        fu = data["fullurl"]
        try:
            page = Page.from_html_txt(fu, data["html"])
            url = URL.from_str(fu)

            rsp = page_ml3(words_actor, page)
            rsp["docid"] = docid
            rsp["fullurl"] = fu
            rsp["url"] = url.url

            return rsp
        except:
            return None
