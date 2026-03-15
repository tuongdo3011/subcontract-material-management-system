from odoo import fields, models, api

class SubcontractMaterialRefuseWizard(models.TransientModel):
    _name = "subcontract.material.refuse.wizard"
    _description = "Lý do từ chối phê duyệt gia công nguyên vật liệu"
    
    reason = fields.Text(string="Lý do", required=True)
    order_id = fields.Many2one("subcontract.material.order", string="Đơn hàng")

    def action_confirm_refuse(self):
        """Khi ấn nút Xác nhận, chuyển trạng thái Đơn gia công hiện tại sang Từ chối và cập nhật Lý do"""
        self.order_id.write({
            'state': 'rejected',
            'reason': self.reason
        })
