<!DOCTYPE html>
<html lang="en">
<head>
    <title>Водитель № ${item.uid}</title>
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
    Водители
</a>

<h1>${item.last_name} ${item.first_name} ${item.patronymic}</h1>
<p><b>Email:</b> ${item.email}</p>
<p><b>Стаж:</b> ${item.experience} лет</p>

<a class="btn btn-md btn-success" href="${request.route_url('driver_edit', uid=item.uid)}">
    Редактировать
</a>
<a class="btn btn-md btn-danger" href="${request.route_url('driver_delete', uid=item.uid)}">
    Удалить
</a>


<h4>Перевозки</h4>
<table class="table table-bordered table-condensed table-hover table-striped">
    <colgroup>
        <col class="col-lg-2">
        <col>
        <col class="col-lg-2">
        <col class="col-lg-2">
        <col class="col-lg-1">
        <col class="col-lg-1">
    </colgroup>
    <thead>
        <tr>
            <td>№ перевозки</td>
            <td>Дата начала</td>
            <td>Дата завершения</td>
            <td>Маршрут</td>
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
            <tr onclick="document.location ='${request.route_url('shipping_view', uid=i.shipping.uid)}'">
                <td>${i.shipping.uid}</td>
                <td>${i.shipping.start_date}</td>
                <td>${i.shipping.end_date}</td>
                <td>${i.shipping.route.name}</td>
                <td>${i.shipping.award}</td>
                <td>${i.shipping.price}</td>
            </tr>
        % endfor
        % if count == 0:
            <tr><td colspan="6">Нет записей.</td></tr>
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