{
    'name' : 'Module Custom Purchase',
    'version' : '14.0.1.0.0',
    'category' : 'purchase',
    'summary' : 'Purchase Custom',
    'desription' : """
        Purchase Custom
    """,
    'website' : '',
    'author' : 'Among Us',
    'depends' : ['web', 'base', 'product'],
    'data' : [
        'security/ir.model.access.csv',
        'views/saya_purchase_view.xml',
        'views/saya_purchase_action.xml',
        'views/saya_purchase_menuitem.xml',
        'views/saya_purchase_sequence.xml',
        'views/saya_purchase_cron.xml',
        'reports/saya_report_pdf.xml'


    ],
    'installable' : True,
    'license' : 'OEEL-1',


}