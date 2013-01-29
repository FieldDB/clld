from json import dumps

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPNotAcceptable

from clld.interfaces import IRepresentation, IIndex
from clld.db.meta import DBSession
from clld import RESOURCES
from clld.web.adapters import get_adapter


def view(interface, ctx, req):
    """renders a resource as pyramid response using the most appropriate adapter
    for the accept header sent.
    """
    adapter = get_adapter(interface, ctx, req, ext=req.matchdict.get('ext'))
    if not adapter:
        raise HTTPNotAcceptable()
    return adapter.render_to_response(ctx, req)


def index_view(ctx, req):
    if req.is_xhr and 'sEcho' in req.params:
        return datatable_xhr_view(ctx, req)
    return view(IIndex, ctx, req)


def resource_view(ctx, req):
    return view(IRepresentation, ctx, req)


def datatable_xhr_view(ctx, req):
    if hasattr(ctx, 'row_class'):
        data = []
        for item in ctx.get_query():
            _d = {'DT_RowId': 'row_%s' % item.pk}
            row_class = ctx.row_class(item)
            if row_class:
                _d['DT_RowClass'] = row_class
            for i, col in enumerate(ctx.cols):
                _d[str(i)] = col.format(item)
            data.append(_d)
    else:
        data = [[col.format(item) for col in ctx.cols] for item in ctx.get_query()]

    # sEcho parameter.
    # Note that it strongly recommended for security reasons that you 'cast' this
    # parameter to an integer in order to prevent Cross Site Scripting (XSS) attacks.
    try:
        echo = int(req.params['sEcho'])
    except ValueError:
        echo = 1

    res = {
        "aaData": data,
        "sEcho": str(echo),
        "iTotalRecords": ctx.count_all,
        "iTotalDisplayRecords": ctx.count_filtered,
    }
    return Response(dumps(res), content_type='application/json')


def _raise(req):
    raise ValueError('test')


def _ping(req):
    return {'status': 'ok'}


def robots(req):
    return Response("Sitemap: %s\n" % req.route_url('sitemapindex'), content_type="text/plain")


def sitemapindex(req):
    return {'sitemaps': [req.route_url(r.name + 's_alt', ext='sitemap.xml') for r in RESOURCES]}
