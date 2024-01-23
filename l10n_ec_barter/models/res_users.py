from odoo import models, api, fields, Command


class ResUsers(models.Model):
    _inherit = 'res.users'

    l10n_ec_state = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], string='Estado',
        default='active'
    )

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

    def l10n_ec_action_active(self):
        for this in self:
            this.l10n_ec_state = 'active'

    def l10n_ec_action_inactive(self):
        for this in self:
            this.l10n_ec_state = 'inactive'

    def approve_permission(self):
        for this in self:
            this.l10n_ec_approve_process = False
            group_adm = self.env.ref('l10n_ec_barter.admin_barter_group')
            this.write({'groups_id': [Command.link(group_adm.id)]})

    def rejected_permission(self):
        for this in self:
            this.l10n_ec_approve_process = False
            html = (
                '<div class="o_mail_notification">El usuario {name} ha rechazado la solicitud para '
                'obtener permiso de administrador</div>'.format(
                    name=this.name))
            this.partner_id.message_post(body=html)
