from ._controllers import (
    AssetDatabase,
    AssetServer,
    Attribute,
    Channel,
    DataServer,
    Element,
    Point,
    Search,
    Stream,
    StreamSet
)


class PiWebApi:
    asset_database = AssetDatabase
    asset_server = AssetServer
    attribute = Attribute
    channel = Channel
    data_server = DataServer
    element = Element
    point = Point
    search = Search
    stream = Stream
    stream_set = StreamSet


pi_web_api = PiWebApi