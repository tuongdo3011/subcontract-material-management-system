# Subcontract Material Management System (Odoo Custom Module)

## 📌 Project Overview
A specialized Odoo module designed to digitalize and streamline the subcontracting workflow. This solution enables businesses to efficiently manage the lifecycle of raw materials sent to external partners and track the receipt of finished products, ensuring inventory accuracy and process transparency.

## 🚀 Key Features
- **End-to-End Workflow:** Manage subcontracting orders through multiple stages from `Draft` ➔ `Done`.
- **Automated Sequencing:** Custom logic to generate unique reference numbers (e.g., `GCNVL/2026/0001`).
- **Interactive Wizards:** Used Transient Models to handle complex actions like "Refuse Order" and "Input Details" via pop-up interfaces.
- **Inventory Integration:** Inherited and extended Odoo core models (`product.template`, `stock.warehouse`) to seamlessly link subcontracting data with standard inventory modules.
- **Detailed History Tracking:** Automatic logging of material movements and delivery history.

## 🛠 Technical Stack
- **Backend:** Python, Odoo Framework (ORM, Logic)
- **Frontend:** XML (QWeb, Form/Tree/Search views)
- **Database:** PostgreSQL
- **Tools:** VS Code, Git/GitHub

## 🏗 Database Architecture
The module implements a robust relational structure:
- **Relational Fields:** Extensive use of `Many2one` and `One2many` to connect Subcontract Orders with Raw Materials and Finished Goods.
- **Inheritance:** Leveraging Odoo's class-level inheritance to expand standard functionalities without modifying core code.


## 📂 Installation
1. Clone this repository into your Odoo `addons` folder.
2. Update your Odoo configuration to include the path to this module.
3. Activate the Developer Mode in Odoo.
4. Go to **Apps** -> **Update Apps List**.
5. Search for `Gia công nguyên vật liệu` and click **Install**.
