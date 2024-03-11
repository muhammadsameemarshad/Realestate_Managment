from odoo import fields, models
from datetime import datetime, timedelta


class EstatePropertiesTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Model for Real-Estate Properties Tag"

    name = fields.Char(required=True)