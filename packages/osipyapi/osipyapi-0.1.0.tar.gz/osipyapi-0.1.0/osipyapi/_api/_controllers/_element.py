from typing import Sequence

from .._api import api, semi_col_formatter, multi_inst_formatter



element = api.router(
    '/elements',
    formatters=dict(
        selected_fields=semi_col_formatter,
        associations=semi_col_formatter
    )
)



class Element:
    """
    https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/element.html
    """

    @element.endpoint('/{web_id}')
    @staticmethod
    def get(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/element/actions/get.html
        """

    @element.endpoint()
    @staticmethod
    def get_by_path(
        path: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/element/actions/getbypath.html
        """

    @element.endpoint(
        '/mulitple',
        formatters=dict(
            web_id=multi_inst_formatter,
            path=multi_inst_formatter
        )
    )
    @staticmethod
    def get_multiple(
        web_id: Sequence[str] = None,
        path: Sequence[str] = None,
        include_mode: str = None,
        as_parallel: bool = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/element/actions/getmultiple.html
        """
        if web_id is None and path is None:
            raise ValueError("Must specify one of either 'web_id' or 'path'")
        
    @element.endpoint('/{web_id}/elements')
    @staticmethod
    def get_elements(
        web_id: str,
        name_filter: str = None,
        description_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        element_type: str = None,
        search_full_hierarchy: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        start_index: int = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/element/actions/getelements.html
        """

    @element.endpoint('/{web_id}/attributes')
    @staticmethod
    def get_attributes(
        web_id: str,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        value_type: str = None,
        search_full_hierarchy: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        start_index: int = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/element/actions/getattributes.html
        """