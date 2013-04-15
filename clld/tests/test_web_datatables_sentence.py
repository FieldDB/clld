from clld.tests.util import TestWithEnv
from clld.db.models import common


class Tests(TestWithEnv):
    def test_Units(self):
        from clld.web.datatables.sentence import Sentences

        self.handle_dt(Sentences, common.Sentence)
