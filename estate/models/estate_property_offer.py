from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertiesOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Model for Real-Estate Properties Offers"
    price = fields.Float('Price')
    state = fields.Selection( selection=[('accepted', 'Accepted'), ('refused', 'Refused')], default=None, string='State', copy=False)
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    validity = fields.Integer(string="Validity(days)")
    date_deadline = fields.Date(string="Validity Date", compute='_compute_deadline',
                                inverse='_inverse_date_deadline', store=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (datetime.now() + timedelta(days=record.validity))

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date).days

    def action_do_accept(self):
        for record in self:
            record.state = 'accepted'
        return True

    def action_do_refused(self):
        for record in self:
            record.state = 'refused'
        return True

    @api.onchange('property_id')
    def _onchange_property_id(self):
        for offer in self:
            if offer.property_id.status == 'sold':
                raise UserError("Cannot add offer to sold property.")


    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
    ]
    @api.constrains("price")
    def _selling_price_constrains(self):
        for record in self:
            if record.price < (record.property_id.expected_price / 100)* 90:
                raise ValidationError("Offer price cannot br lower than 90% of expected price")



