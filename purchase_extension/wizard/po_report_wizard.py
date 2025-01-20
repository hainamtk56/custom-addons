from datetime import datetime

from odoo import fields, models


class POReportWizard(models.TransientModel):
    _name = 'po.report.wizard'
    _description = "Purchase Order Report Wizard"

    def _get_default_month(self):
        return str(datetime.now().month)

    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', required=True, default=_get_default_month)

    department_ids = fields.Many2many('hr.department', string="Department")

    def action_export_data(self):
        report_model = self.env['po.report']
        report_lines = []

        departments = self.department_ids or self.env['hr.department'].search([])

        year = str(datetime.now().year)
        month = self.month.zfill(2)

        if int(month) >= 12:
            end_year = str(int(year) + 1)
            end_month = '01'
        else:
            end_year = year
            end_month = str(int(month) + 1).zfill(2)

        for department in departments:
            domain = [
                ('department_id', '=', department.id),
                ('create_date', '>=', f'{year}-{month}-01'),
                ('create_date', '<', f'{end_year}-{end_month}-01'),
                ('state', '=', 'purchase'),
            ]
            purchase_orders = self.env['purchase.order'].search(domain)
            actual_spending = sum(po.amount_total for po in purchase_orders)
            report_line = report_model.create({
                'department_id': department.id,
                'actual_spending': actual_spending
            })
            report_lines.append(report_line.id)
        return {
            'name': f'Department Purchase report - {self.month.zfill(2)}/{datetime.now().year}',
            'type': 'ir.actions.act_window',
            'res_model': 'po.report',
            'view_mode': 'list',
            'view_id': self.env.ref('purchase_extension.view_po_report_list').id,
            'domain': [('id', 'in', report_lines)],
            'target': 'current',
        }
