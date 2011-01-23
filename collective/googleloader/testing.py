from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

class GoogleLoader(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.googleloader
        self.loadZCML(package=collective.googleloader)

        # Install product and call its initialize() function
        z2.installProduct(app, 'collective.googleloader')

        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.googleloader:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.googleloader')

        # Note: Again, you can skip this if my.product is not a Zope 2-
        # style product

MY_PRODUCT_FIXTURE = GoogleLoader()
MY_PRODUCT_INTEGRATION_TESTING = IntegrationTesting(bases=(MY_PRODUCT_FIXTURE,), name="MyProduct:Integration")
