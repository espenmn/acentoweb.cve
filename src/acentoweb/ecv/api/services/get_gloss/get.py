# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

from zope.schema import getFieldsInOrder

@implementer(IExpandableElement)
@adapter(Interface, Interface)
class GetGloss(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        uid = self.request.get("uid")

        #if 'id' in request.args:
        #    uid = self.request.get('id')
        #else:
        #    uid = None

        result = {
            'get_gloss': {
                '@id': '{}/@get_gloss'.format(
                    self.context.absolute_url(),
                ),
            },
        }

        # Get gloss by ID
        # You can also call this directly on the content item without id (uid)
        # /path/to/gloss/@get_gloss
        if uid:
            obj = api.content.get(UID=uid)
        else:
            obj = api.content.get(path=self.context.absolute_url_path())

        items = {}
        if obj and obj.portal_type == "cnlse_gloss"  :
            items['title'] = obj.Title()
            items['description'] = obj.Description()

            # Looping over all the fields / values
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
                        if str(type(ref_value)) ==  "<class 'z3c.relationfield.relation.RelationValue'>":
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

                items[key] = value


            result['get_gloss']['items'] = items
            return result

        # If no content was found, we should probably return some
        # error message or empty list
        result['get_gloss']['items'] = items
        return result


class GetGlossGet(Service):

    def reply(self):
        service_factory = GetGloss(self.context, self.request)
        return service_factory(expand=True)['get_gloss']
