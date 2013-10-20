"""
    Unit testing for collective.timedevents

    http://www.twinapex.com

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__copyright__ = "Copyright 2008 Twinapex Research"
__license__ = "GPL"
__docformat__ = "epytext"

import unittest

from AccessControl import Unauthorized
from Products.Five import zcml
from zope import component
from zope.app.testing import placelesssetup
from Products.Five import fiveconfigure
from AccessControl.ImplPython import ZopeSecurityPolicy
from AccessControl.SecurityManager import setSecurityPolicy

from interfaces import (ITickEvent,
                        IIntervalTicks15Event,
                        IIntervalTicksHourlyEvent,
                        IIntervalTicksDailyEvent,
                        IIntervalTicksWeeklyEvent,
                        IIntervalTicksMonthlyEvent)
from Products.PloneTestCase import PloneTestCase as ptc

from Products.PloneTestCase.layer import onsetup

@onsetup
def setup():
    fiveconfigure.debug_mode = True
    import collective.timedevents
    zcml.load_config('configure.zcml', collective.timedevents)
    fiveconfigure.debug_mode = False

# The order here is important.
placelesssetup.setUp()
setup()
ptc.setupPloneSite(products=["collective.timedevents"])

INTERVALVIEWS = [
         ('@@tick_fifteen', IIntervalTicks15Event),
         ('@@tick_hourly', IIntervalTicksHourlyEvent),
         ('@@tick_daily', IIntervalTicksDailyEvent),
         ('@@tick_weekly', IIntervalTicksWeeklyEvent),
         ('@@tick_monthly', IIntervalTicksMonthlyEvent),
        ]

class TickTestCase(ptc.PloneTestCase):
    """ Test ticking services

    TODO: Add test for next/last tick code.
    """

    def afterSetUp(self):
        # Set verbose security policy, making debugging Unauthorized
        # exceptions great deal easier in unit tests
        setSecurityPolicy(ZopeSecurityPolicy(verbose=True))

    def tearDown(self):
        ptc.PloneTestCase.tearDown(self)

    def test_url(self):
        """ Test that the tick view URL is exposed properly. """
        self.loginAsPortalOwner()
        portal = self.portal

        view = portal.restrictedTraverse('@@tick')
        view()

    def test_urls(self):
        """ Test that the tick view URL is exposed properly. """
        self.loginAsPortalOwner()
        portal = self.portal

        for v in INTERVALVIEWS:
            view = portal.restrictedTraverse(v[0])
            view()

    def test_security(self):
        """ Check that only admin can execute tick. """
        try:
            portal = self.portal
            view = portal.restrictedTraverse('@@tick')
            raise AssertionError("Anonymous could tick")
        except Unauthorized:
            pass

    def test_security_intervals(self):
        """ Check that only admin can execute tick. """
        for v in INTERVALVIEWS:
            try:
                portal = self.portal
                view = portal.restrictedTraverse(v[0])
                raise AssertionError("Anonymous could tick")
            except Unauthorized:
                pass

    def test_subscription(self):
        """ Test that the event subscriber receives a tick. """

        # global ugly variables work fow now
        global success
        success = False

        def my_tick(event):
            global success
            success = True

        component.getSiteManager().registerHandler(my_tick, [ITickEvent])

        # First
        self.loginAsPortalOwner()
        portal = self.portal
        view = portal.restrictedTraverse('@@tick')
        view()

        self.assertEqual(success, True)

        # Subsequent ticks should have no effect until interval has passed
        success = False
        view()
        self.assertEqual(success, False)

        # Must unregister, otherwise piclking errors - ZODB tries to store this entry?
        component.getSiteManager().unregisterHandler(my_tick, [ITickEvent])

    def test_subscriptions(self):
        for v in INTERVALVIEWS:
            self.helper_test_sub(v)

    def helper_test_sub(self, v):
        """ Test that the event subscriber receives a tick. """

        # global ugly variables work fow now
        global success
        success = False

        def my_tick(event):
            global success
            success = True

        component.getSiteManager().registerHandler(my_tick, [v[1]])

        # First
        self.loginAsPortalOwner()
        portal = self.portal
        view = portal.restrictedTraverse(v[0])
        view()

        self.assertEqual(success, True)

        # All ticks have effect. Interval is handled by the external
        # trigger (cron or clockserver)
        success = False
        view()
        self.assertEqual(success, True)

        # Must unregister, otherwise piclking errors - ZODB tries to store this entry?
        component.getSiteManager().unregisterHandler(my_tick, [v[1]])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TickTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
