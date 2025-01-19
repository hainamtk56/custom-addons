from odoo import models, fields, exceptions, api


class Appover(models.Model):
    _name = 'approver'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Approver'

    partner_id = fields.Many2one('res.partner', string='Name', required=True, domain=[('user_ids', '!=', False)])
    is_approver = fields.Boolean(compute='_compute_is_approver')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='pending')

    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')

    def _compute_is_approver(self):
        current_user = self.env.user
        for record in self:
            record.is_approver = bool(record.partner_id.user_ids.filtered(lambda u: u.id == current_user.id))

    def action_approve(self):
        for record in self:
            if not record.is_approver:
                raise exceptions.UserError("You do not have the right to approve this plan!")
            record.status = 'approved'
            mess = f"Business plan was approved by {record.partner_id.name}."
            creator_user_id = self.plan_sale_order_id.create_uid
            self.plan_sale_order_id.message_post(
                body=mess,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
                partner_ids=[creator_user_id.partner_id.id],
            )
        self._check_status_to_change_plan_sale_order_status()

    def action_reject(self):
        for record in self:
            if not record.is_approver:
                raise exceptions.UserError("You do not have the right to reject this plan!")
            record.status = 'rejected'
            mess = f"Business plan was rejected by {record.partner_id.name}."
            creator_user_id = self.plan_sale_order_id.create_uid
            self.plan_sale_order_id.message_post(
                body=mess,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
                partner_ids=[creator_user_id.partner_id.id],
            )
        self._check_status_to_change_plan_sale_order_status()

    def _check_status_to_change_plan_sale_order_status(self):
        for record in self:
            if all(approver.status == 'approved' for approver in record.plan_sale_order_id.approvers):
                record.plan_sale_order_id.status = 'approved'
            elif all(approver.status != 'pending' for approver in record.plan_sale_order_id.approvers):
                record.plan_sale_order_id.status = 'rejected'
            else:
                record.plan_sale_order_id.status = 'sent'
