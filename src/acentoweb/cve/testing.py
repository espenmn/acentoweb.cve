# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import acentoweb.cve


class AcentowebCveLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=acentoweb.cve)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'acentoweb.cve:default')


ACENTOWEB_CVE_FIXTURE = AcentowebCveLayer()


ACENTOWEB_CVE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ACENTOWEB_CVE_FIXTURE,),
    name='AcentowebCveLayer:IntegrationTesting',
)


ACENTOWEB_CVE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ACENTOWEB_CVE_FIXTURE,),
    name='AcentowebCveLayer:FunctionalTesting',
)


ACENTOWEB_CVE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ACENTOWEB_CVE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='AcentowebCveLayer:AcceptanceTesting',
)
