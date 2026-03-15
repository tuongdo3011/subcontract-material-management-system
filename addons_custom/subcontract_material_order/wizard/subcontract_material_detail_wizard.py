from odoo import models, fields, api

class SubcontractMaterialDetailWizard(models.TransientModel):
    _name = "subcontract.material.detail.wizard"
    _description = "Chi tiết lịch sử hàng về"

    history_id = fields.Many2one("subcontract.material.history")
    date_receipted = fields.Date("Ngày nhận")
    total_qty_receipted = fields.Integer("Tổng số lượng nhận")
    finished_product = fields.Many2one("product.product", string="Thành phẩm")
    qty_receipted = fields.Integer("Số lượng nhận")
    
    
    