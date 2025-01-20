# -*- coding: utf-8 -*-

from odoo import models, fields, exceptions, api


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _description = 'Plan Sale Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Text('Name', required=True)
    order_id = fields.Many2one('sale.order', string='Order', readonly=True, required=True)
    information = fields.Text('Sale plan information', required=True)
    status = fields.Selection(
        [('draft', 'Draft'), ('sent', 'Sent'), ('approved', 'Approved'), ('rejected', 'Rejected')], string='Status',
        readonly=True, default='draft')
    approvers = fields.One2many('approver', 'plan_sale_order_id', string='approvers')

    @api.model
    def create(self, vals):
        plans = super(PlanSaleOrder, self).create(vals)
        for plan in plans:
            if plan.order_id:
                plan.order_id.plan_sale_order_id = plan
        return plans

    @api.constrains('approvers')
    def _check_approvers(self):
        if not self.approvers:
            raise exceptions.ValidationError("Please add approvers before submit")
        # check duplicate approvers
        approvers = self.approvers.mapped('partner_id')  # sum of approver
        if len(approvers) != len(self.approvers):  # if sum of approver != sum of unique approvers
            raise exceptions.ValidationError("Duplicate approvers")
        # current user must not be in approvers
        current_user = self.env.user.partner_id
        if current_user in approvers:
            raise exceptions.ValidationError("You can not be an approver")

    def action_submit(self):
        for record in self:
            approvers_ids = [approver.partner_id.id for approver in record.approvers]
            mess = f"Business plan {record.name} is waiting for your approval."
            record.message_post(
                author_id=self.env.ref('base.partner_root').id,
                subject='New business plan!',
                body=mess,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
                partner_ids=approvers_ids
            )
            record.status = 'sent'
            for approver in record.approvers:
                approver.status = 'pending'  # set status of each approver to pending
