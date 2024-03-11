from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class EstateProperties(models.Model):
    default_date = datetime.now() + timedelta(days=90)

    _name = "estate.property"
    _description = "Model for Real-Estate Properties"
    name = fields.Char(required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.Many2many('estate.property.offer', string='Property Offers')
    description = fields.Text("Description")
    postcode = fields.Char("PostCode")
    date_availability = fields.Date("Date Available", default=default_date, copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area(sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation")
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        string="State")
    available_from = fields.Date("Available From",  default=lambda self: fields.Date.today())
    salesman = fields.Many2one('res.users', default=lambda self: self.env.user, string="Salesman")
    buyer = fields.Many2one('res.partner', string="Buyer", readonly=True, compute='_set_buyer')
    total_area = fields.Float("Total Area", compute='_compute_total')
    best_offer = fields.Float("Best Offer", compute='_compute_offers')
    status = fields.Char("Status", readonly=True)
    offer_state = fields.Char(default=lambda self: self.offer_ids.state, string="Offer State")

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = (record.living_area + record.garden_area)

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.onchange('garden')
    def _compute_garder(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                pass

    def action_do_cancel(self):
        for record in self:
            if record.status != 'Sold':
                record.status = "Cancel"
            if record.status == 'Sold':
                raise UserError("Property is Sold-out")
        return True

    def action_do_sold(self):
        for record in self:
            if record.status != 'Cancel':
                record.status = "Sold"
            if record.status == 'Cancel':
                raise UserError("Property is Canceled")
        return True

    @api.onchange('offer_ids.state')
    def _set_buyer(self):
        for record in self:
            if record.status == "Sold":
                offer_accepted = record.offer_ids.filtered(lambda offer: offer.state == 'accepted')
                if not offer_accepted:
                    record.buyer = None
                    continue
                offer = offer_accepted[0]
                record.buyer = offer.partner_id

            else:
                offer_accepted = record.offer_ids.filtered(lambda offer: offer.state == 'accepted')
                if not offer_accepted:
                    record.buyer = None
                    continue
                offer = offer_accepted[0]
                record.buyer = offer.partner_id
                record.status = "Sold"


