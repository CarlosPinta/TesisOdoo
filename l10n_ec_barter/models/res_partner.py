from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('name')
    def _compute_partner_user_id(self):
        partners = self.search([])
        for this in partners:
            if this.id == self.env.user.partner_id.id:
                this.l10n_ec_partner_user_id = self.env.user.id

    l10n_ec_partner_user_id = fields.Many2one(
        'res.users',
        compute='_compute_partner_user_id',
        store=True,
        string='Usuario Actual'
    )
    l10n_ec_state = fields.Selection([
        ('not_published', 'No Publicado'),
        ('published', 'Publicado'),
        ('discarded', 'Descartado')
    ],
        string='Estado',
        default='not_published'
    )

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        self._compute_partner_user_id()
        return res

    def action_published(self):
        return True

    def action_discard(self):
        return True

    def action_not_published(self):
        return True
