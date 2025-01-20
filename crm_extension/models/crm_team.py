import calendar
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    # Monthly target fields
    target_january = fields.Float('January Target', default=0)
    target_february = fields.Float('February Target', default=0)
    target_march = fields.Float('March Target', default=0)
    target_april = fields.Float('April Target', default=0)
    target_may = fields.Float('May Target', default=0)
    target_june = fields.Float('June Target', default=0)
    target_july = fields.Float('July Target', default=0)
    target_august = fields.Float('August Target', default=0)
    target_september = fields.Float('September Target', default=0)
    target_october = fields.Float('October Target', default=0)
    target_november = fields.Float('November Target', default=0)
    target_december = fields.Float('December Target', default=0)

    actual_revenue = fields.Float('Actual Revenue', readonly=True, compute='_compute_actual_revenue')
    target_revenue = fields.Float('Target Revenue', readonly=True, compute='_compute_target_revenue')
    sale_diff = fields.Float('Sale Difference', readonly=True, compute='_compute_sale_diff')

    @api.depends('actual_revenue', 'target_revenue')
    def _compute_sale_diff(self):
        for team in self:
            team.sale_diff = team.actual_revenue - team.target_revenue

    @api.constrains('target_january', 'target_february', 'target_march',
                    'target_april', 'target_may', 'target_june',
                    'target_july', 'target_august', 'target_september',
                    'target_october', 'target_november', 'target_december')
    def _check_target_values(self):
        for record in self:
            target_fields = ['target_january', 'target_february', 'target_march',
                             'target_april', 'target_may', 'target_june',
                             'target_july', 'target_august', 'target_september',
                             'target_october', 'target_november', 'target_december']
            for field in target_fields:
                if getattr(record, field) <= 0:
                    raise ValidationError(
                        f"Target value for {field.replace('target_', '').capitalize()} must be greater than 0")

    def _compute_actual_revenue(self):
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
                ('team_id', '=', record.id),
                ('create_date', '>=', f'{year}-{month}-01'),
                ('create_date', '<', f'{end_year}-{end_month}-01'),
                ('type', '=', 'opportunity')
            ]

            opportunities = self.env['crm.lead'].search(domain)
            record.actual_revenue = sum(opp.actual_revenue for opp in opportunities)

    @api.depends('target_january', 'target_february', 'target_march',
                 'target_april', 'target_may', 'target_june',
                 'target_july', 'target_august', 'target_september',
                 'target_october', 'target_november', 'target_december')
    def _compute_target_revenue(self):
        for record in self:
            month = str(datetime.now().month).zfill(2)
            month_name = calendar.month_name[int(month)].lower()
            target_field = f'target_{month_name}'
            record.target_revenue = getattr(record, target_field, 0.0)
