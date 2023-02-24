# -*- coding: utf-8 -*-

from acentoweb.ecv import _
from Products.Five.browser import BrowserView
from tempfile import TemporaryFile
from zope.schema import getFieldsInOrder

import datetime


#from zope.interface.interfaces import IMethod
#from plone.dexterity.interfaces import IDexterityFTI
#from zope.component import getUtility

def getCVE(self):
    """Returns the ecv content,
    """
    request = self.request
    context = self.context

    CVE = """<?xml version="1.0" encoding="UTF-8"?>
<lexicon id="Demo Lexicon">"""

    for item in self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss"], sort_on="sortable_title", sort_order="ascending"):
        #If we add ecv_id to index, we can skip getObject for next line
        obj = item.getObject()
        eco_id = obj.cve_id.replace("\"", "\'")
        eco_description = obj.Description().replace("\"", "\'")
        eco_title = obj.Title().replace("\"", "\'")

        CVE = CVE + """
        <entry id="{id}">
        <form>{title}</form>
            <sense>
               <definition>{description}</definition>""".format(id=eco_id, description=eco_description, title=eco_title)

        ## Looping over all the fields / values
        for key, value in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
            value = getattr(getattr(obj, key), 'output', getattr(obj, key))

            ## what shall we do with empty/not existing values?
            # If value does not exist, just skip it
            if value == None or value == []:
                value = ""

            # If value is a list, loop through it
            if type(value)() == []:
                listvalues = ""
                for ref_value in value:
                    ## Do do: make a proper check for class
                    if str(type(ref_value)) ==  "<class 'z3c.relationfield.relation.RelationValue'>":
                        ## What do we want to show here. Link to other objects ?
                        ## Other objects IDs maybe ?
                        ## Or maybe {title, id, url}
                        listvalues += ref_value.to_object.title
                value=listvalues

            ##If it is an image or file
            if value.__class__.__name__ ==  "NamedBlobImage":
                #If we want to download images, we probably need to redirect later or use a zip
                value = "{url}/@@images/{key}".format(url = obj.absolute_url(), key=key)

            if value.__class__.__name__ ==  "NamedBlobFile":
                #Returns the download link for the video
                value = "{url}/view/++widget++form.widgets.{key}/@@download/{filename}".format(url = obj.absolute_url(), key=key, filename=value.filename)

            if value == None or value == []:
                value = ""

            # Alternatively, just skip it completely if not present
            #if value != None and value != []::
            CVE = CVE + """<{key}>{value}</{key}>""".format(value=value, key=key)

        CVE = CVE + """</sense></entry>"""
    CVE = CVE + """</lexicon>"""
    return CVE


class LexiconDisplay(BrowserView):

    def __call__(self):
        """Returns the ecv content,
        """
        #We could put get items here, might save a few milliseconds :)
        #return self.index()
        request = self.request
        context = self.context

        CVE = getCVE(self)


        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/exml")
        self.request.RESPONSE.setHeader("Content-type", "text/xml")

        #return xml
        return CVE


class LexiconView(BrowserView):

    def __call__(self):
        """Returns the ecv content,
        """
        #We could put get items here, might save a few milliseconds :)
        #return self.index()
        request = self.request
        context = self.context

        CVE = getCVE(self)

        # Add header

        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/ecv")
        R.setHeader("Content-Disposition", "attachment; filename=%s.lexicon" % self.context.getId())

        #return and downloads the file
        return CVE



#def get_items(self):
#    return self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss"], sort_on="sortable_title", sort_order="ascending")
