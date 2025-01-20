# models/sales_report_wizard.py
import calendar
from datetime import datetime

from odoo import models, fields


class SalesReportWizard(models.TransientModel):
    _name = 'sales.report.wizard'
    _description = 'Sales Report Wizard'

    # Lấy tháng hiện tại làm giá trị mặc định
    def _get_default_month(self):
        return str(datetime.now().month)

    month = fields.Selection([
        ('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month', required=True, default=_get_default_month)

    sales_team_ids = fields.Many2many('crm.team', string='Sales Teams')

    def action_generate_detail_report(self):
        year = str(datetime.now().year)
        month = self.month.zfill(2)

        if int(month) >= 12:
            end_year = str(int(year) + 1)
            end_month = '01'
        else:
            end_year = year
            end_month = str(int(month) + 1).zfill(2)

        domain = [
            ('create_date', '>=', f'{year}-{month}-01'),
            ('create_date', '<', f'{end_year}-{end_month}-01'),
            ('type', '=', 'opportunity')
        ]

        if self.sales_team_ids:
            domain.append(('team_id', 'in', self.sales_team_ids.ids))

        return {
            'name': f'Sales Detail Report - {self.month}/{year}',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'list',
            'view_id': self.env.ref('crm_extension.crm_lead_detail_report_list').id,
            'domain': domain,
            'target': 'current',
        }

    def action_generate_target_report(self):
        self.ensure_one()
        # Tạo báo cáo đánh giá chỉ tiêu
        report_model = self.env['sales.target.report']
        report_lines = []

        # Lọc teams theo selection
        teams = self.sales_team_ids or self.env['crm.team'].search([])

        for team in teams:
            year = str(datetime.now().year)
            month = self.month.zfill(2)

            if int(month) >= 12:
                end_year = str(int(year) + 1)
                end_month = '01'
            else:
                end_year = year
                end_month = str(int(month) + 1).zfill(2)
            domain = [
                ('team_id', '=', team.id),
                ('create_date', '>=', f'{year}-{month}-01'),
                ('create_date', '<', f'{end_year}-{end_month}-01'),
                ('type', '=', 'opportunity')
            ]

            opportunities = self.env['crm.lead'].search(domain)
            actual_revenue = sum(opp.actual_revenue for opp in opportunities)

            # Lấy chỉ tiêu từ cấu hình theo biến month
            month_name = calendar.month_name[int(month)].lower()
            target_field = f'target_{month_name}'
            target_revenue = getattr(team, target_field, 0.0)

            # Tạo record báo cáo
            report_line = report_model.create({
                'sales_team_id': team.id,
                'actual_revenue': actual_revenue,
                'target_revenue': target_revenue,
            })
            report_lines.append(report_line.id)

        # Trả về action để mở view
        return {
            'name': f'Sales Target Report - {self.month}/{datetime.now().year}',
            'type': 'ir.actions.act_window',
            'res_model': 'sales.target.report',
            'view_mode': 'list',
            'view_id': self.env.ref('crm_extension.sales_target_report_list').id,
            'domain': [('id', 'in', report_lines)],
            'target': 'current',
        }
