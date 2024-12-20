# -*- coding: utf-8 -*-
from odoo import fields, models, api

class RecursoCinematograficos(models.Model):
    _name = "recurso.cinematografico"  # recomendado usar puntos, no guines bajos (odoo 14, almenos)
 

    name = fields.Char(string='Recurso')
    descripcion = fields.Char(string='Descripcion')
    precio = fields.Float(string='Precio')
    contacto_id = fields.Many2one(
        comodel_name='res.partner', 
        domain="[('is_company', '=', False)]"
    )
    
    imagen = fields.Binary(string = 'Imagen', attachment=True) # Tambien se puede usar para imagenes ademas de image.mixin
