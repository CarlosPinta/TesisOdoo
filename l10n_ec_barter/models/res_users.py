from odoo import models, api, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    l10n_ec_state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published')
    ])

    @api.model
    def signup(self, values, token=None):
        res = super(ResUsers, self).signup(values, token=token)
        return res

    def _create_user_from_template(self, values):
        res = super(ResUsers, self)._create_user_from_template(values)
        if res:
            res.write({
                'groups_id': [(6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('l10n_ec_barter.client_barter_group').id,
                ])]
            })
        return res
