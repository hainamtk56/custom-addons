# __manifest__.py
{
    'name': 'Custom Document Management',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rule.xml',
        'views/document_views.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'document/static/src/**/*.js',
                # 'document/static/src/**/*.css',
            ],
    },
    'installable': True,
    'application': True,
}