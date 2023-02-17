# -*- coding: utf-8 -*-

from acentoweb.ecv import _
from Products.Five.browser import BrowserView

import datetime;
from tempfile import TemporaryFile

from zope.interface.interfaces import IMethod



class Lexicon(BrowserView):

    def __call__(self):
        """Returns the ecv content,
        """
        request = self.request
        context = self.context


        CVE = """<?xml version="1.0" encoding="UTF-8"?>
                <lexicon id="Demo Lexicon">"""

        for item in self.get_items():
            #If we add ecv_id to index, we can skip getObject for next line
            obj = item.getObject()
            eco_id = obj.cve_id.replace("\"", "\'")
            eco_description = obj.Description().replace("\"", "\'")
            eco_title = obj.Title().replace("\"", "\'")

            CVE = CVE + """
            <entry id="{id}">
            <form>{title}</form>
                <sense>
                    <pos>{semantico}</pos>
                    <gloss>gloss here</gloss>
                    <definition>{description}</definition>
                </sense>
            </entry>
            """.format(id=eco_id, description=eco_description, title=eco_title, semantic=obj.semantico)

        CVE = CVE + """</lexicon>"""

        # Add header

        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/ecv")
        R.setHeader("Content-Disposition", "attachment; filename=%s.ecv" % self.context.getId())

        #return and downloads the file
        return CVE



    def get_items(self):
        return self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss"], sort_on="sortable_title", sort_order="ascending")
