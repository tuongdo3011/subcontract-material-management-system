from odoo import fields, models, api

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"
    
    is_material_warehouse = fields.Boolean("Là kho NVL")