{
    'name': "purchase_extension",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Purchase',
    'version': '0.1',
    'intallable': True,
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'purchase', 'mail'],

    # always loaded
    'data': [
        'data/groups.xml',
        'data/users.xml',
        'data/departments.xml',
        'security/ir.model.access.csv',
        'views/hr_department_views.xml',
        'views/purchase_order_views.xml',
        'views/budget_limit_config_views.xml',
        'views/budget_limit_views.xml',
        'views/po_report_views.xml',
    ],
}
