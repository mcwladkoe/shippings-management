from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )

from pyramid.view import (
    view_config,
    view_defaults
    )

from ..security import (
    USERS,
    check_password
)


@view_config(route_name='dashboard', renderer='../templates/dashboard.mako', permission='edit')
def dashboard(request):
    return dict(
        request=request,
    )