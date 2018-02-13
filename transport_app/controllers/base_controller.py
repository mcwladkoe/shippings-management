# -*- coding: utf-8 -*-
import colander
import deform.widget

from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import logging
log = logging.getLogger(__name__)


class BaseController(object):
    
    entity = ''
    entity_name = ''

    def __init__(self, request):
        self.request = request

    @property
    def form(self):
        raise NotImplementedError('form property not implemented')

    @property
    def reqts(self):
        return self.form.get_widget_resources()

    def entity_list(self):
        items = DBSession.query(self.entity).order_by(self.entity.created)
        return dict(title='{} View'.format(self.entity_name.capitalize()), entity=items)


    def add(self):
        form = self.form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())

            # Add a new entity to the database
            item = self.entity()
            for field, value in appstruct.iteritems():
                if hasattr(item, field):
                    setattr(item, field, value)
            item.created = datetime.utcnow()
            item.updated = datetime.utcnow()
            try:
                DBSession.add(item)
                DBSession.flush()
            except IntegrityError as e:
                log.exception(e)
                return Response('Ошибка. {} с таким email уже существует'.format(self.entity_name.capitalize()))
            except SQLAlchemyError as e:
                log.exception(e)
                return Response('Ошибка СУБД')

            url = self.request.route_url('{}_list'.format(self.entity_name))
            return HTTPFound(url)

        return dict(form=form)

    def view(self):
        uid = int(self.request.matchdict['uid'])
        item = DBSession.query(self.entity).filter_by(uid=uid).first()
        if not item:
            return HTTPFound(self.request.route_url('{}_list'.format(self.entity_name)))
        return dict(item=item)


    def edit(self):
        uid = int(self.request.matchdict['uid'])
        item = DBSession.query(self.entity).filter_by(uid=uid).first()
        if not item:
            return HTTPFound(self.request.route_url('{}_list'.format(self.entity_name)))
        form = self.form

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(item=item, form=e.render())

            # Change the content and redirect to the view
            for field, value in appstruct.iteritems():
                if hasattr(item, field):
                    setattr(item, field, value)
            item.updated = datetime.utcnow()
            try:
                DBSession.add(item)
                DBSession.flush()
            except IntegrityError as e:
                log.exception(e)
                return Response('Ошибка. {} с таким email уже существует'.format(self.entity_name.capitalize()))

            url = self.request.route_url('{}_view'.format(self.entity_name), uid=uid)
            return HTTPFound(url)
        form = self.form.render(item.__dict__)

        return dict(item=item, form=form)


    def delete(self):
        uid = int(self.request.matchdict['uid'])
        item = DBSession.query(self.entity).filter_by(uid=uid).first()
        if not item:
            return HTTPFound(self.request.route_url('{}_list'.format(self.entity_name)))
        try:
            DBSession.delete(item)
        except SQLAlchemyError:
            return HTTPFound(self.request.route_url('{}_view'.format(self.entity_name), uid=uid))
        return HTTPFound(self.request.route_url('{}_list'.format(self.entity_name)))
