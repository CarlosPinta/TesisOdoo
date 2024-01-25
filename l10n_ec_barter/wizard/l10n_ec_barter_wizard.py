from odoo import models, api, fields
from datetime import datetime


class L10nEcBarterWizard(models.TransientModel):
    _name = 'l10n_ec.barter.wizard'
    _description = 'Permite Crear una propuesta para un producto especifico'

    main_product_id = fields.Many2one(
        'product.template',
        string="Producto Padre",
        required=True
    )
    product_offered_id = fields.Many2one(
        'product.template',
        string="Producto Ofrecido",
        required=True
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
            date_now = datetime.today().date()
            res = {
                "main_product_id": this.main_product_id.id,
                "product_offered_id": this.product_offered_id.id,
                "message": this.message,
                "date": date_now,
                "user_id": this.user_id.id
            }
            barter_line_obj.create(res)
            return True
