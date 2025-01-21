# -*- coding: utf-8 -*-
{
    'name': "crm_extension",
    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'sales_team', 'crm', 'sale_crm', 'hr', 'mail', 'sale'],

    'data': [
        'data/groups.xml',
        'data/users.xml',
        'security/ir.model.access.csv',
        'security/record_rule.xml',
        'views/crm_team_view.xml',
        'views/crm_lead_view.xml',
        'views/sales_detail_report_view.xml',
        'views/sales_target_report_view.xml',
    ],
}
