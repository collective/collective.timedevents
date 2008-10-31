"""
    Time based events

"""

__author__ = "Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>"
__copyright__ = "Copyright 2008 Twinapex Research"
__license__ = "GPL"
__docformat__ = "epytext"


from zope.interface import Interface, Attribute

class ITickEvent(Interface):
    '''An event signaling a tick (vide the TickingMachine class).
    '''
    date_time = Attribute("Time of the last tick")
    next_tick = Attribute("Estimated time of the next tick")


