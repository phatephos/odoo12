import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('baoshunkeji.com', port=8069)

# Check available databases
print(odoo.db.list())

# Login
odoo.login('tender_db', 'admin', 'OeN4Bj0^')

# Current user
user = odoo.env.user
user_data = odoo.execute('res.users', 'read', [user.id])
print(user_data)
partner1 = odoo.env['crm_c.partner']
partner_ids = odoo.env['crm_c.partner'].search([],limit=5)
for partner in partner1.browse(partner_ids):
        print(partner.name)
