from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import datetime


class L10nEcBarterWizard(models.TransientModel):
    _name = 'l10n_ec.barter.wizard'
    _description = 'Permite Crear una propuesta para un producto especifico'

    main_product_id = fields.Many2one(
        'product.template',
        string="Producto Padre",
        required=True
    )
    type = fields.Selection([
        ('product', 'Por Producto'),
        ('price', 'Por Valor')
    ],
        string="Tipo de Propuesta",
        default='product',
        required=True
    )
    product_offered_id = fields.Many2one(
        'product.template',
        string="Producto Ofrecido",
    )
    price = fields.Float(
        string="Precio"
    )
    message = fields.Char(
        string="Mensaje"
    )
    user_id = fields.Many2one(
        'res.users',
        string="Usuario",
        default=lambda self: self.env.uid,
        required=True
    )

    def create_barter(self):
        barter_line_obj = self.env['l10n_ec.product.template.barter'].sudo()
        for this in self:
            if this.main_product_id.l10n_ec_user_id.id == this.user_id.id:
                raise ValidationError("El propietario del producto no puede ofertar por el mismo producto")
            in_offer = this.main_product_id.l10n_ec_barter_line_ids.filtered(
                lambda line: line.state == 'pending' and line.product_offered.id != this.product_offered_id.id)
            if in_offer:
                raise ValidationError("No puede ofrecer el mismo producto dos veces, a menos que rechace la oferta")
            date_now = datetime.today().date()
            res = {
                "main_product_id": this.main_product_id.id,
                "type": this.type,
                "price": this.price,
                "product_offered_id": this.product_offered_id.id if this.product_offered_id else None,
                "message": this.message,
                "date": date_now,
                "offered_user_id": this.user_id.id
            }
            barter = barter_line_obj.create(res)
            email_template = self.env.ref('l10n_ec_barter.mail_template_product_barter_accept')
            email_values = email_template.generate_email(barter.id, ['subject', 'body_html',
                                                                     'email_from', 'email_to',
                                                                     'auto_delete'])
            email_values['model'] = 'l10n_ec.product.template.barter'
            email_values['res_id'] = barter.id
            email_values['email_to'] = barter.main_user_id.email
            send_email = self.env['mail.mail'].sudo().create(email_values)
            send_email.send()
            return True
