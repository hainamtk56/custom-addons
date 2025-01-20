# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import models, fields
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    department_id = fields.Many2one('hr.department', string='Department', required=True)
    binary_file = fields.Binary(string="Binary File")

    def button_confirm(self):
        current_user = self.env.user

        if current_user.has_group('purchase_extension.group_purchasing_staff'):
            current_user_budget_limit = self.env['budget.limit'].search([
                ('staff', '=', current_user.id)
            ], limit=1).limit

            if self.amount_total > current_user_budget_limit:
                self.create_purchase_activity()
                self._cr.commit()
                raise UserError('This order exceeds your budget limit per order')

        return super().button_confirm()

    def create_purchase_activity(self):
        accountant_group = self.env.ref('purchase_extension.group_accountant')
        users = accountant_group.users

        for user in users:
            values = {
                'res_model_id': self.sudo().env.ref('purchase.model_purchase_order').id,
                'res_id': self.id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': f'Review Purchase Order {self.name}',
                'note': f'''
                    Vui lòng xem xét đơn hàng:
                    - Tổng giá trị: {self.amount_total}
                    - Nhà cung cấp: {self.partner_id.name}
                    - Phòng ban: {self.department_id.name}
                ''',
                'date_deadline': fields.Date.today() + timedelta(days=7),
                'user_id': user.id
            }

            self.env['mail.activity'].create(values)
