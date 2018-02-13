<!DOCTYPE html>
<html lang="en">
<head>
    <title>Маршруты</title>
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
<div class="pull-right">
    <a class="btn" href="${request.route_url('logout')}">Выйти</a>|
    <a class="btn" href="${request.route_url('dashboard')}">Главная</a>
</div>
<style>
    body {
        margin: 0 30px;
    }
</style>
<h1>Маршруты</h1>

<a class="btn btn-default" href="${request.route_url('route_add')}">Зарегестрировать новый маршрут</a>
<br/>
<br/>
<table class="table table-bordered table-condensed table-hover table-striped">
    <colgroup>
        <col class="col-lg-2">
        <col>
        <col class="col-lg-2">
        <col class="col-lg-2">
        <col class="col-lg-1">
    </colgroup>
    <thead>
        <tr>
            <td>№ маршрута</td>
            <td>Название</td>
            <td>Расстояние</td>
            <td>Стоимость</td>
            <td>Перевозки</td>
        </tr>
    </thead>
    <tbody>
        <%
            count = 0
        %>
        % for item in entity:
            <%
                count = 1
            %>
            <tr onclick="document.location ='${request.route_url('route_view', uid=item.uid)}'">
                <td>${item.uid}</td>
                <td>${item.name}</td>
                <td>${item.distance}</td>
                <td>${item.base_price}</td>
                <td>${len(item.shippings)}</td>
            </tr>
        % endfor
        % if count == 0:
            <tr><td colspan="5">Нет записей.</td></tr>
        % endif
    </tbody>
</table>
</body>
</html>
