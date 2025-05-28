from __future__ import absolute_import
from . import plexapp
from . import plexconnection
from . import plexserver
from . import plexresource
from . import plexservermanager
from . import compat


class MyPlexServer(plexserver.PlexServer):
    TYPE = 'MYPLEXSERVER'

    def __init__(self):
        plexserver.PlexServer.__init__(self)
        self.uuid = 'myplex'
        self.name = 'plex.tv'
        conn = plexconnection.PlexConnection(plexresource.ResourceConnection.SOURCE_MYPLEX, "https://plex.tv", False,
                                             None, skipLocalCheck=True)
        self.connections.append(conn)
        self.activeConnection = conn

    def getToken(self):
        return plexapp.ACCOUNT.authToken

    def buildUrl(self, path, includeToken=False):
        if "://node.plexapp.com" in path:
            # Locate the best fit server that supports channels, otherwise we'll
            # continue to use the node urls. Service code between the node and
            # PMS differs sometimes, so it's a toss up which one is actually
            # more accurate. Either way, we try to offload work from the node.

            server = plexservermanager.MANAGER.getChannelServer()
            if server:
                url = server.swizzleUrl(path, includeToken)
                if url:
                    return url

        return plexserver.PlexServer.buildUrl(self, path, includeToken)


class PlexDiscoverServer(MyPlexServer):
    TYPE = 'PLEXDISCOVERSERVER'

    def __init__(self):
        MyPlexServer.__init__(self)
        self.uuid = 'plexdiscover'
        self.name = 'discover.plex.tv'
        conn = plexconnection.PlexConnection(plexresource.ResourceConnection.SOURCE_MYPLEX,
                                             "https://discover.provider.plex.tv", False,
                                             None, skipLocalCheck=True)
        self.connections.append(conn)
        self.activeConnection = conn

    def getImageTranscodeURL(self, path, width, height, **extraOpts):
        if not path:
            return ''

        eOpts = {"scale": 1}
        eOpts.update(extraOpts)
        imageUrl = path

        params = ("&width=%s&height=%s" % (width, height)) + ''.join(["&%s=%s" % (key, eOpts[key]) for key in eOpts])

        path = "/photo?url=" + compat.quote_plus(imageUrl) + params

        return "https://images.plex.tv{}".format(path)
