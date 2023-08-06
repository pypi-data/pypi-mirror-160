from .._api import api



channel = api.router('/channels')



class Channel:

    @channel.endpoint('/instances')
    def get_instances():
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/channel/actions/instances.html
        """