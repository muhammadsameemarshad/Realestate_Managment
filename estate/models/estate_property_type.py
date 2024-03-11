from odoo import fields, models
from datetime import datetime, timedelta


class EstatePropertiesType(models.Model):
    _name = 'estate.property.type'
    _description = "Model for Real-Estate Properties Type"

    name = fields.Char(required=True)