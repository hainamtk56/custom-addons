{
    'name': "purchase_extension",
    'summary': "purchase_extension",
    'category': 'Inventory/Purchase',
    'version': '0.1',
    'intallable': True,
    'application': True,
    'depends': ['base', 'hr', 'purchase', 'mail'],
    'data': [
        'data/groups.xml',
        'data/users.xml',
        'security/ir.model.access.csv',
        'data/departments.xml',
        'views/hr_department_views.xml',
        'views/purchase_order_views.xml',
        'views/budget_limit_config_views.xml',
        'views/budget_limit_views.xml',
        'views/po_report_views.xml',
    ],
}
