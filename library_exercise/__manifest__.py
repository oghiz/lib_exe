# -*- coding: utf-8 -*-
{
    'name': "Library",
    'summary': """Just a basic library module exercise""",
    'description': """Long description of library module's purpose""",
    'author': "Augustinas Kunsmonas",
    'website': "http://www.google.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/book.xml',
        'views/lend.xml',
        'views/lend_expired_email.xml',
        'data/lend_expiration_cron.xml',
        'report/lend_report.xml',
    ],
}
