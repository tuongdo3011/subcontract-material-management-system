from odoo import models, fields, api

class SubcontractMaterialHistory(models.Model):
    _name = "subcontract.material.history"
    _description = "Lịch sử hàng về"

    order_id = fields.Many2one("subcontract.material.order")
    finished_line_id = fields.Many2one("subcontract.material.finished")
    date_receipted  = fields.Date("Ngày nhận")
    total_qty_receipted = fields.Integer("Tổng số lượng nhận")

    def action_view_detail(self):
        """Hiển thị pop up Lịch sử hàng về khi ấn nút Chi tiết"""
        return {
            'name': 'Lịch sử hàng về',
            'type': 'ir.actions.act_window',
            'res_model': 'subcontract.material.detail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_history_id': self.id,
                        'default_date_receipted': self.date_receipted,
                        'default_total_qty_receipted': self.total_qty_receipted,
                        }
        }
    