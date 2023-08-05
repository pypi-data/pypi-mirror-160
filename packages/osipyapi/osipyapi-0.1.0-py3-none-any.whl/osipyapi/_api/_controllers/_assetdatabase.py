from datetime import datetime
from typing import Sequence

from .._api import api, semi_col_formatter, multi_inst_formatter



assetdatabase = api.router(
    '/assetdatabases',
    formatters=dict(selected_fields=semi_col_formatter)
)



class AssetDatabase:
    """
    https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase.html
    """

    @assetdatabase.endpoint('/{web_id}')
    @staticmethod
    def by_web_id(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/get.html
        """

    @assetdatabase.endpoint()
    @staticmethod
    def by_path(
        path: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getbypath.html
        """

    @assetdatabase.endpoint('/{web_id}/analyses')
    @staticmethod
    def find_analyses(
        web_id: str,
        field: str = None,
        query: str = None,
        sort_field: str = None,
        start_index: int = None,
        sort_order: str = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/findanalyses.html
        """

    @assetdatabase.endpoint(
        '/{web_id}/elementattributes',
        formatters=dict(associations=semi_col_formatter)
    )
    @staticmethod
    def find_element_attributes(
        web_id: str,
        element_name_filter: str = None,
        element_description_filter: str = None,
        element_category: str = None,
        element_template: str = None,
        element_type: str = None,
        attribute_name_filter: str = None,
        attribute_description_filter: str = None,
        attribute_category: str = None,
        attribute_type: str = None,
        search_full_hierarchy: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        start_index: int = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/findelementattributes.html
        """

    @assetdatabase.endpoint(
        '/{web_id}/eventframeattributes',
        formatters=dict(associations=semi_col_formatter)
    )
    @staticmethod
    def find_event_frame_attributes(
        web_id: str,
        search_mode: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        event_frame_name_filter: str = None,
        event_frame_description_filter: str = None,
        referenced_element_name_filter: str = None,
        event_frame_category: str = None,
        event_frame_template: str = None,
        attribute_name_filter: str = None,
        attribute_description_filter: str = None,
        attribute_category: str = None,
        attribute_type: str = None,
        search_full_hierarchy: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        start_index: int = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/findeventframeattributes.html
        """

    @assetdatabase.endpoint('/{web_id}/analysiscategories')
    @staticmethod
    def get_analysis_categories(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getanalysiscategories.html
        """

    @assetdatabase.endpoint('/{web_id}/analysistemplates')
    @staticmethod
    def get_analysis_templates(
        web_id: str,
        field: str = None,
        query: str = None,
        sort_field: str = None,
        sort_order: str = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getanalysistemplates.html
        """

    @assetdatabase.endpoint('/{web_id}/attributecategories')
    @staticmethod
    def get_attribute_categories(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getattributecategories.html
        """
        
    @assetdatabase.endpoint('/{web_id}/elementcategories')
    @staticmethod
    def get_element_categories(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getelementcategories.html
        """
        
    @assetdatabase.endpoint(
        '/{web_id}/elements',
        formatters=dict(associations=semi_col_formatter)
    )
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
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getelements.html
        """

    @assetdatabase.endpoint('/{web_id}/elementtemplates')
    @staticmethod
    def get_element_templates(
        web_id: str,
        field: str = None,
        query: str = None,
        sort_field: str = None,
        sort_order: str = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getelementtemplates.html
        """
        
    @assetdatabase.endpoint('/{web_id}/enumerationsets')
    @staticmethod
    def get_enumeration_sets(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getenumerationsets.html
        """
        
    @assetdatabase.endpoint(
        '/{web_id}/eventframes',
        formatters=dict(severity=multi_inst_formatter)
    )
    def get_event_frames(
        web_id: str,
        search_mode: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        name_filter: str = None,
        referenced_element_name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        referenced_element_template_name: str = None,
        severity: Sequence[str] = None,
        can_be_acknowledged: str = None,
        is_acknowleged: str = None,
        search_full_hierarchy: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        start_index: int = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/geteventframes.html
        """

    @assetdatabase.endpoint(
        '/{web_id}/referencedelements',
        formatters=dict(associations=semi_col_formatter)
    )
    def get_referenced_elements(
        web_id: str,
        name_filter: str = None,
        description_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        element_type: str = None,
        sort_field: str = None,
        sort_order: str = None,
        start_index: int = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getreferencedelements.html
        """
        
    @assetdatabase.endpoint(
        '/{web_id}/security',
        formatters=dict(
            security_item=multi_inst_formatter,
            user_identity=multi_inst_formatter
        )
    )
    def get_security(
        web_id: str,
        security_item: Sequence[str] = None,
        user_identity: Sequence[str] = None,
        force_refresh: bool = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getsecurity.html
        """

    @assetdatabase.endpoint('/{web_id}/securityentries')
    @staticmethod
    def get_security_entries(
        web_id: str,
        security_item: str = None,
        name_filter: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getsecurityentries.html
        """
        
    @assetdatabase.endpoint('/{web_id}/securityentries/{name}')
    @staticmethod
    def get_security_entry_by_name(
        web_id: str,
        name: str,
        security_item: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/getsecurityentrybyname.html
        """
        
    @assetdatabase.endpoint('/{web_id}/tablecategories')
    @staticmethod
    def get_table_categories(
        web_id: str,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/assetdatabase/actions/gettablecategories.html
        """