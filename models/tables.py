# -*- coding: utf-8 -*-
from datetime import datetime

def get_first_name():
	name = 'Nobody'
	if auth.user:
		name = auth.user.first_name
	return name

CATEGORY = ['Car', 'Bike', 'Book','Music', 'Outdoors', 'For the House', 'Misc.']

db.define_table('bboard',
				Field('name'),
				Field('user_id',db.auth_user),
				Field('phone'),
				Field('email'),
				Field('category'),
				Field('date_posted','datetime'),
				Field('bbmessage','text'),
				)

#This allows you to rename bbmessage
db.bboard.id.readable = False
db.bboard.bbmessage.label = 'Message'
db.bboard.name.default = get_first_name
db.bboard.date_posted.default = datetime.utcnow()
db.bboard.name.writable = False
db.bboard.date_posted.writable = False
db.bboard.user_id.default = auth.user_id
db.bboard.user_id.writable = db.bboard.user_id.readable = False
db.bboard.email.requires = IS_EMAIL()
db.bboard.phone.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',
         error_message='use format (###)###-####')
db.bboard.category.requires = IS_IN_SET(CATEGORY)
db.bboard.category.default = 'Misc.'
db.bboard.category.required = True