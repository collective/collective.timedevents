"""
    Exposed URLs for sending time based events.

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__copyright__ = "Copyright 2008 Twinapex Research"
__license__ = "GPL"
__docformat__ = "epytext"


import logging
import time

# Zope imports
from DateTime.DateTime import DateTime
from zope.event import notify
from zope.interface import implementer
from zope.interface import alsoProvides

try:
    from plone.protect.interfaces import IDisableCSRFProtection

    HAS_PROTECT = True
except ImportError:
    HAS_PROTECT = False
from Products.Five.browser import BrowserView
from zope.session.session import SessionData
from zope.session.session import PersistentSessionDataContainer

# Local imports
from collective.timedevents.events import TickEvent
from collective.timedevents.events import (
    IntervalTicks15Event,
    IntervalTicksHourlyEvent,
    IntervalTicksDailyEvent,
    IntervalTicksWeeklyEvent,
    IntervalTicksMonthlyEvent,
)
from collective.timedevents.interfaces import IIntervalTicks

client_id = "collective.timedevents"
package_id = "collective.timedevents"

from collective.timedevents.events import LOGGING_LEVEL

logger = logging.getLogger("collective.timedevents")


class TickData:
    """Persistent information about ticking."""

    def __init__(self, interval):
        self.interval = interval
        self.last_tick = None


# We fake a persistent session using constant client id
sdc = PersistentSessionDataContainer()


class TickTriggerView(BrowserView):
    """View that is called by Zope clock server.

    Clock server pulse calls this view regularly. View check whether we have
    enough interval since the last event burst and calls event handlers.

    Ticking data is kept in Zope persistent session storage,
    using view url as the key.
    """

    # Interval between send tick events in seconds
    interval = 10

    def getTickData(self):
        """Lazily initialize run-time tick data.

        We need to store process shared data somewhere.
        """

        # Make sure persistent data is not cleared between clock pulses
        sdc.timeout = self.interval * 3
        client_id = "tick-data:" + self.context.absolute_url()

        try:
            container = sdc[client_id]
        except KeyError:
            container = sdc[client_id] = SessionData()

        if "interval" not in container:
            # Initialize data
            container["interval"] = self.interval
            container["last_tick"] = None

        return container

    def getInterval(self):
        return self.getTickData()["interval"]

    def setLastTick(self, time):
        self.getTickData()["last_tick"] = time

    def getLastTick(self):
        return self.getTickData()["last_tick"]

    def tick(self):
        """Perform tick event firing when needed."""
        # Check current time.
        current = DateTime()

        # Get lastTick. If it is invalid, set it to the minimum possible value.
        last = self.getLastTick()

        if not isinstance(last, DateTime):
            last = DateTime(0)
        else:
            pass

        # Get interval. Make sure the value used here is no lesser than 0.
        interval = self.getInterval()
        if interval < 0:
            interval = 0

        # If current time less lastTick is equal to or greater than
        # (0.9 * interval) then set lastTick to the current time and
        # execute _notify(). Otherwise do nothing.
        if current.timeTime() - last.timeTime() >= 0.9 * interval:
            self.setLastTick(current)
            notify(
                TickEvent(
                    current,
                    self.getNextTickEstimation(last_tick=current, interval=interval),
                )
            )

    def getNextTickEstimation(self, last_tick=None, interval=None):
        """This method tries to estimate a time when a next tick will occur.
        Then it returns a DateTime object representing that time.
        """
        if last_tick is None:
            last_tick = DateTime(self.getLastTick())

        if interval is None:
            interval = float(self.getInterval())

        # unit conversion - seconds to days (needed by DateTime)
        interval = interval / 86400.0

        # compute a DateTime object for the estimated time
        next_tick_estimation = last_tick + interval

        return next_tick_estimation

    def __call__(self):
        self.tick()
        return "OK"


@implementer(IIntervalTicks)
class IntervalTicksView(BrowserView):
    """Cron-style interval based ticking. A zope clockserver or
    cron-job triggers each of methods below. The timing is handled
    by clockserver or cron, not here.

    For instance, to trigger the hourly event, create a cron-job or
    clockserver setting that goes of every hour, and calls the corresponding
    view by url.
    """

    def fifteenMinutes(self):
        """
        cron job every 15 minutes
        """
        logger.log(LOGGING_LEVEL, "Firing IntervalTicks15Event")
        notify(IntervalTicks15Event(context=self.context))
        if HAS_PROTECT:
            alsoProvides(self.request, IDisableCSRFProtection)
        return "done: %s" % time.strftime("%Y%m%d-%H:%M", time.localtime())

    def hourly(self):
        """
        Hourly cron job
        """
        logger.log(LOGGING_LEVEL, "Firing IntervalTicksHourlyEvent")
        notify(IntervalTicksHourlyEvent(context=self.context))
        if HAS_PROTECT:
            alsoProvides(self.request, IDisableCSRFProtection)
        return "done: %s" % time.strftime("%Y%m%d-%H:%M", time.localtime())

    def daily(self):
        """
        Daily cron job
        """
        logger.log(LOGGING_LEVEL, "Firing IntervalTicksDailyEvent")
        notify(IntervalTicksDailyEvent(context=self.context))
        if HAS_PROTECT:
            alsoProvides(self.request, IDisableCSRFProtection)
        return "done: %s" % time.strftime("%Y%m%d-%H:%M", time.localtime())

    def weekly(self):
        """
        weekly cron job
        """
        logger.log(LOGGING_LEVEL, "Firing IntervalTicksWeeklyEvent")
        notify(IntervalTicksWeeklyEvent(context=self.context))
        if HAS_PROTECT:
            alsoProvides(self.request, IDisableCSRFProtection)
        return "done: %s" % time.strftime("%Y%m%d-%H:%M", time.localtime())

    def monthly(self):
        """
        monthly cron job
        """
        logger.log(LOGGING_LEVEL, "Firing IntervalTicksMonthlyEvent")
        notify(IntervalTicksMonthlyEvent(context=self.context))
        if HAS_PROTECT:
            alsoProvides(self.request, IDisableCSRFProtection)
        return "done: %s" % time.strftime("%Y%m%d-%H:%M", time.localtime())
