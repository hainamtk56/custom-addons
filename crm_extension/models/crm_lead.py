# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    minimum_revenue = fields.Float('Minimum Revenue (Before VAT)')
    is_manager = fields.Boolean(
        'Is Manager',
        compute='_compute_is_manager',
        compute_sudo=False
    )
    sales_team_member_ids = fields.Many2many(
        'res.users',
        string='Sales Team Members',
        compute='_compute_sales_team_member_ids',
        compute_sudo=False
    )

    actual_revenue = fields.Float(
        'Actual Revenue',
        compute='_compute_actual_revenue',
        store=True
    )

    priority = fields.Selection(tracking=True)

    @api.depends('order_ids.state', 'order_ids.amount_untaxed')
    def _compute_actual_revenue(self):
        for lead in self:
            lead.actual_revenue = sum(
                order.amount_untaxed for order in lead.order_ids.filtered(lambda o: o.state == 'sale')
            )

    @api.depends_context('uid')
    def _compute_sales_team_member_ids(self):
        for record in self:
            current_user = self.env.user
            result = []

            if current_user.has_group('crm_extension.group_sales_manager'):
                # Nếu là manager, lấy tất cả thành viên của mọi team
                teams = self.env['crm.team'].search([])
                for team in teams:
                    result.extend(team.member_ids.ids)
                    result.append(team.user_id.id)  # Thêm team leader
            else:
                # Nếu không phải manager, chỉ lấy thành viên của team hiện tại
                if record.team_id and current_user.sale_team_id == record.team_id:
                    result.extend(current_user.sale_team_id.member_ids.ids)
                    result.append(record.team_id.user_id.id)  # Thêm team leader

            # Loại bỏ các ID trùng lặp
            result = list(set(result))
            record.sales_team_member_ids = result

            # Nếu user không thuộc team hiện tại, set user_id = False
            if not result:
                record.write({'user_id': False})

    @api.constrains('minimum_revenue')
    def _check_minimum_revenue(self):
        if any(record.minimum_revenue <= 0 for record in self):
            raise exceptions.ValidationError("Minimum Revenue must be greater than 0")

    def action_sale_quotations_new(self):
        action = super().action_sale_quotations_new()
        if any(record.minimum_revenue <= 0 for record in self):
            raise exceptions.ValidationError("Minimum Revenue must be greater than 0")
        return action

    @api.depends_context('uid')
    def _compute_is_manager(self):
        for record in self:
            record.is_manager = self.env.user.has_group('crm_extension.group_sales_manager')