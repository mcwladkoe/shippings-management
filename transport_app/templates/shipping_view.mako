<!DOCTYPE html>
<html lang="en">
<head>
    <title>Перевозка № ${item.uid}</title>
    <link rel="stylesheet"
          href="${request.static_url('deform:static/css/bootstrap.min.css')}"
          type="text/css" media="screen" charset="utf-8"/>
    <link rel="stylesheet"
          href="${request.static_url('deform:static/css/form.css')}"
          type="text/css"/>
    % for reqt in view.reqts['css']:
        <link rel="stylesheet" type="text/css"
              href="${request.static_url(reqt)}"/>
    % endfor
    <script src="${request.static_url('deform:static/scripts/jquery-2.0.3.min.js')}"
            type="text/javascript"></script>
    <script src="${request.static_url('deform:static/scripts/bootstrap.min.js')}"
            type="text/javascript"></script>

    % for reqt in view.reqts['js']:
        <script src="${request.static_url(reqt)}"
                type="text/javascript"></script>
    % endfor
</head>
<body>
<style>
    body {
        margin-left: 30px
    }
</style>
<a class="btn" href="${request.route_url('dashboard')}">
    Главная
</a>
|
<a class="btn" href="${request.route_url('driver_list')}">
    Перевозки
</a>
<h1>Перевозка № ${item.uid}</h1>
<p><b>Начало поездки:</b> ${item.start_date}</p>
<p><b>Конец поездки:</b> ${item.end_date}</p>
<p><b>Маршрут:</b> <a href="${request.route_path('route_view', uid=item.route.uid)}">${item.route.name} (${item.route.distance} км)</a></p>
<p><b>Премия:</b> ${item.award} грн.</p>
<p><b>Водители:</b>
    <ul>
        % for i in item.drivers:
            <li>
                <a href="${request.route_path('driver_view', uid=i.driver.uid)}">${i.driver.full_name}</a>
            </li>
        % endfor
    </ul>
</p>
<p><b>Стоимость:</b> ${item.price} грн.</p>

##<h1>${item.last_name} ${item.first_name} ${item.patronymic}</h1>
##<p><b>Email:</b> ${item.email}</p>
##<p><b>Стаж:</b> ${item.experience}</p>

<a class="btn btn-md btn-success" href="${request.route_url('shipping_edit', uid=item.uid)}">
    Редактировать
</a>
<a class="btn btn-md btn-danger" href="${request.route_url('shipping_delete', uid=item.uid)}">
    Удалить
</a>

##<a class="btn btn-default" href="${request.route_url('customer_order_add', customer_id=customer.uid)}">
##    Новый заказ
##</a>
##<a class="btn btn-default" href="${request.route_url('customer_order_list', customer_id=customer.uid)}">
##    Список заказов
##</a>

</body>
</html>