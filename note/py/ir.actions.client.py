def show_notification(self):
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Thông báo',
            'message': 'Thao tác đã hoàn thành',
            'type': 'success',  # 'success', 'warning', 'danger', 'info'
            'sticky': False,    # True để thông báo không tự động biến mất
            'next': {           # Action tiếp theo sau khi hiển thị thông báo
                'type': 'ir.actions.act_window',
                'name': 'Quay về danh sách',
                'res_model': 'your.model',
                'view_mode': 'tree,form',
            }
        }
    }