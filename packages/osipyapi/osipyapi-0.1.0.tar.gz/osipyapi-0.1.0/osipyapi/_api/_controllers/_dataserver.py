from typing import Sequence

from .._api import api, semi_col_formatter



dataserver = api.router(
    '/dataservers',
    formatters=dict(selected_fields=semi_col_formatter)
)



class DataServer:
    """
    https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver.html
    """

    @dataserver.endpoint()
    @staticmethod
    def list(
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/list.html
        """

    @dataserver.endpoint('/{web_id}')
    @staticmethod
    def get(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/get.html
        """

    @dataserver.endpoint()
    @staticmethod
    def get_by_path(
        path: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/getbypath.html
        """
    
    @dataserver.endpoint()
    @staticmethod
    def get_by_name(
        name: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/getbyname.html
        """

    @dataserver.endpoint('/{web_id}/enumerationsets')
    @staticmethod
    def get_enumeration_sets(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/getenumerationsets.html
        """

    @dataserver.endpoint('/{web_id}/license')
    @staticmethod
    def get_license(
        web_id: str,
        module: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/getlicense.html
        """
    
    @dataserver.endpoint('/{web_id}/points')
    @staticmethod
    def get_points(
        web_id: str,
        name_filter: str = None,
        source_filter: str = None,
        start_index: int = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/dataserver/actions/getpoints.html
        """