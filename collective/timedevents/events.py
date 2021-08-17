"""
    Time based events

    http://www.twinapex.com

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__copyright__ = "Copyright 2008 Twinapex Research"
__license__ = "GPL"
__docformat__ = "epytext"


# Python imports
import os
import logging

# Zope imports
from zope.interface import implementer
from DateTime import DateTime
from zope.component import adapter

# Local imports
from collective.timedevents.interfaces import (
    ITickEvent,
    IIntervalTicksGenericEvent,
    IIntervalTicks15Event,
    IIntervalTicksHourlyEvent,
    IIntervalTicksDailyEvent,
    IIntervalTicksWeeklyEvent,
    IIntervalTicksMonthlyEvent,
)

LOGGING_LEVEL = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
}.get(os.environ.get("TICK_LOGGER_LEVEL", "INFO").upper())


@implementer(ITickEvent)
class TickEvent(object):
    """This class implements the ITickEvent interface."""

    def __init__(self, date_time, next_tick):
        self.date_time = DateTime(date_time)
        self.next_tick = DateTime(next_tick)


@adapter(ITickEvent)
def tick_logger(tick_event):
    """This function is a handler for the ITickEvent. Its purpose is to log all
    ticks.
    """

    l = logging.getLogger("collective.timedevents")
    l.log(LOGGING_LEVEL, "(%s) TICK detected." % tick_event.date_time.ISO())


@implementer(IIntervalTicksGenericEvent)
class IntervalTicksGenericEvent(object):
    """
    IntervalTicks generic event
    """

    def __init__(self, context):
        self.context = context


@implementer(IIntervalTicks15Event)
class IntervalTicks15Event(IntervalTicksGenericEvent):
    """
    An Event that will be fired every 15 minutes from a cronjob

    """


@implementer(IIntervalTicksHourlyEvent)
class IntervalTicksHourlyEvent(IntervalTicksGenericEvent):
    """
    An Event that will be fired hourly from a cronjob

    """


@implementer(IIntervalTicksDailyEvent)
class IntervalTicksDailyEvent(IntervalTicksGenericEvent):
    """
    An Event that will be fired daily from a cronjob

    """


@implementer(IIntervalTicksWeeklyEvent)
class IntervalTicksWeeklyEvent(IntervalTicksGenericEvent):
    """
    An Event that will be fired weekly from a cronjob

    """


@implementer(IIntervalTicksMonthlyEvent)
class IntervalTicksMonthlyEvent(IntervalTicksGenericEvent):
    """
    An Event that will be fired monthly from a cronjob

    """
