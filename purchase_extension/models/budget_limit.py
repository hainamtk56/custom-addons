# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BudgetLimit(models.Model):
    _name = 'budget.limit'

    staff = fields.Many2one(
        'res.users',
        string='Staff',
        required=True,
        domain=lambda self: [('groups_id', 'in', [self.env.ref('purchase_extension.group_purchasing_staff').id])]
    )
    limit = fields.Float(string='Budget Limit per Order', required=True)

    @api.constrains('limit')
    def _check_limit(self):
        for record in self:
            if record.limit <= 0:
                raise ValueError('Budget limit must be positive')

    @api.constrains('staff')
    def _check_staff(self):
        for record in self:
            if self.search_count([('staff', '=', record.staff.id)]) > 1:
                raise ValidationError('Each staff member can have only one budget limit')
