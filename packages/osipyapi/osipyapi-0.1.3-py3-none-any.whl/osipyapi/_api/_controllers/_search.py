from typing import Sequence

from .._api import api, semi_col_formatter



search = api.router('/search')


class Search:
    """
    https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/search.html
    """

    @search.endpoint(
        '/query',
        formatters=dict(
            scope=semi_col_formatter,
            fields=semi_col_formatter
        )
    )
    @staticmethod
    def execute_query(
        q: str,
        scope: Sequence[str] = None,
        fields: Sequence[str] = None,
        count: int = None,
        start: int = None
    ):
        """
        https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/controllers/search/actions/query.html
        """