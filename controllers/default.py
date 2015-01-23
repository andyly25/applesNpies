# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    This appears when you go to bboard/default/index
    """
    response.flash = T("yoHohoOH!")
    # generate an index of the posts (grabs all records)
    posts = db().select(db.bboard.ALL)

    return dict(posts = posts)

@auth.requires_login()
def add():
    """Add a post"""
    form = SQLFORM(db.bboard)
    if form.process().accepted:
        # successful processing
        # session.flash = T('Added')
        redirect(URL('default','index2'))
    return dict(form=form)

def returnBack():
    redirect(URL('default','index2'))

def view():
    """view a post"""
    # p = db(db.bboard.id == request.args(0)).select().first()
    p = db.bboard(request.args(0)) or redirect(URL('default','index2'))
    url = URL('download')
    form = SQLFORM(db.bboard, record = p, readonly = True, upload=url)
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
def edit():
    """view a post"""
    # p = db(db.bboard.id == request.args(0)).select().first()
    p = db.bboard(request.args(0)) or redirect(URL('default','index2'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized')
        redirect(URL('default', 'index2'))
    form = SQLFORM(db.bboard, record = p)
    if form.process().accepted:
        session.flash = T('Updated')
        # redirect(URL('default','index2',args=[p.id]))
        redirect(URL('default','view',args=[p.id]))
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
@auth.requires_signature()
def delete():
    """Deletes a post"""
    p = db.bboard(request.args(0)) or redirect(URL('default','index2'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized')
        redirect(URL('default', 'index2'))
    db(db.bboard.id == p.id).delete()
    redirect(URL('default', 'index2'))

def index2():
    """Better index."""
    # Let's get all data
    q = db.bboard
    url = URL('download')

    def generate_del_button(row):
        #If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class = 'btn', _href=URL('default','delete',args=[row.id],user_signature = True))
        return b

    def generate_edit_button(row):
        #If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class = 'btn', _href=URL('default','edit',args=[row.id]))
        return b

    def shorten_post (row):
        """ gives short description of entries"""
        return row.bbmessage[:10] + '...'
    
    # creates extra buttons
    links = []
    if len(request.args)==0:
        # we are in the main index
        links.append(dict(header = 'Post', body = shorten_post))
        db.bboard.bbmessage.readable = False
    links.append(dict(header= '',body = generate_edit_button))
    links.append(dict(header= '', body = generate_del_button))


    form = SQLFORM.grid(q,
        fields = [db.bboard.user_id, db.bboard.date_posted,db.bboard.title,
        db.bboard.category, db.bboard.bbmessage],
        editable = False, deletable = False,
        links=links, 
        paginate = 5,
        csv = False,
        upload=url
        )
    return dict(form = form)

def download():
    return response.download(request, db)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
