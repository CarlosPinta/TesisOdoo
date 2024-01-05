from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    user_id = fields.Many2one(
        'res.users', string='Propietario',
        default=lambda self: self.env.user
    )
