from odoo import models, api, fields


class L10nEcBarterRatingWizard(models.TransientModel):
    _name = 'l10n_ec.barter.rating.wizard'

    user_id = fields.Many2one(
        'res.users',
        string='Usuario'
    )
    rating_user_id = fields.Many2one(
        'res.users',
        string='Valorador',
        default=lambda self: self.env.user
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
    barter_template_id = fields.Many2one(
        'l10n_ec.product.template.barter',
        string="Oferta"
    )

    def create_rating(self):
        rating_user_obj = self.env['res.user.barter.rating']
        for this in self:
            rating_user_obj.create({
                'user_id': this.user_id.id,
                'rating_user_id': this.rating_user_id.id,
                'rating': this.rating,
                'comment': this.comment
            })
            if this.barter_template_id.main_user_id.id == this.rating_user_id.id:
                this.barter_template_id.main_product_id.l10n_ec_qualify_main = True
                this.barter_template_id.product_offered_id.l10n_ec_qualify_offer = True
            if this.barter_template_id.offered_user_id.id == this.rating_user_id.id:
                this.barter_template_id.main_product_id.l10n_ec_qualify_offer = True
                this.barter_template_id.product_offered_id.l10n_ec_qualify_main = True
