# -*- coding: utf-8 -*-
"""
@author: Oscar González M. <oggonzalezm96@gmail.com>
@Date: 18/03/25
@project devigo_tienda_ropa_bonita
@name: pagos_ventas
"""
MONTO_DEFAULT_COMISION = 40

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pagos_ids = fields.One2many('tienda_ropa.pagos', 'venta_id', string='Pagos')

    total_pagado = fields.Float(
        string="Total Pagado",
        compute='_compute_total_pagado',
        store=True
    )

    total_adeudado = fields.Float(
        string="Total adeudado",
        compute='_compute_total_pagado',
        store=True
    )

    porcentaje_comision = fields.Float(
        string="Porcentaje de comisión",
        default=MONTO_DEFAULT_COMISION,
        group_operator="avg"
    )

    monto_comision = fields.Float(
        string="Monto de comisión",
        compute='_compute_monto_comision',
        store=True,
        help="El monto de comisión se paga sobre el margen de ganancia"
    )

    comision_pagada = fields.Boolean(
        string="Comisión Pagada",
        default=False
    )

    @api.depends('pagos_ids.monto')
    def _compute_total_pagado(self):
        for record in self:
            record.total_pagado = sum(record.pagos_ids.mapped('monto'))
            record.total_adeudado = record.amount_total - record.total_pagado

    
    def marcar_comision_pagada(self):
        self.comision_pagada = True

    @api.depends('porcentaje_comision')
    def _compute_monto_comision(self):
        for record in self:
            record.monto_comision = ((record.margin * record.porcentaje_comision) / 100 ) \
                if record.state in ['sale', 'done'] else 0 
    
    