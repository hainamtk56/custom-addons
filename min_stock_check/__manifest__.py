{
    'name': 'Minimum Stock Check',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Check minimum stock quantity based on future demands',
    'depends': ['stock', 'mrp'],
    'data': [
        'views/product_template_views.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
}
