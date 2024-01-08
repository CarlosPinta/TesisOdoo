from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_ec_user_id = fields.Many2one(
        'res.users', string='Propietario',
        default=lambda self: self.env.user
    )
    l10n_ec_state = fields.Selection([
        ('not_published', 'No Publicado'),
        ('published', 'Publicado'),
        ('discarded', 'Descartado')
    ],
        string='Estado',
        default='not_published'
    )
