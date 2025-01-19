# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import json
import calendar


class MonthlyReport(http.Controller):
    def _get_data(self, month):
        teams = http.request.env['crm.team'].sudo().search([])
        departments = http.request.env['hr.department'].sudo().search([])
        result = {}

        team_results = []
        department_results = []

        year = str(datetime.now().year)
        month = str(month).zfill(2)

        if int(month) >= 12:
            end_year = str(int(year) + 1)
            end_month = '01'
        else:
            end_year = year
            end_month = str(int(month) + 1).zfill(2)

        for team in teams:
            domain = [
                ('team_id', '=', team.id),
                ('create_date', '>=', f'{year}-{month}-01'),
                ('create_date', '<', f'{end_year}-{end_month}-01'),
                ('type', '=', 'opportunity')
            ]

            opportunities = http.request.env['crm.lead'].sudo().search(domain)
            actual_revenue = sum(opp.actual_revenue for opp in opportunities)

            month_name = calendar.month_name[int(month)].lower()
            target_field = f'target_{month_name}'
            target_revenue = getattr(team, target_field, 0.0)

            sale_diff = actual_revenue - target_revenue


            team_results.append({
                'sales_team_name': team.name,
                'real_revenue': actual_revenue,
                'diff': sale_diff,
            })

        for department in departments:
            domain = [
                ('department_id', '=', department.id),
                ('create_date', '>=', f'{year}-{month}-01'),
                ('create_date', '<', f'{end_year}-{end_month}-01'),
                ('state', '=', 'purchase'),
            ]
            purchase_orders = http.request.env['purchase.order'].sudo().search(domain)
            actual_spending = sum(po.amount_total for po in purchase_orders)
            po_diff = actual_spending - department.spending_limit

            department_results.append({
                'department_name': department.name,
                'real_cost': actual_spending,
                'diff': po_diff,
            })

        result['sales'] = team_results
        result['purchase'] = department_results
        return result


    @http.route('/monthly_report', type='http', auth='public', methods=['POST'], csrf=False)
    def index(self, **kw):
        try:
            data = request.httprequest.data
            data = json.loads(data)
            if not data.get('token') or data['token'] != "odooneverdie":
                return json.dumps({
                    'code': 404,
                    'status': 'error',
                    'message': 'Invalid token',
                })
            if not data.get('month'):
                return json.dumps({
                    'code': 404,
                    'status': 'error',
                    'message': 'Invalid month',
                })
            result = self._get_data(data['month'])
            result['code'] = 200
            return json.dumps(result)
        except Exception as e:
            return json.dumps({
                "code": 404,
                "status": "error",
                "message": str(e),
            })

