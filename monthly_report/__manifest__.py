# -*- coding: utf-8 -*-
{
    'name': "monthly_report",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_crm', 'hr', 'purchase', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/mail_tmpl.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}
