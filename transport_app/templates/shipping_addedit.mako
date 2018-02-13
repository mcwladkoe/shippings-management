<!DOCTYPE html>
<html lang="en">
<head>
    <title>
        % if request.matched_route.name == 'shipping_add':
            Регистрация
        % else:
            Редактирование
        % endif
        перевозки
    </title>
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
    <a class="btn" href="${request.route_url('dashboard')}">
        Главная
    </a>
    |
    <a class="btn" href="${request.route_url('shipping_list')}">
        Перевозки
    </a>
    % if request.matched_route.name != 'shipping_add':
         |
        <a class="btn" href="${request.route_url('shipping_view', uid=item.uid)}">
            Просмотр
        </a>
    % endif
    <h1 style="margin-left: 40px">
        % if request.matched_route.name == 'shipping_add':
            Регистрация
        % else:
            Редактирование
        % endif
        <span>перевозки</span>
    </h1>
    <style>
        .form-control {
            width: 400px !important
        }
        
        body {
            margin-left: 30px
        }
    </style>
    <p>${form | n}</p>
    <script type="text/javascript">
        deform.load()
    </script>
</body>
</html>