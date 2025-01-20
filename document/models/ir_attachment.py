from odoo import models, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        attachments = super().create(vals_list)
        for attachment in attachments:
            if attachment.res_model and attachment.res_id:
                record = self.env[attachment.res_model].browse(attachment.res_id)
                if hasattr(record, 'message_post'):
                    record.message_post(
                        attachment_ids=[attachment.id],
                        subtype_xmlid='mail.mt_note'
                    )
        return attachments
