# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UpdateWizard(models.TransientModel):
    _name = 'update.wizard'
    _description = 'Wizard para actualizar vista general'
    
    name = fields.Char(string='Nueva descripción')
