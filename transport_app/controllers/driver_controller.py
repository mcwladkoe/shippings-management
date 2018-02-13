# -*- coding: utf-8 -*-
import colander
import deform.widget

from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession, Driver

from .base_controller import BaseController

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import logging
log = logging.getLogger(__name__)


class DriverView(colander.MappingSchema):

    email = colander.SchemaNode(colander.String(), title="Email:",
                          validator=colander.Length(max=50))
    last_name = colander.SchemaNode(colander.String(), title="Фамилия:",
                          validator=colander.Length(max=50))
    first_name = colander.SchemaNode(colander.String(), title="Имя:",
                          validator=colander.Length(max=50))
    patronymic = colander.SchemaNode(colander.String(), title="Отчество:",
                          validator=colander.Length(max=50))
    experience = colander.SchemaNode(colander.Float(), title="Опыт (лет):",
        validator=colander.Range(0, 100))


class Drivers(BaseController):

    entity = Driver
    entity_name = 'driver'

    @property
    def form(self):
        schema = DriverView()
        return deform.Form(schema, buttons=('submit',))

    @view_config(
        route_name='driver_list',
        renderer='../templates/driver_list.mako',
        permission='edit'
    )
    def entity_list(self):
        return BaseController.entity_list(self)

    @view_config(
        route_name='driver_add',
        renderer='../templates/driver_addedit.mako',
        permission='edit'
    )
    def add(self):
        return BaseController.add(self)

    @view_config(
        route_name='driver_view',
        renderer='../templates/driver_view.mako',
        permission='edit'
    )
    def view(self):
        return BaseController.view(self)


    @view_config(
        route_name='driver_edit',
        renderer='../templates/driver_addedit.mako',
        permission='edit'
    )
    def edit(self):
        return BaseController.edit(self)


    @view_config(route_name='driver_delete', permission='edit')
    def delete(self):
        return BaseController.delete(self)
