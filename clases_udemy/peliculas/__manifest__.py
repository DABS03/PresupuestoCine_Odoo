# -*- coding:utf-8 -*-

{
    'name': 'Peliculas',
    'version': '1.0',
    'depends': [
        'contacts'
        ], # modulo base de Odoo
    'author': 'Diego Burgos',
    'category': 'Peliculas',
    'website': 'https://google.com',
    'description': '''
    MODULO PARA HACER PRESUPUESTOS DE PELICULAS
    ''',
    'data': [
        'views/presupuesto_views.xml',
        'views/menu.xml',
        'data/categoria.xml',
        'data/secuencia.xml'
    ],
}


 #   C:\Users\dabur\Desktop\odoo14\.venv\Scripts\python.exe C:\Users\dabur\Desktop\odoo14\odoo\odoo-bin -c C:\Users\dabur\Desktop\odoo14\o14_com.conf "--db-filter=^o14-com-*" --http-port 8071 -d o14-com-prueba -u peliculas