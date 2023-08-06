from datetime import datetime, timedelta
from typing import Sequence

from .._api import api, semi_col_formatter, multi_inst_formatter



stream = api.router(
    '/streams',
    formatters=dict(selected_fields=semi_col_formatter)
)



class Stream:
    """
    https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream.html
    """

    @stream.endpoint('/{web_id}/channel')
    @staticmethod
    def get_channel(
        web_id: str,
        include_initial_values: bool = None,
        heartbeat_rate: int = None,
        web_id_type: str = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getchannel.html
        """
    
    @stream.endpoint('/{web_id}/end')
    @staticmethod
    def get_end(
        web_id: str,
        desired_units: str = None,
        selected_fields: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getend.html
        """
    
    @stream.endpoint('/{web_id}/interpolated')
    @staticmethod
    def get_interpolated(
        web_id: str,
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        interval: timedelta = None,
        sync_time: datetime = None,
        sync_time_boundary_type: str = None,
        desired_units: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        selected_fields: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getinterpolated.html
        """
    
    @stream.endpoint(
        '/{web_id}/interpolatedattimes',
        formatters=dict(time=multi_inst_formatter)
    )
    @staticmethod
    def get_interpolated_at_times(
        web_id: str,
        time: Sequence[datetime],
        time_zone: str = None,
        desired_units: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getinterpolatedattimes.html
        """
    
    @stream.endpoint(
        '/{web_id}/recorded',
        formatters=dict(associations=semi_col_formatter)
    )
    @staticmethod
    def get_recorded(
        web_id: str,
        start_time: datetime = None,
        end_time: datetime = None,
        time_zone: str = None,
        boundary_type: str = None,
        desired_units: str = None,
        filter_expression: str = None,
        include_filtered_values: bool = None,
        max_count: int = None,
        selected_fields: Sequence[str] = None,
        associations: Sequence[str] = None
    ):

        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getrecorded.html
        """

    @stream.endpoint(
        '/{web_id}/recordedattime',
        formatters=dict(associations=semi_col_formatter)
    )
    @staticmethod
    def get_recorded_at_time(
        web_id: str,
        time: datetime,
        time_zone: str = None,
        retrieval_mode: str = None,
        desired_units: str = None,
        selected_fields: Sequence[str] = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getrecordedattime.html
        """
    
    @stream.endpoint(
        '/{web_id}/recordedattimes',
        formatters=dict(
            time=multi_inst_formatter,
            associations=semi_col_formatter
        )
    )
    @staticmethod
    def get_recorded_at_times(
        web_id: str,
        time: Sequence[datetime],
        time_zone: str = None,
        retrieval_mode: str = None,
        desired_units: str = None,
        sort_order: str = None,
        selected_fields: Sequence[str] = None,
        associations: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getrecordedattimes.html
        """

    @stream.endpoint('/{web_id}/summary')
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
        selected_fields: Sequence[str] = None,
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getsummary.html
        """

    @stream.endpoint('/{web_id}/value')
    @staticmethod
    def get_value(
        web_id: str,
        time: datetime,
        time_zone: str = None,
        desired_units: str = None,
        selected_fields: Sequence[str] = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/stream/actions/getvalueadhoc.html
        """