# ©  2015-2018 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _reconcile_account_move_lines(self, data):
        if self.company_id.romanian_accounting:
            data['stock_output_lines'] = {}
        return super(PosSession, self)._reconcile_account_move_lines(data)


    def _accumulate_amounts(self, data):
        data = super(PosSession, self)._accumulate_amounts(data)

        amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0}

        if self.company_id.romanian_accounting:
            # nu trebuie generate note contabile  pentru ca acestea sunt generate in miscarea de stoc
            data.update({
                'stock_expense': defaultdict(amounts),
                'stock_return': defaultdict(amounts),
                'stock_output': defaultdict(amounts),
            })

        return data
