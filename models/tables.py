# -*- coding: utf-8 -*-
db.define_table('bboard',
				Field('name'),
				Field('phone'),
				Field('email'),
				Field('date_posted','datetime'),
				Field('bbmessage','text'),
				)

#This allows you to rename bbmessage
db.bboard.bbmessage.label = 'Message'

