from odoo import models, api, fields, Command
from odoo.exceptions import ValidationError
import math


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.depends('l10n_ec_rating_line_ids')
    def _compute_rating_total(self):
        for this in self:
            ratings = this.l10n_ec_rating_line_ids
            if ratings:
                rate_list = [int(value) for value in ratings.mapped('rating')]
                this.l10n_ec_rating_total = str(math.ceil(sum(rate_list) / len(ratings)))

    l10n_ec_state = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], string='Estado',
        default='active'
    )
    l10n_ec_rating_line_ids = fields.One2many(
        'res.user.barter.rating',
        'user_id',
        string='Valoraciones'
    )
    l10n_ec_rating_total = fields.Selection([
        ('0', 'Muy Malo'),
        ('1', 'Malo'),
        ('2', 'Regular'),
        ('3', 'Bueno'),
        ('4', 'Excelente'),
    ], string='Valoración',
        compute='_compute_rating_total',
        store=True
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
            group_inactive = self.env.ref('l10n_ec_barter.no_access_barter_group')
            group_client = self.env.ref('l10n_ec_barter.client_barter_group')
            this.write({'groups_id': [(3, group_inactive.id)]})
            this.write({'groups_id': [(4, group_client.id)]})

    def l10n_ec_action_inactive(self):
        for this in self:
            this.l10n_ec_state = 'inactive'
            group_inactive = self.env.ref('l10n_ec_barter.no_access_barter_group')
            group_client = self.env.ref('l10n_ec_barter.client_barter_group')
            group_admin = self.env.ref('l10n_ec_barter.admin_barter_group')
            this.write({'groups_id': [(4, group_inactive.id)]})
            this.write({'groups_id': [(3, group_client.id)]})
            this.write({'groups_id': [(3, group_admin.id)]})

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


class ResUserBarterRating(models.Model):
    _name = 'res.user.barter.rating'

    user_id = fields.Many2one(
        'res.users',
        string='Usuario'
    )
    rating_user_id = fields.Many2one(
        'res.users',
        string='Valorador'
    )
    rating = fields.Selection([
        ('0', 'Muy Malo'),
        ('1', 'Malo'),
        ('2', 'Regular'),
        ('3', 'Bueno'),
        ('4', 'Excelente'),
    ], string='Valoración'
    )
    comment = fields.Text(
        string='Comentario'
    )
