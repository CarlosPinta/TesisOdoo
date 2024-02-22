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
        'muk_web_theme',
        'web_unsplash'
    ],

    'data': [
        'data/ir.module.category.csv',
        'data/res_groups_data.xml',
        'data/mail_templates_data.xml',
        'views/l10n_ec_barter_views.xml',
        'views/res_partner_view.xml',
        'views/res_users_views.xml',
        'views/product_template_views.xml',
        'views/external_menu_page.xml',
        'wizard/l10n_ec_barter_wizard.xml',
        'wizard/l10n_ec_barter_rating_wizard.xml',
        'security/ir.model.access.csv',
    ],
}
