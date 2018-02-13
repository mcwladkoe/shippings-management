# -*- coding: utf-8 -*-
import colander
import deform.widget

import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession, Route

from .base_controller import BaseController

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import logging
log = logging.getLogger(__name__)

class RouteView(colander.MappingSchema):

    name = colander.SchemaNode(colander.String(), title="Название:",
                          validator=colander.Length(max=50))
    distance = colander.SchemaNode(colander.Float(), title="Расстояние (км):",
        validator=colander.Range(0, 10000))

    base_price = colander.SchemaNode(colander.Float(), title="Стоимость (грн):",
        validator=colander.Range(0, 1000000))


class Routes(BaseController):

    entity = Route
    entity_name = 'route'

    @property
    def form(self):
        schema = RouteView()
        return deform.Form(schema, buttons=('submit',))

    @view_config(
        route_name='route_list',
        renderer='../templates/route_list.mako',
        permission='edit'
    )
    def entity_list(self):
        return BaseController.entity_list(self)

    @view_config(
        route_name='route_add',
        renderer='../templates/route_addedit.mako',
        permission='edit'
    )
    def add(self):
        return BaseController.add(self)

    @view_config(
        route_name='route_view',
        renderer='../templates/route_view.mako',
        permission='edit'
    )
    def view(self):
        return BaseController.view(self)

    @view_config(
        route_name='route_edit',
        renderer='../templates/route_addedit.mako',
        permission='edit'
    )
    def edit(self):
        return BaseController.edit(self)


    @view_config(route_name='route_delete', permission='edit')
    def delete(self):
        return BaseController.delete(self)
