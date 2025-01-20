from odoo import fields, models


class POReport(models.Model):
    _name = 'po.report'
    _description = 'Purchase Report for Accountants'

    department_id = fields.Many2one('hr.department', string='Department')
    limit = fields.Float(related='department_id.spending_limit')
    actual_spending = fields.Float(string='Actual Spending')
