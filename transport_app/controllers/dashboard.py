
from pyramid.view import view_config


@view_config(route_name='dashboard', renderer='../templates/dashboard.mako', permission='edit')
def dashboard(request):
    return dict(
        request=request,
    )