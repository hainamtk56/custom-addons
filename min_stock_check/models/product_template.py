from odoo import models, fields, api
from datetime import datetime, timedelta, date
from odoo.tools import float_compare


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_stock_qty_day = fields.Integer(
        string='Check Minimum Stock Quantity Before (days)'
    )
