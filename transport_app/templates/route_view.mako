<!DOCTYPE html>
<html lang="en">
<head>
    <title>Маршрут № ${item.uid}</title>
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
<a class="btn" href="${request.route_url('route_list')}">
    Маршруты
</a>
<p><b>Название:</b> ${item.name}</p>
<p><b>Расстояние:</b> ${item.distance} км</p>
<p><b>Стоимость:</b> ${item.base_price} грн</p>

<a class="btn btn-md btn-success" href="${request.route_url('route_edit', uid=item.uid)}">
    Редактировать
</a>
<a class="btn btn-md btn-danger" href="${request.route_url('route_delete', uid=item.uid)}">
    Удалить
</a>

<h4>Перевозки</h4>
<table class="table table-bordered table-condensed table-hover table-striped">
    <colgroup>
        <col class="col-lg-2">
        <col>
        <col class="col-lg-2">
        <col class="col-lg-1">
        <col class="col-lg-1">
    </colgroup>
    <thead>
        <tr>
            <td>№ перевозки</td>
            <td>Дата начала</td>
            <td>Дата завершения</td>
            <td>Премия</td>
            <td>Цена</td>
        </tr>
    </thead>
    <tbody>
        <%
            count = 0
        %>
        % for i in item.shippings:
            <%
                count = 1
            %>
            <tr onclick="document.location ='${request.route_url('shipping_view', uid=i.uid)}'">
                <td>${i.uid}</td>
                <td>${i.start_date}</td>
                <td>${i.end_date}</td>
                <td>${i.award}</td>
                <td>${i.price}</td>
            </tr>
        % endfor
        % if count == 0:
            <tr><td colspan="5">Нет записей.</td></tr>
        % endif
    </tbody>
</table>

##<a class="btn btn-default" href="${request.route_url('customer_order_add', customer_id=customer.uid)}">
##    Новый заказ
##</a>
##<a class="btn btn-default" href="${request.route_url('customer_order_list', customer_id=customer.uid)}">
##    Список заказов
##</a>

</body>
</html>