from odoo import models, api, fields
from odoo.exceptions import ValidationError, UserError


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
    l10n_ec_approve_process = fields.Boolean(
        string="En proceso de aprobación",
        default=False
    )

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        self._compute_partner_user_id()
        return res

    def request_permission(self):
        users = self.env['res.users'].sudo().search([])
        for this in self:
            if not this.l10n_ec_partner_user_id.id == self.env.user.id:
                raise ValidationError("Usted no puede pedir autorización para aumentar permisos de usuario")
            if self.env.user.has_group('l10n_ec_barter.admin_barter_group'):
                raise UserError("Usted ya tiene el permiso de Administrador")
            user_admin = users.filtered(lambda sh: sh.has_group('l10n_ec_barter.admin_barter_group'))
            this.l10n_ec_approve_process = True
            html = (
                '<div class="o_mail_notification">El usuario : {name} requiere acceso de administrador, si es correcto'
                'acceda al menu de Usuarios y apruebe las solicitud caso contrario rechace la solicitud</div>'.format(
                    name=this.name))
            for user in user_admin:
                user.partner_id.message_post(body=html)

