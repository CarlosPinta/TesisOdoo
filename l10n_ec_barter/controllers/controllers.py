# -*- coding: utf-8 -*-
# from odoo import http


# class L10nEcBarter(http.Controller):
#     @http.route('/l10n_ec_barter/l10n_ec_barter', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_ec_barter/l10n_ec_barter/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_ec_barter.listing', {
#             'root': '/l10n_ec_barter/l10n_ec_barter',
#             'objects': http.request.env['l10n_ec_barter.l10n_ec_barter'].search([]),
#         })

#     @http.route('/l10n_ec_barter/l10n_ec_barter/objects/<model("l10n_ec_barter.l10n_ec_barter"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_ec_barter.object', {
#             'object': obj
#         })
