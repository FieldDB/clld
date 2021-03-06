from sqlalchemy.orm import joinedload

from clld.db.models.common import Unit, Language
from clld.web.datatables.base import DataTable, LinkCol


class DescriptionLinkCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.description}


class Units(DataTable):
    __constraints__ = [Language]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(Unit.language))

        if self.language:
            return query.filter(Unit.language == self.language)
        return query

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            DescriptionLinkCol(self, 'description'),
            LinkCol(
                self, 'language', model_col=Language.name, get_obj=lambda i: i.language),
        ]
