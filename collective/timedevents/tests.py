"""
    Unit testing for collective.timedevents

    http://www.twinapex.com

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__copyright__ = "Copyright 2008 Twinapex Research"
__license__ = "GPL"
__docformat__ = "epytext"

from AccessControl import Unauthorized
from zope import component
from AccessControl.ImplPython import ZopeSecurityPolicy
from AccessControl.SecurityManager import setSecurityPolicy
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import TestCase

from collective.timedevents.interfaces import (
    ITickEvent,
    IIntervalTicks15Event,
    IIntervalTicksHourlyEvent,
    IIntervalTicksDailyEvent,
    IIntervalTicksWeeklyEvent,
    IIntervalTicksMonthlyEvent,
)


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.timedevents

        self.loadZCML(package=collective.timedevents)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ["Manager"])


FIXTURE = Fixture()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="collective.timedevents:Functional"
)


INTERVALVIEWS = [
    ("@@tick_fifteen", IIntervalTicks15Event),
    ("@@tick_hourly", IIntervalTicksHourlyEvent),
    ("@@tick_daily", IIntervalTicksDailyEvent),
    ("@@tick_weekly", IIntervalTicksWeeklyEvent),
    ("@@tick_monthly", IIntervalTicksMonthlyEvent),
]


class TickTestCase(TestCase):
    """Test ticking services

    TODO: Add test for next/last tick code.
    """

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        # Set verbose security policy, making debugging Unauthorized
        # exceptions great deal easier in unit tests
        setSecurityPolicy(ZopeSecurityPolicy(verbose=True))
        self.portal = self.layer["portal"]

    def test_url(self):
        """Test that the tick view URL is exposed properly."""
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal = self.portal

        view = portal.restrictedTraverse("@@tick")
        view()

    def test_urls(self):
        """Test that the tick view URL is exposed properly."""
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        for v in INTERVALVIEWS:
            view = self.portal.restrictedTraverse(v[0])
            view()

    def test_security(self):
        """Check that only admin can execute tick."""
        setRoles(self.portal, TEST_USER_ID, [])
        try:
            self.portal.restrictedTraverse("@@tick")
            raise AssertionError("Anonymous could tick")
        except Unauthorized:
            pass

    def test_security_intervals(self):
        """Check that only admin can execute tick interval views."""
        setRoles(self.portal, TEST_USER_ID, [])
        for v in INTERVALVIEWS:
            try:
                self.portal.restrictedTraverse(v[0])
                raise AssertionError("Anonymous could tick: " + v[0])
            except Unauthorized:
                pass

    def test_subscription(self):
        """Test that the event subscriber receives a tick."""

        # global ugly variables work fow now
        global success
        success = False

        def my_tick(event):
            global success
            success = True

        component.getSiteManager().registerHandler(my_tick, [ITickEvent])

        # First
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        view = self.portal.restrictedTraverse("@@tick")
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
        """Test that the event subscriber receives a tick."""

        # global ugly variables work fow now
        global success
        success = False

        def my_tick(event):
            global success
            success = True

        component.getSiteManager().registerHandler(my_tick, [v[1]])

        # First
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        view = self.portal.restrictedTraverse(v[0])
        view()

        self.assertEqual(success, True)

        # All ticks have effect. Interval is handled by the external
        # trigger (cron or clockserver)
        success = False
        view()
        self.assertEqual(success, True)

        # Must unregister, otherwise piclking errors - ZODB tries to store this entry?
        component.getSiteManager().unregisterHandler(my_tick, [v[1]])
