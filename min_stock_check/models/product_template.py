from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    min_stock_qty_day = fields.Integer(
        string='Check Minimum Stock Quantity Before (days)'
    )
