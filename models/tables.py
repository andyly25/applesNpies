# -*- coding: utf-8 -*-
from datetime import datetime

def get_first_name():
	name = 'Nobody'
	if auth.user:
		name = auth.user.first_name
	return name

CATEGORY = ['Car', 'Bike', 'Book','Music', 'Outdoors', 'For the House', 'Misc.']
# SOLD = ['Available', 'Sold']

db.define_table('bboard',
				Field('title'),
				Field('name'),
				Field('user_id',db.auth_user),
				Field('phone'),
				Field('email'),
			   	Field('picture', 'upload', uploadfield = 'picture_file'),
			   	Field('picture_file', 'blob'),
				Field('category'),
				Field('price'),
				Field('sold', 'boolean', default=False),
				Field('date_posted','datetime'),
				Field('bbmessage','text'),
				)

#This allows you to rename bbmessage
# db.bboard.sold.writable = False
# db.bboard.sold.default = False
# db.bboard.sold.requires = IS_IN_SET(SOLD)
db.bboard.sold.label = 'Check if item is sold'

# if db.bboard.sold == False:
#     db.bboard.sold.label = 'The item is: Available'
# else:
#     db.bboard.sold.label= 'The item is: Sold'

db.bboard.price.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The price should be in the range 0..100000')
db.bboard.id.readable = False
db.bboard.bbmessage.label = 'Message'
db.bboard.name.default = get_first_name
db.bboard.date_posted.default = datetime.utcnow()
db.bboard.name.writable = False
db.bboard.date_posted.writable = False
db.bboard.user_id.default = auth.user_id
db.bboard.user_id.writable = db.bboard.user_id.readable = False
db.bboard.email.requires = IS_EMAIL(error_message='invalid email!')
db.bboard.phone.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',
         error_message='use format (###)###-####')
db.bboard.category.requires = IS_IN_SET(CATEGORY)
db.bboard.category.default = 'Misc.'
db.bboard.category.required = True