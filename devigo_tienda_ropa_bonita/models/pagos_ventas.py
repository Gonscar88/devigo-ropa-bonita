# -*- coding: utf-8 -*-
"""
@author: Oscar González M. <oggonzalezm96@gmail.com>
@Date: 18/03/25
@project devigo_tienda_ropa_bonita
@name: pagos_ventas
"""

from odoo import api, fields, models


class PagosVentas(models.Model):
    _name = 'tienda_ropa.pagos'
    _description = 'Pagos de Ventas'

    fecha_pago = fields.Date(string='Fecha de Pago')

    monto = fields.Float(string='Monto')

    venta_id = fields.Many2one('sale.order', string='Venta')

    notas = fields.Char(
        string="Notas extra",
    )

    pago_recibido = fields.Boolean(
        "Pago recibido", help="El pago ya ha sido recibido por la administración"
    )

    @api.model
    def default_get(self, fields_list):
        """Método para establecer valores por defecto cuando se abre desde una venta"""
        res = super(PagosVentas, self).default_get(fields_list)
        if self._context.get('active_model') == 'sale.order' and self._context.get('active_id'):
            res['venta_id'] = self._context.get('active_id')
            res['fecha_pago'] = fields.Date.context_today(self)
        return res
    
    def action_confirm_payment(self):
        """Método que se ejecuta al confirmar el pago"""
        # Aquí puedes agregar la lógica adicional que necesites
        # Por ejemplo, actualizar campos en la orden de venta, crear entradas contables, etc.
        self.venta_id._compute_total_pagado()
        self.venta_id._compute_monto_comision()
        return {'type': 'ir.actions.act_window_close'}
    