# -*- coding: utf-8 -*-
{
    'name': "Sales Plan",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '0.1',
    'installable': True,
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'crm', 'sale', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/plan_sale_order_view.xml',
        'views/sale_order_view.xml',
        'data/groups_1.xml',
    ],
}

