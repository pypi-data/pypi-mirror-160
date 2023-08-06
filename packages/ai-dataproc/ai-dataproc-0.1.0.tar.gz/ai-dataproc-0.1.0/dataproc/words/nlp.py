from dataproc.conf import Config
from dataproc.words.utils import locale
from dataproc.zio.zworker import Actor


class NLP(Actor):

    def execute(self, model, msg):
        data = msg.decode()
        return model.keywords(data)

    def init_model(self):
        from dataproc.words.ml_models import create_word_actor
        self.model = create_word_actor(Config.BASE_PATH, locale["es-AR"],
                                       with_nlp=True, nlp_rank=True)
