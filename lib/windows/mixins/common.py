# coding=utf-8

from kodi_six import xbmcgui
from lib import util


class CommonMixin(object):
    @classmethod
    def isWatchedAction(cls, action):
        return action == xbmcgui.ACTION_NONE and action.getButtonCode() == 61527

    def toggleWatched(self, item, state=None, **kw):
        """

        :param item:
        :param state: the state we want to set watched to
        :param kw:
        :return:
        """
        if state is None:
            state = not item.isFullyWatched

        util.DEBUG_LOG("Toggling watched for {} to: {}", item, state)

        if state:
            item.markWatched(**kw)
            return False
        else:
            item.markUnwatched(**kw)
            return True
