"""
    Time based events

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__copyright__ = "Copyright 2008 Twinapex Research"
__license__ = "GPL"
__docformat__ = "epytext"


from zope.interface import Interface, Attribute


class ITickEvent(Interface):
    """An event signaling a tick (vide the TickingMachine class)."""

    date_time = Attribute("Time of the last tick")
    next_tick = Attribute("Estimated time of the next tick")


class IIntervalTicksGenericEvent(Interface):
    """
    Generic cron event
    """

    context = Attribute("An acquisition context to be passed to the cron handler")


class IIntervalTicks15Event(IIntervalTicksGenericEvent):
    """
    An Event that will be fired every 15 minutes from a cronjob

    """


class IIntervalTicksHourlyEvent(IIntervalTicksGenericEvent):
    """
    An Event that will be fired hourly from a cronjob

    """


class IIntervalTicksDailyEvent(IIntervalTicksGenericEvent):
    """
    An Event that will be fired daily from a cronjob

    """


class IIntervalTicksWeeklyEvent(IIntervalTicksGenericEvent):
    """
    An Event that will be fired weekly from a cronjob

    """


class IIntervalTicksMonthlyEvent(IIntervalTicksGenericEvent):
    """
    An Event that will be fired monthly from a cronjob

    """


class IIntervalTicks(Interface):
    """
    Interface for the cron-style interval notification
    """

    def fifteenMinutes():
        """
        Notify subscribers about the event fifteenMinutes
        """

    def hourly():
        """
        Notify subscribers about the event hourly
        """

    def daily():
        """
        Notify subscribers about the event daily
        """

    def weekly():
        """
        Notify subscribers about the event weekly
        """

    def monthly():
        """
        Notify subscribers about the event monthly
        """
