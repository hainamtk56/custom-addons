from odoo import models, fields, api, exceptions

class SaleOder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Business Plan')

    def action_confirm(self):
        for record in self:
            if record.state != 'sale':
                if not record.plan_sale_order_id:
                    raise exceptions.ValidationError("Business plan has not been set")
                if record.plan_sale_order_id.status != 'approved':
                    raise exceptions.ValidationError("Business plan has not been approved")
        return super().action_confirm()

    def action_create_plan_sale_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Plan Sale Order',
            'res_model': 'plan.sale.order',
            'view_mode': 'form',
            'context': {'default_order_id': self.id}
            }

