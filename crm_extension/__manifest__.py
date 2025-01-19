# -*- coding: utf-8 -*-
{
    'name': "crm_extension",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sales_team', 'crm', 'sale_crm', 'hr', 'mail', 'sale'],

    # always loaded
    'data': [
        'security/record_rule.xml',
        'security/ir.model.access.csv',
        'data/groups.xml',
        'data/users.xml',
        'views/crm_lead_view.xml',
        'views/crm_team_view.xml',
        'views/sales_detail_report_view.xml',
        'views/sales_target_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

