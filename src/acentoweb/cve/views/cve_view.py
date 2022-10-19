# -*- coding: utf-8 -*-

from acentoweb.cve import _
from Products.Five.browser import BrowserView

import datetime;

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CveView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('cve_view.pt')

    def __call__(self):
        # Implement your own actions:
        #self.msg = _(u'A small message')
        #We could put items and date here, might save a few milliseconds :)
        return self.index()

    def get_items(self):
        return self.context.portal_catalog(portal_type='CNLSE Glosa', sort_on='sortable_title', sort_order='ascending')

    def now_date(self):
        datetime.datetime.now().isoformat()
