# models/sales_target_report.py
from odoo import models, fields


class SalesTargetReport(models.Model):
    _name = 'sales.target.report'
    _description = 'Sales Target Report'

    sales_team_id = fields.Many2one('crm.team', string='Sales Team', required=True)
    actual_revenue = fields.Float('Actual Revenue', readonly=True)
    target_revenue = fields.Float('Target Revenue', readonly=True)
