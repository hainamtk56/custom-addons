# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class Department(models.Model):
    _inherit = 'hr.department'
    _description = 'Department Inherit'

    spending_limit = fields.Float(string='Spending Limit/Month', default=0.0)
    actual_spending = fields.Float(string='Actual Spending', compute='_compute_actual_spending')
    po_diff = fields.Float('PO Difference', readonly=True, compute='_compute_po_diff')

    @api.depends('actual_spending', 'spending_limit')
    def _compute_po_diff(self):
        for record in self:
            record.po_diff = record.actual_spending - record.spending_limit

    def _compute_actual_spending(self):
        year = str(datetime.now().year)
        month = str(datetime.now().month).zfill(2)

        if int(month) >= 12:
            end_year = str(int(year) + 1)
            end_month = '01'
        else:
            end_year = year
            end_month = str(int(month) + 1).zfill(2)

        for record in self:
            domain = [
                ('department_id', '=', record.id),
                ('create_date', '>=', f'{year}-{month}-01'),
                ('create_date', '<', f'{end_year}-{end_month}-01'),
                ('state', '=', 'purchase'),
            ]
            purchase_orders = self.env['purchase.order'].search(domain)
            record.actual_spending = sum(po.amount_total for po in purchase_orders)