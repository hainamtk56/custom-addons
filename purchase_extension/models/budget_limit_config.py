# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BudgetLimitConfig(models.Model):
    _name = 'budget.limit.config'

    config = fields.Many2many('budget.limit', string='Budget Limits', domain=lambda self : [('staff.groups_id', 'in', [self.env.ref('purchase_extension.group_purchasing_staff').id])])