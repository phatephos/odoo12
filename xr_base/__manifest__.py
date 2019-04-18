# -*- coding: utf-8 -*-
{
    'name': 'xr_base',
    'summary': """
         Basic archives""",
    'description': """
        Basic archives
    """,
    'author': "lizhaoyang",
    'website': "http://www.yourcompany.com",
    'category': 'xr_base',
    'version': '0.1',
    'depends': ['base', 'mail',],
    'data': [
        'security/product_security.xml',
        'security/ir.model.access.csv',
        'views/company.xml',
        'views/account.xml',
        'views/archives.xml',
        'views/area.xml',
        'views/customer.xml',
        'views/department.xml',
        'views/personnel.xml',
        'views/product.xml',
        'views/technology.xml',
        'views/material.xml',

        'views/views.xml'

    ],
    'sequence': 12,
    'installable': True,
    'application': True,
    'auto_install': False,
}

