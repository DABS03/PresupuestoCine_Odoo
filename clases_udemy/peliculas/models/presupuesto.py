# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

# Cada clase es un modelo (tabla en la base de datos)
class Presupuesto(models.Model):
    _name = "presupuesto"
    _description = "Presupuesto de Películas"
    _inherit = ['image.mixin'] # Modelo para imagenes

    @api.depends('detalle_ids') #para que con cada cambio se ejecute _compute_total al modifica de detalle_ids
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.detalle_ids:
                sub_total += linea.importe
            record.base = sub_total
            record.impuestos = record.base * 0.19
            record.total = record.base * 1.19

    name = fields.Char(string='Pelicula') # name tiene caracteristica especiales
    clasificacion = fields.Selection(selection=[
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    ], string='Clasificacion')

    dsc_clasificacion = fields.Char(string='Descripcion clasificacion')

    fch_estreno= fields.Date( string='Fecha de estreno')
    puntuacion = fields.Integer( string='Puntuacion', related='puntuacion2' )
    puntuacion2 = fields.Integer( string='Puntuacion2' )
    active = fields.Boolean( string='Activo', default=True) #caracteristica especiales
    
    
    director_id = fields.Many2one ( #muchos (peliculas) a uno (director)
        comodel_name='res.partner',
        string='Director'
    )

    categoria_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',
        default=lambda self: self.env.ref('peliculas.category_director')
    )

    actor_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Actores',

    )

    categoria_actor_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Actor',
        default=lambda self: self.env.ref('peliculas.category_actor')
    )

    opinion = fields.Html(string='Opinion')
    detalle_ids = fields.One2many( # una cabecera puede tener muchos detalles
        comodel_name='presupuesto.detalle', 
        inverse_name='presupuesto_id', # nombre del campo que relaciona el detalle con la cabecera
        string='Detalles',
    )

    campos_ocultos = fields.Boolean(string='Ver Campos ocultos', default=False)

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )

    genero_ids = fields.Many2many(
        comodel_name='genero',
        string='Genero'
    )

    vista_general = fields.Text(string='Descripcion')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Version libro')
    libro = fields.Binary(string='Libro')
    libro_filename = fields.Char(string='Nombre del libro')

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
    
    ], default='borrador', string='Estados', copy=False)

    fch_aprobado = fields.Date(string='Fecha de aprobacion', copy=False)
    num_presupuesto = fields.Char(string = 'Numero de presupuesto', copy=False)
    fch_creacion = fields.Datetime(string='Fecha de creación', copy=False, default=lambda self: fields.Datetime.now())


    terminos = fields.Text(string='Terminos y condiciones')
    base = fields.Monetary(
        string='Base imponible',
        compute='_compute_total'
    )
    
    impuestos = fields.Monetary(
        string='Impuestos',
        compute='_compute_total'
    )
    
    total = fields.Monetary(
        string='Total',
        compute='_compute_total'
    )

    def aprobar_presupuesto(self):
        logger.info('\n********************* Presupuesto aprobado *********************\n')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.info('\n********************* Presupuesto cancelado *********************\n')
        self.state = 'cancelado'

    def unlink(self):
        logger.info('\n******************* Se disparó unlink *********************\n')
        for record in self:
            if record.state != 'cancelado':
                raise UserError('No se puede eliminar un presupuesto que no está en estado cancelado')
        return super(Presupuesto, self).unlink()
        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence_obj = self.env['ir.sequence']
            correlativo = sequence_obj.next_by_code('secuencia.presupuesto.pelicula')
            vals['num_presupuesto'] = correlativo
            logger.info('\n******************* CREATE Variables: {0}.'.format(vals))
        return super(Presupuesto, self).create(vals_list)
    
    def write(self, variables):
        logger.info('\n******************* WRITE Variables: {0}.'.format(variables))
    
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        logger.info('\n******************* Copiando presupuesto *********************\n')
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        default['puntuacion2'] =  1
        return super(Presupuesto, self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        logger.info('\n******************* Se disparó _onchange_clasificacion')
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = 'General'
            elif self.clasificacion == 'PG':
                self.dsc_clasificacion = 'Se recomienda compañia de un adulto'
            elif self.clasificacion == 'PG-13':
                self.dsc_clasificacion = 'Para mayores de 13 años'
            elif self.clasificacion == 'R':
                self.dsc_clasificacion = 'Para mayores de 18 años'
            elif self.clasificacion == 'NC-17':
                self.dsc_clasificacion = 'Para mayores de 18 años'
        else:
            self.dsc_clasificacion = False

        
class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"
    _description = "Detalle de Presupuesto de Películas"

    presupuesto_id = fields.Many2one( #Muchos detalles pertenecen a un presupuesto
        comodel_name='presupuesto', #relacion con el primer modelo: presupuesto
        string='Presupuesto',
    )

    name = fields.Many2one(
        comodel_name='recurso.cinematografico',
        string = 'Recurso',
    )

    descripcion = fields.Char(string='Descripcion', related='name.descripcion') # Relacionado con recurso_cinematografico
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        related='name.contacto_id'
    )
    imagen = fields.Binary(string='Imagen', related='name.imagen')
    cantidad = fields.Integer(string='Cantidad', default=1.0)
    precio = fields.Float(string='Precio', digits='Product Price')
    importe = fields.Monetary(string='Importe')
    
    #siempre debe llamarse currency_id
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        related='presupuesto_id.currency_id'
        )

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio

    @api.onchange('cantidad', 'precio')
    def _onchange_cantidad_precio(self):
        if self.cantidad and self.precio:
            self.importe = self.cantidad * self.precio

