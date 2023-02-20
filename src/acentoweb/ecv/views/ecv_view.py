# -*- coding: utf-8 -*-

from acentoweb.ecv import _
from Products.Five.browser import BrowserView
import datetime;
from tempfile import TemporaryFile
from zope.interface.interfaces import IMethod

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile



#def get_ecv_fields(item):
#    ecv_fields = ''
#    for field in [ {'name': 'translation_en', 'desc': 'Translation equivalents in English' } ]:
#        ecv_fields = ecv_fields + """<{title} DESCRIPTION=\"{description}\" LANG_REF=\"eng\">{title}</{title}></CV_ENTRY_ML>\n""".format( description=field["desc"], title=field["name"])
#    return ecv_fields



class EcvDisplay(BrowserView):

    def __call__(self):
        """Returns the ecv content,
        """
        #We could put get items here, might save a few milliseconds :)
        #return self.index()
        request = self.request
        context = self.context


        CVE = """<?xml version=\"1.0\" ?>
<CV_RESOURCE AUTHOR=\"\" DATE=\"%s\" VERSION=\"0.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://www.mpi.nl/tools/elan/EAFv2.8.xsd\">\n
<LANGUAGE LANG_DEF=\"http://cdb.iso.org/lg/CDB-00138502-001\" LANG_ID=\"eng\" LANG_LABEL=\"English (eng)\"/>
<CONTROLLED_VOCABULARY CV_ID=\"ASL Signbank lexicon\">
<DESCRIPTION LANG_REF=\"eng\">The main dataset in the ASL Signbank</DESCRIPTION>\n""" % datetime.datetime.now().isoformat()

        for item in self.get_items():
            #If we add ecv_id to index, we can skip getObject for next line
            obj = item.getObject()
            eco_id = obj.cve_id.replace("\"", "\'")
            eco_description = obj.Description().replace("\"", "\'")
            eco_title = obj.Title().replace("\"", "\'")

            CVE = CVE + """<CV_ENTRY_ML CVE_ID=\"{id}\" EXT_REF=\"signbank-ecv\"><CVE_VALUE DESCRIPTION=\"{description}\" LANG_REF=\"eng\">{title}</CVE_VALUE></CV_ENTRY_ML>\n"""   .format(id =eco_id, description=eco_description, title=eco_title)

        CVE = CVE + """</CONTROLLED_VOCABULARY>
<EXTERNAL_REF EXT_REF_ID=\"signbank-ecv\" TYPE=\"resource_url\"
 VALUE=\"https://aslsignbank.haskins.yale.edu//dictionary/gloss/\"/>
</CV_RESOURCE>"""

        # Add header

        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/exml")
        self.request.RESPONSE.setHeader("Content-type", "text/xml")


        #return xml

        return CVE


    def get_items(self):
        return self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss"], sort_on="sortable_title", sort_order="ascending")



class EcvView(BrowserView):
    #def __init__(self, context, request):
    #    super(EcvView, self).__init__(context, request)

    def __call__(self):
        """Returns the csv/ecv file,
        """
        #We could put get items here, might save a few milliseconds :)
        #return self.index()
        request = self.request
        context = self.context

        CVE = """<?xml version=\"1.0\" ?>
<CV_RESOURCE AUTHOR=\"\" DATE=\"%s\" VERSION=\"0.2\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://www.mpi.nl/tools/elan/EAFv2.8.xsd\">\n
<LANGUAGE LANG_DEF=\"http://cdb.iso.org/lg/CDB-00138502-001\" LANG_ID=\"eng\" LANG_LABEL=\"English (eng)\"/>
<CONTROLLED_VOCABULARY CV_ID=\"ASL Signbank lexicon\">
<DESCRIPTION LANG_REF=\"eng\">The main dataset in the ASL Signbank</DESCRIPTION>\n""" % datetime.datetime.now().isoformat()

        for item in self.get_items():
            #If we add ecv_id to index, we can skip getObject for next line
            obj = item.getObject()
            eco_id = obj.cve_id.replace("\"", "\'")



        CVE = CVE + """</CONTROLLED_VOCABULARY>
<EXTERNAL_REF EXT_REF_ID=\"signbank-ecv\" TYPE=\"resource_url\"
 VALUE=\"https://aslsignbank.haskins.yale.edu//dictionary/gloss/\"/>
</CV_RESOURCE>"""


        # Add header

        dataLen = len(CVE)
        R = self.request.RESPONSE
        R.setHeader("Content-Length", dataLen)
        R.setHeader("Content-Type", "text/ecv")
        R.setHeader("Content-Disposition", "attachment; filename=%s.ecv" % self.context.getId())

        #return and downloads the file
        return CVE

    def get_items(self):
        return self.context.portal_catalog(portal_type=["CNLSE Glosa", "cnlse_glosa", "cnlse_gloss" ], sort_on="sortable_title", sort_order="ascending")
