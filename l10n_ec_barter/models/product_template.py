from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_ec_user_id = fields.Many2one(
        'res.users',
        string='Propietario',
        default=lambda self: self.env.user
    )
    l10n_ec_state = fields.Selection([
        ('not_published', 'No Publicado'),
        ('published', 'Publicado'),
        ('exchange', 'Intercambiado'),
        ('discarded', 'Descartado')
    ],
        string='Estado',
        default='not_published'
    )

    def action_published(self):
        for this in self:
            this.l10n_ec_state = 'published'

    def action_discarded(self):
        for this in self:
            this.l10n_ec_state = 'discarded'

    def action_not_published(self):
        for this in self:
            this.l10n_ec_state = 'not_published'
