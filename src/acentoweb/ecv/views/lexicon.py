# -*- coding: utf-8 -*-

from acentoweb.ecv import _
from Products.Five.browser import BrowserView
import datetime;
from tempfile import TemporaryFile
#from zope.interface.interfaces import IMethod
from zope.schema import getFieldsInOrder
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility






class LexiconDisplay(BrowserView):

    def __call__(self):
        """Returns the ecv content,
        """
        #We could put get items here, might save a few milliseconds :)
        #return self.index()
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

            #import pdb; pdb.set_trace()


            CVE = CVE + """
            <entry id="{id}">
            <form>{title}</form>
                <sense>
                   <definition>{description}</definition>
""".format(id=eco_id, description=eco_description, title=eco_title)

            for key, value in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
                value = getattr(getattr(obj, key), 'output', getattr(obj, key))

                ## what shall we do with empty values?
                if value == None or value == []:
                    value = ""

                # Alternatively, just skip it completely if not present
                #if value != None and value != []::
                CVE = CVE + """<{key}>{value}</{key}>""".format(value=value, key=key)

        CVE = CVE + """</sense>
    </entry>
</lexicon>"""


        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/exml")
        self.request.RESPONSE.setHeader("Content-type", "text/xml")


        #return xml

        return CVE


    def get_items(self):
        return self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss"], sort_on="sortable_title", sort_order="ascending")







class LexiconView(BrowserView):

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
                    <pos>{semantic}</pos>
                    <gloss>gloss here</gloss>
                    <definition>{description}</definition>
                    <gloss_id_en>{gloss_id_en}</gloss_id_en>
                    <synonyms>{synonyms}</synonyms>
                </sense>
            </entry>
""".format(id=eco_id, description=eco_description, title=eco_title, semantic=obj.semantic or None, gloss_id_en=obj.gloss_id_en, synonyms = obj.synonyms)

        CVE = CVE + """</lexicon>"""

        # Add header

        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/ecv")
        R.setHeader("Content-Disposition", "attachment; filename=%s.lexicon" % self.context.getId())

        #return and downloads the file
        return CVE



    def get_items(self):
        return self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss"], sort_on="sortable_title", sort_order="ascending")
