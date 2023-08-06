from datetime import datetime, timedelta
from typing import Sequence

from .._api import api, semi_col_formatter, multi_inst_formatter



streamset = api.router(
    '/streamsets',
    formatters=dict(
        selected_fields=semi_col_formatter,
        web_id=multi_inst_formatter
    )
)



class StreamSet:
    """
    https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset.html
    """

    @streamset.endpoint('/{web_id}/channel')
    @staticmethod
    def get_channel(
        web_id: str,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        include_initial_values: bool = None,
        heartbeat_rate: int = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getchannel.html
        """
    
    @streamset.endpoint('/channel')
    @staticmethod
    def get_channel_adhoc(
        web_id: Sequence[str],
        include_initial_values: bool = None,
        heartbeat_rate: int = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getchanneladhoc.html
        """
    
    @streamset.endpoint('/{web_id}/end')
    @staticmethod
    def get_end(
        web_id: str,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getend.html
        """

    
    @streamset.endpoint('/end')
    @staticmethod
    def get_end_adhoc(
        web_id: Sequence[str],
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getendadhoc.html
        """
    
    @streamset.endpoint('/{web_id}/interpolated')
    @staticmethod
    def get_interpolated(
        web_id: str,
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        interval: timedelta = None,
        sync_time: datetime = None,
        sync_time_boundary_type: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getinterpolated.html
        """
    
    @streamset.endpoint('/interpolated')
    @staticmethod
    def get_interpolated_adhoc(
        web_id: Sequence[str],
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        interval: timedelta = None,
        sync_time: datetime = None,
        sync_time_boundary_type: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getinterpolatedadhoc.html
        """
    
    @streamset.endpoint(
        '/{web_id}/interpolatedattimes',
        formatters=dict(time=multi_inst_formatter)
    )
    @staticmethod
    def get_interpolated_at_times(
        web_id: str,
        time: Sequence[datetime],
        time_zone: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getinterpolatedattimes.html
        """

    @streamset.endpoint(
        '/interpolatedattimes',
        formatters=dict(time=multi_inst_formatter)
    )
    @staticmethod
    def get_interpolated_at_times_adhoc(
        web_id: Sequence[str],
        time: Sequence[datetime],
        time_zone: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getinterpolatedattimesadhoc.html
        """
    
    @streamset.endpoint(
        '/joined',
        formatters=dict(subordinate_web_id=multi_inst_formatter)
    )
    @staticmethod
    def get_joined(
        base_web_id: str,
        subordinate_web_id: Sequence[str],
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        boundary_type: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getjoined.html
        """
    
    @streamset.endpoint('/{web_id}/recorded')
    @staticmethod
    def get_recorded(
        web_id: str,
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        boundary_type: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        max_count: int = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getrecorded.html
        """
    
    @streamset.endpoint('/recorded')
    @staticmethod
    def get_recorded_adhoc(
        web_id: Sequence[str],
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        boundary_type: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        max_count: int = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getrecordedadhoc.html
        """

    @streamset.endpoint('/{web_id}/recordedattime')
    @staticmethod
    def get_recorded_at_time(
        web_id: str,
        time: datetime,
        time_zone: str = None,
        retrieval_mode: str = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getrecordedattime.html
        """
    
    @streamset.endpoint('/recorded')
    @staticmethod
    def get_recorded_at_time_adhoc(
        web_id: Sequence[str],
        time: datetime,
        time_zone: str = None,
        retrieval_mode: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getrecordedattimeadhoc.html
        """

    @streamset.endpoint(
        '/{web_id}/recordedattimes',
        formatters=dict(time=multi_inst_formatter)
    )
    @staticmethod    
    def get_recorded_at_times(
        web_id: str,
        time: Sequence[datetime],
        time_zone: str = None,
        retrieval_mode: str = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getrecordedattimes.html
        """

    @streamset.endpoint(
        '/recordedattimes',
        formatters=dict(time=multi_inst_formatter)
    )
    @staticmethod
    def get_recorded_at_times_adhoc(
        web_id: Sequence[str],
        time: Sequence[datetime],
        time_zone: str = None,
        retrieval_mode: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getrecordedattimesadhoc.html
        """

    @streamset.endpoint('/{web_id}/summary')
    @staticmethod
    def get_summary(
        web_id: str,
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        summary_type: str = None,
        calculation_basis: str = None,
        time_type: str = None,
        summary_duration: str = None,
        sample_type: str = None,
        sample_interval: timedelta = None,
        filter_expression: str = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getsummary.html
        """
    
    @streamset.endpoint('/summary')
    @staticmethod
    def get_summary_adhoc(
        web_id: Sequence[str],
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        summary_type: str = None,
        calculation_basis: str = None,
        time_type: str = None,
        summary_duration: str = None,
        sample_type: str = None,
        sample_interval: timedelta = None,
        filter_expression: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getsummaryadhoc.html
        """

    @streamset.endpoint('/{web_id}/value')
    @staticmethod
    def get_value(
        web_id: str,
        time: datetime,
        time_zone: str = None,
        name_filter: str = None,
        category_name: str = None,
        template_name: str = None,
        search_full_hierarchy: bool = None,
        show_excluded: bool = None,
        show_hidden: bool = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getvalueadhoc.html
        """

    @streamset.endpoint('/value')
    @staticmethod
    def get_value_adhoc(
        web_id: Sequence[str],
        time: datetime,
        time_zone: str = None,
        sort_field: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/streamset/actions/getvalueadhoc.html
        """