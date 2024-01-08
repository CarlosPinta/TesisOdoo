# -*- coding: utf-8 -*-
{
    'name': "l10n_ec_barter",

    'summary': """
        Este módulo permite el intercambio entre productos, tomandpo en cuenta pricniaplmente
        la negociación op conversacion ya que le interecambio unicamente se realizar por otro producto,
        En este punto es importante conocer los siguientes puntos en el cual esta enfocado el sistema de Trueque""",

    'description': """
         Este módulo permite el intercambio entre productos, tomandpo en cuenta pricniaplmente
        la negociación op conversacion ya que le interecambio unicamente se realizar por otro producto,
        En este punto es importante conocer los siguientes puntos en el cual esta enfocado el sistema de Trueque
    """,

    'author': "Carlos Pinta, Kevin Argoti",
    'website': "",

    'category': 'Products',
    'version': '0.1',

    'depends': [
        'base',
        'product',
        'muk_web_theme'
    ],

    'data': [
        'views/l10n_ec_barter_views.xml',
        'views/res_partner_view.xml',
        'views/res_users_views.xml',
        'views/product_template_views.xml',
        'data/ir.module.category.csv',
        'data/res_groups_data.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
}
