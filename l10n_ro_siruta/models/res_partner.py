# -*- coding: utf-8 -*-
##############################################################################
#
#     Author:  Fekete Mihai <mihai.fekete@forbiom.eu>
#    Copyright (C) 2014 FOREST AND BIOMASS SERVICES ROMANIA SA
#    (http://www.forbiom.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    city_id = fields.Many2one('res.country.city', string='City', ondelete='set null', index=True)
    city = fields.Char(related='city_id.name', string='City', store=True)
    commune_id = fields.Many2one('res.country.commune', string='City/Commune', ondelete='set null', index=True)
    zone_id = fields.Many2one('res.country.zone', string='Zone', ondelete='set null', index=True)

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.commune_id = self.city_id.commune_id.id
            self.state_id = self.city_id.state_id.id
            self.zone_id = self.city_id.zone_id.id
            self.country_id = self.city_id.country_id.id

    @api.model
    def _address_fields(self):
        """ Extends list of address fields with city_id, commune_id, zone_id
        to be synced from the parent when the `use_parent_address`
        flag is set. """
        new_list = ['city_id', 'commune_id', 'zone_id']
        return super(ResPartner, self)._address_fields() + new_list

    @api.one
    def _search_city(self):
        city_obj = self.env['res.country.city']
        if self.state_id:
            city_id = city_obj.search([("name", "ilike", self.city),
                                       ("state_id", "=", self.state_id.id)])
            if city_id:
                self.city_id = city_id[0].id
        else:
            city_id = city_obj.search([("name", "ilike", self.city)])
            if city_id:
                self.city_id = city_id[0].id

    @api.model
    def _install_l10n_ro_siruta(self):
        """Updates city_id field by searching on city and state_id."""
        partners = self.search([("city", "!=", False)])
        partners._search_city()



    @api.onchange('commune_id')
    def _onchange_commune_id(self):
        if self.city_id.commune_id != self.commune_id:
            self.city_id = False

        if self.commune_id:
            domain = [('commune_id', '=', self.commune_id.id)]
        else:
            domain = []
        return {'domain': {'city_id': domain}}



    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.commune_id.state_id != self.state_id:
            self.commune_id = False
        if self.state_id:
            domain = [('state_id', '=', self.state_id.id)]
        else:
            domain = []
        return {'domain': {'commune_id': domain}}
