from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession, Base
from .security import groupfinder

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='.resources.Root')
    config.include('pyramid_mako')
    
        # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['transport_app.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    config.add_route('dashboard', '/dashboard')
    config.add_route('driver_list', '/driver/list')
    config.add_route('driver_add', '/driver/add')
    config.add_route('driver_view', '/driver/{uid}')
    config.add_route('driver_edit', '/driver/{uid}/edit')
    config.add_route('driver_delete', '/driver/{uid}/delete')
    #config.add_route('dashboard', '/')
    config.add_route('route_list', '/route/list')
    config.add_route('route_add', '/route/add')
    config.add_route('route_view', '/route/{uid}')
    config.add_route('route_edit', '/route/{uid}/edit')
    config.add_route('route_delete', '/route/{uid}/delete')

    config.add_route('shipping_list', '/shipping/list')
    config.add_route('shipping_add', '/shipping/add')
    config.add_route('shipping_view', '/shipping/{uid}')
    config.add_route('shipping_edit', '/shipping/{uid}/edit')
    config.add_route('shipping_delete', '/shipping/{uid}/delete')

    config.add_route('login', '/')
    #config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_static_view('deform_static', 'deform:static/')
    config.scan('.controllers')
    return config.make_wsgi_app()