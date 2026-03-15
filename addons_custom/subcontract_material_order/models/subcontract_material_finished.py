from odoo import models, fields, api

class SubcontractMaterialFinished(models.Model):
    _name = "subcontract.material.finished"
    _description = "Thành phẩm"

    order_id = fields.Many2one("subcontract.material.order")
    product_id = fields.Many2one("product.product", string="Sản phẩm")
    qty = fields.Float(string="Số lượng")
    qty_received = fields.Float(string="Số lượng nhập")
    qty_remaining = fields.Float(string="Số lượng còn lại")