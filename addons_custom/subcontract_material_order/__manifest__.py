{
    'name': 'Gia công nguyên vật liệu',
    'version': '1.0',
    'depends': ['base', 'stock', 'product', 'uom'],
    'category': 'Uncategorized',
    'description': "",
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'data/order_name_sequence.xml',
        'view/subcontract_material_order_views.xml',
        'view/subcontract_material_order_line_views.xml',
        'view/subcontract_material_finished_views.xml',
        'view/stock_warehouse_views.xml',
        'view/product_template_views.xml',
        'wizard/subcontract_material_refuse_wizard_views.xml',
        'wizard/subcontract_material_detail_wizard_views.xml',
        'view/subcontract_material_menus.xml',
    ]
}