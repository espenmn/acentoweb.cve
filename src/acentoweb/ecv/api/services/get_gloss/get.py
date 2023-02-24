# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class GetGloss(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        import pdb; pdb.set_trace();
        uid = self.request.uid or None
        result = {
            'get_gloss': {
                '@id': '{}/@get_gloss'.format(
                    self.context.absolute_url(),
                ),
            },
        }

        # Get gloss by ID

        plone.api.content.get(UID=uid)
        items = []
        items.append({
                'title': brain.Title,
                'description': brain.Description,
                '@id': brain.getURL(),
            })

        result['lexicon']['items'] = items


class GetGlossGet(Service):

    def reply(self):
        service_factory = GetGloss(self.context, self.request)
        return service_factory(expand=True)['get_gloss']
