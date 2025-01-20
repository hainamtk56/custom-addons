# -*- coding: utf-8 -*-
{
    'name': "Sales Plan",

    'summary': "Business Plan",

    'category': 'Sales/Sales',
    'version': '0.1',
    'installable': True,
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'crm', 'sale', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/groups.xml',
        'data/users.xml',
        'views/sale_order_view.xml',
        'views/plan_sale_order_view.xml',
    ],
}
