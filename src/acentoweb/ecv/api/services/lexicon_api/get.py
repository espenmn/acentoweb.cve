# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class LexiconApi(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        result = {
            'lexicon': {
                #'@id': '{}/@lexicon_api'.format(
                #    self.context.absolute_url(),
                #),
            },
        }
        #if not expand:
        #    return result

        # === Get content and return lexicon as json ===

        #try:
        #    subjects = self.context.Subject()
        #except:
        #    subjects = []
        query = {}
        query['portal_type'] =  "cnlse_gloss"
        #query['Subject'] = {
        #    'query': subjects,
        #    'operator': 'or',
        #}
        brains = api.content.find(**query)
        items = []
        for brain in brains:
            # obj = brain.getObject()
            # parent = obj.aq_inner.aq_parent
            items.append({
                'title': brain.Title,
                'cve_id': brain.id,
                'description': brain.Description,
                #'@id': brain.getURL(),
            })
        result['lexicon']['items'] = items
        return result


class LexiconApiGet(Service):

    def reply(self):
        service_factory = LexiconApi(self.context, self.request)
        return service_factory(expand=True)['lexicon_api']
