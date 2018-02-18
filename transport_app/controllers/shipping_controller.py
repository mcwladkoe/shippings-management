# -*- coding: utf-8 -*-
import colander
import deform.widget

from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession, Shipping, Driver, DriverShipping, Route

from .base_controller import BaseController

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import logging
log = logging.getLogger(__name__)


class ShippingView(colander.MappingSchema):

    start_date = colander.SchemaNode(colander.DateTime(), title="Начало рейса:")
    end_date = colander.SchemaNode(colander.DateTime(), title="Конец рейса:")

    award = colander.SchemaNode(colander.Float(), title="Премия (грн):")

    route_id = colander.SchemaNode(colander.Integer(), title="Маршрут:",
        widget=deform.widget.SelectWidget(values=Route.options())
    )

    driver_1_id = colander.SchemaNode(colander.Integer(), title="Водитель 1:",
        widget=deform.widget.SelectWidget(values=Driver.options()))
    driver_2_id = colander.SchemaNode(colander.Integer(), title="Водитель 2:", default=0, 
        widget=deform.widget.SelectWidget(values=Driver.options(second=True)))


class Shippings(BaseController):

    entity = Shipping
    entity_name = 'shipping'

    @property
    def form(self):
        schema = ShippingView()
        return deform.Form(schema, buttons=('submit',))

    @view_config(
        route_name='shipping_list',
        renderer='../templates/shipping_list.mako',
        permission='edit'
    )
    def entity_list(self):
        return BaseController.entity_list(self)

    @view_config(
        route_name='shipping_add',
        renderer='../templates/shipping_addedit.mako',
        permission='edit'
    )
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
            route = DBSession.query(Route).filter(Route.uid == item.route_id).first()
            if not route:
                return Response('Ошибка. Такого маршрута не существует')
            if appstruct['driver_1_id'] == appstruct['driver_2_id']:
                return Response('Ошибка. Водитель выбран два раза')
            driver1 = DBSession.query(Driver).filter(
                Driver.uid == appstruct['driver_1_id']
            ).first()
            if not driver1:
                return Response('Ошибка. Такого водителя id {} не существует'\
                    .format(appstruct['driver_1_id']))
            d1 = DriverShipping(driver_id = driver1.uid, shipping = item,
                price = route.base_price * (100 + driver1.experience / 100. + item.award)
                )
            item.price = d1.price
            if appstruct['driver_2_id']:
                driver2 = DBSession.query(Driver).filter(
                    Driver.uid == appstruct['driver_2_id']
                ).first()
                if not driver2:
                    return Response(
                        'Ошибка. Такого водителя id {} не существует'\
                            .format(appstruct['driver_2_id']
                    ))
                d2 = DriverShipping(driver_id = driver2.uid, shipping = item,
                    price = route.base_price * (100 + driver2.experience / 100. + item.award))
                item.price += d2.price

            item.created = datetime.utcnow()
            item.updated = datetime.utcnow()
            try:
                DBSession.add(item)
                DBSession.flush()
                DBSession.add(d1)
                if appstruct['driver_2_id']:
                    DBSession.add(d2)
            except IntegrityError as e:
                log.exception(e)
                return Response('Ошибка. {}'.format(e))
            except SQLAlchemyError as e:
                log.exception(e)
                return Response('Ошибка СУБД')

            url = self.request.route_url('{}_list'.format(self.entity_name))
            return HTTPFound(url)
        return dict(form=form)

    @view_config(
        route_name='shipping_view',
        renderer='../templates/shipping_view.mako',
        permission='edit'
    )
    def view(self):
        return BaseController.view(self)


    @view_config(
        route_name='shipping_edit',
        renderer='../templates/shipping_addedit.mako',
        permission='edit'
    )
    def edit(self):
        # TODO:
        # change drivers for edit
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
            route = DBSession.query(Route).filter(Route.uid == item.route_id).first()
            if not route:
                return Response('Ошибка. Такого маршрута не существует')
            if appstruct['driver_1_id'] == appstruct['driver_2_id']:
                return Response('Ошибка. Водитель выбран два раза')
            drivers = DBSession.query(DriverShipping).filter(DriverShipping.id == item.uid).all()
            if appstruct['driver_1_id'] != drivers[0].driver_id:
                driver = DBSession.query(Driver).filter(
                    Driver.uid == appstruct['driver_1_id']
                ).first()
                if not driver:
                    return Response('Ошибка. Такого водителя id {} не существует' \
                                    .format(appstruct['driver_1_id']))
                drivers[0].driver_id = driver.uid
                drivers[0].price=route.base_price * (100 + driver.experience / 100.) + item.award
                DBSession.add(drivers[0])
                item.price = drivers[0].price
            if appstruct['driver_2_id']:
                driver = DBSession.query(Driver).filter(
                    Driver.uid == appstruct['driver_2_id']
                ).first()
                if not driver:
                    return Response('Ошибка. Такого водителя id {} не существует' \
                                    .format(appstruct['driver_2_id']))
                if len(drivers) == 2:
                    if appstruct['driver_2_id'] != drivers[1].driver_id:

                        drivers[1].driver_id = driver.uid
                        drivers[1].price = route.base_price * (100 + driver.experience / 100.) + item.award
                        DBSession.add(drivers[1])
                        item.price += drivers[0].price
                else:
                    d2 = DriverShipping(driver_id=driver.uid, shipping=item,
                                        price=route.base_price * (100 + driver.experience / 100. + item.award))
                    item.price += d2.price
                    DBSession.add(d2)
            elif len(drivers) == 2:
                DBSession.delete(drivers[1])
            DBSession.flush()
            item.updated = datetime.utcnow()
            try:
                DBSession.add(item)
                DBSession.flush()
            except IntegrityError as e:
                log.exception(e)
                return Response('Ошибка. {}'.format(e))
            except SQLAlchemyError as e:
                log.exception(e)
                return Response('Ошибка СУБД')
            url = self.request.route_url('{}_view'.format(self.entity_name), uid=uid)
            return HTTPFound(url)

        form = self.form.render(item.__dict__)
        return dict(item=item, form=form)


    @view_config(route_name='shipping_delete', permission='edit')
    def delete(self):
        return BaseController.delete(self)
