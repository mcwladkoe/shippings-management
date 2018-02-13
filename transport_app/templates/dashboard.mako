<!DOCTYPE html>
<html lang="en">
<head>
    <title>Управление перевозками</title>
    <link rel="stylesheet"
          href="${request.static_url('deform:static/css/bootstrap.min.css')}"
          type="text/css" media="screen" charset="utf-8"/>
    <link rel="stylesheet"
          href="${request.static_url('deform:static/css/form.css')}"
          type="text/css"/>
    <script src="${request.static_url('deform:static/scripts/jquery-2.0.3.min.js')}"
            type="text/javascript"></script>
    <script src="${request.static_url('deform:static/scripts/bootstrap.min.js')}"
            type="text/javascript"></script>

</head>
<body>
    <div align="center">
        <h1>Управление перевозками</h1>
        <a
            class="btn btn-md btn-success"
            href="${request.route_path('driver_list')}"
        >
            Водители
        </a>
        <a
            class="btn btn-md btn-success"
            href="${request.route_path('route_list')}"
        >
            Маршруты
        </a>
        <a
            class="btn btn-md btn-success"
            href="${request.route_path('shipping_list')}"
        >
            Перевозки
        </a>
    </div>
</body>
</html>