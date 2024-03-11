{
  'name': "Real-Estate Management",
  'version': '1.0',
  'depends': ['base'],
  'author': "Sameem Arshad",
  'category': 'Category',
  'description': """
  This is a test module of Real-Estate Management!
  Written for the Odoo Quickstart Tutorial.
  """,
  # data files always loaded at installation
  'data': [
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/estate_menus.xml',
    'views/estate_property_type.xml',
    'views/estate_property_tag.xml',
    'views/estate_property_offer.xml',
  ],
  'installable': True,
  'auto_install': True,
  'application': True,

}