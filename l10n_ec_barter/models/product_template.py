from odoo import models, api, fields
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_ec_user_id = fields.Many2one(
        'res.users',
        string='Propietario',
        default=lambda self: self.env.user
    )
    offered_user_id = fields.Many2one(
        'res.users',
        string='Usuario con el que Intercambio',
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
    l10n_ec_barter_line_ids = fields.One2many(
        "l10n_ec.product.template.barter",
        "main_product_id",
        string='Ofertas'
    )
    l10n_ec_description = fields.Text(
        string='Descripción del Producto',
        required=True
    )
    l10n_ec_message = fields.Text(
        string="Mensaje de Finalización de Intercambio"
    )
    l10n_ec_qualify_main = fields.Boolean(
        string="Calificación Propietario"
    )
    l10n_ec_qualify_offer = fields.Boolean(
        string="Calificación Ofertante"
    )

    def action_published(self):
        for this in self:
            if not this.l10n_ec_user_id.id == self.env.user.id:
                raise ValidationError("Solo el propietario del producto puede realizar esta acción")
            this.l10n_ec_state = 'published'

    def action_discarded(self):
        for this in self:
            if not this.l10n_ec_user_id.id == self.env.user.id:
                raise ValidationError("Solo el propietario del producto puede realizar esta acción")
            if this.l10n_ec_barter_line_ids.filtered(lambda barter: barter.state == 'accept'):
                raise ValidationError("Error: No puede descartar el producto porque ya se intercambio")
            this.l10n_ec_state = 'discarded'

    def action_not_published(self):
        for this in self:
            if not this.l10n_ec_user_id.id == self.env.user.id:
                raise ValidationError("Solo el propietario del producto puede realizar esta acción")
            if this.l10n_ec_barter_line_ids.filtered(lambda barter: barter.state == 'accept'):
                raise ValidationError("Error: No puede descartar el producto porque ya se intercambio")
            this.l10n_ec_state = 'not_published'

    def action_propose_barter(self):
        view_id = self.env.ref('l10n_ec_barter.l10n_ec_barter_wizard_form').id
        if self.env.user.id == self.l10n_ec_user_id.id:
            raise ValidationError("Error: No se puede ofertar en un producto propio")
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'l10n_ec.barter.wizard',
            'view_mode': 'form',
            'name': 'Ofertar',
            'view_id': view_id,
            'target': 'new',
            "context": {'default_main_product_id': self.id}
        }

    def qualify_action(self):
        view_id = self.env.ref('l10n_ec_barter.l10n_ec_barter_rating_wizard_form').id
        accept_offer = self.l10n_ec_barter_line_ids.filtered(lambda l: l.state == 'accept')
        if accept_offer:
            context = {
                'default_barter_template_id': accept_offer.id
            }
            if accept_offer.main_user_id.id == self.env.user.id:
                if self.l10n_ec_qualify_main:
                    raise ValidationError("Usted ya califico al usuario ofertante")
                context.update({
                    'default_user_id': accept_offer.offered_user_id.id,
                })
            if accept_offer.offered_user_id.id == self.env.user.id:
                if self.l10n_ec_qualify_offer:
                    raise ValidationError("Usted ya califico al usuario propietario")
                context.update({
                    'default_user_id': accept_offer.main_user_id.id,
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'l10n_ec.barter.rating.wizard',
                'view_mode': 'form',
                'name': 'Calificar',
                'view_id': view_id,
                'target': 'new',
                "context": context
            }


class L10nEcProductTemplateBarter(models.Model):
    _name = 'l10n_ec.product.template.barter'

    main_product_id = fields.Many2one(
        'product.template',
        string="Producto Padre"
    )
    product_offered_id = fields.Many2one(
        'product.template',
        string="Producto Ofrecido",
    )
    type = fields.Selection([
        ('product', 'Por Producto'),
        ('price', 'Por Valor')
    ], string="Tipo de Propuesta",
        required=True
    )
    price = fields.Float(
        string="Precio"
    )
    main_user_id = fields.Many2one(
        related='main_product_id.l10n_ec_user_id',
        string="Usuario Producto Principal",
        store=True
    )
    offered_user_id = fields.Many2one(
        'res.users',
        string="Usuario Producto Ofertado",
    )
    date = fields.Date(
        string="Fecha",
        default=lambda self: fields.Date.today()
    )
    message = fields.Char(
        string="Mensaje"
    )
    state = fields.Selection([
        ('pending', 'Pendiente'),
        ('accept', 'Aceptado'),
        ('rejected', 'Rechazado'),
        ('cancel', 'Descartado'),
    ], string="Estado",
        default="pending"
    )

    def accept_barter(self):
        for this in self:
            if not this.main_user_id.id == self.env.user.id:
                raise ValidationError("Solo el propietario del producto puede realizar esta acción")
            this.state = 'accept'
            email_template = self.env.ref('l10n_ec_barter.mail_template_product_barter_accept')
            email_values = email_template.generate_email(this.id, ['subject', 'body_html',
                                                                   'email_from', 'email_to',
                                                                   'auto_delete'])
            email_values['model'] = 'l10n_ec.product.template.barter'
            email_values['res_id'] = this.id
            email_values['email_to'] = this.offered_user_id.email
            send_email = self.env['mail.mail'].sudo().create(email_values)
            send_email.send()
            this.main_product_id.l10n_ec_state = 'exchange'
            this.main_product_id.offered_user_id = this.offered_user_id.id
            if this.product_offered_id:
                this.product_offered_id.l10n_ec_state = 'exchange'
                this.product_offered_id.offered_user_id = this.main_user_id.id

    def decline_barter(self):
        for this in self:
            if not this.main_user_id.id == self.env.user.id:
                raise ValidationError("Solo el propietario del producto puede realizar esta acción")
            this.state = 'rejected'
            email_template = self.env.ref('l10n_ec_barter.mail_template_product_barter_rejected')
            email_values = email_template.generate_email(this.id, ['subject', 'body_html',
                                                                   'email_from', 'email_to',
                                                                   'auto_delete'])
            email_values['model'] = 'l10n_ec.product.template.barter'
            email_values['res_id'] = this.id
            email_values['email_to'] = this.offered_user_id.email
            send_email = self.env['mail.mail'].sudo().create(email_values)
            send_email.send()
