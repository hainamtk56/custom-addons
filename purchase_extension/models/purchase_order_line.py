# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    rcm_vendor = fields.Many2one(
        'res.partner',
        string='Recommended Vendor',
        domain=[('id', 'in', 'self.product_id.seller_ids')]
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            self.rcm_vendor = False
            return

        supplier_infos = self.env['product.supplierinfo'].search([
            ('product_id', '=', self.product_id.id)
        ])

        if not supplier_infos:
            self.rcm_vendor = False
            return

        sorted_suppliers = sorted(
            supplier_infos,
            key=lambda s: (s.price, s.delay or 0)
        )

        self.rcm_vendor = sorted_suppliers[0].partner_id if sorted_suppliers else False
