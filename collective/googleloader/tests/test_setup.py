import unittest2 as unittest

from collective.googleloader import testing

class TestSetup(unittest.TestCase):

    layer = testing.MY_PRODUCT_INTEGRATION_TESTING

    def test_javascripts(self):
        portal = self.layer['portal']
        jsregistry = portal.portal_javascripts
        resources = jsregistry.resources
        self.failUnless(resources[0].getId().startswith('https://www.google.com/jsapi?key='))
        self.failUnless(resources[1].getId()=='googleloader.js')
        googleload = portal.restrictedTraverse('googleloader.js')()
        self.failUnless(not bool(googleload))
