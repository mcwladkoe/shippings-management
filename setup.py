from setuptools import setup

requires = [
    'pyramid',
    'pyramid_mako',
    'deform',
    'sqlalchemy',
    'pyramid_tm',
    'zope.sqlalchemy',
    'pytz',
    'bcrypt',
    'colander',
]

setup(name='transport_app',
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = transport_app:main
    [console_scripts]
    initialize_db = transport_app.initialize_db:main
    """,
)