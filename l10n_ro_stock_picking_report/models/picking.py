# ©  2008-2020 Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_report_base_filename(self):
        self.ensure_one()
        return "{} {}".format(self.picking_type_id.name, self.name)
