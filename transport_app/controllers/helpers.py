from pyramid.view import view_config

from ..models import DBSession, Route, Driver


@view_config(
    route_name='lookup',
    renderer='json',
    permission='edit'
)
def lookup(request):
    routes = DBSession.query(Route).all()
    route_dict = {}
    for i in routes:
        route_dict[i.uid] = i.base_price
    drivers = DBSession.query(Driver).all()
    drivers_dict = {}
    for i in drivers:
        drivers_dict[i.uid] = i.experience
    return dict(route_dict=route_dict, drivers_dict=drivers_dict)