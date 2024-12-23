# -*- coding: utf-8 -*-

from odoo import models, fields, api

            # TrasientModel = tablas temporales, no guardan los datos permanentemente
            # Recomendado para popus
class UpdateWizard(models.TransientModel):
    _name = 'update.wizard'
    #_description = 'Wizard para actualizar vista general'
    
    name = fields.Char(string='Nueva descripción')

    def update_vista_general(self):
        presupuesto_obj = self.env['presupuesto']
        #presupuesto_id = presupuesto_obj.search([('id', '=', self._context['active_id'])])
        
        # El search de abajo siempre buscará por el id
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.vista_general = self.name
