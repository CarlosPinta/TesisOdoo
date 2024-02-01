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
    l10n_ec_barter_line_ids = fields.One2many(
        "l10n_ec.product.template.barter",
        "main_product_id",
        string='Ofertas'
    )
    l10n_ec_description = fields.Text(
        string='Descripción del Producto'
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

    def action_propose_barter(self):
        view_id = self.env.ref('l10n_ec_barter.l10n_ec_barter_wizard_form').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'l10n_ec.barter.wizard',
            'view_mode': 'form',
            'name': 'Ofertar',
            'view_id': view_id,
            'target': 'new',
            "context": {'default_main_product_id': self.id}
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
        required=True
    )
    date = fields.Date(
        string="Fecha",
        default=lambda self: fields.Date.today()
    )
    message = fields.Char(
        string="Mensaje"
    )
    user_id = fields.Many2one(
        'res.users',
        string="Usuario",
    )

    def accept_barter(self):
        for this in self:
            return True

    def decline_barter(self):
        for this in self:
            return True
