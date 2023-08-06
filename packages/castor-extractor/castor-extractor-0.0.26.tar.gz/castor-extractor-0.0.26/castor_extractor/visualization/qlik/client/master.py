from typing import Callable, Dict, List, Optional, Union

from tqdm import tqdm  # type: ignore

from ..assets import QlikAsset
from .constants import SCOPED_ASSETS
from .engine import EngineApiClient
from .rest import RestApiClient

ListedData = List[dict]
KeyedData = Dict[str, ListedData]


class MissingAppsScopeError(Exception):
    """
    Error to be raised when the scope on apps was required and not provided
    """

    def __init__(self, asset: QlikAsset):
        error_msg = f"App ids must be provided to fetch {asset}."
        super().__init__(error_msg)


def _fetch_on_apps(
    app_ids: List[str], fetch_callback: Callable, display_progress: bool
) -> KeyedData:
    apps_data: KeyedData = dict()
    apps_iterator = app_ids if not display_progress else tqdm(app_ids)
    for app_id in apps_iterator:
        data = fetch_callback(app_id)
        apps_data[app_id] = data
    return apps_data


class QlikMasterClient:
    """
    Qlik master client acts as a wrapper class on top of Qlik RestApiClient and
    EngineApiClient to fetch assets regardless of the underlying API.
    """

    def __init__(
        self,
        server_url: str,
        api_key: str,
        except_http_error_statuses: Optional[List[int]] = None,
        display_progress: bool = True,
    ):
        self._server_url = server_url
        self._api_key = api_key
        self.display_progress = display_progress

        self.rest_api_client = RestApiClient(
            server_url=self._server_url,
            api_key=self._api_key,
            except_http_error_statuses=except_http_error_statuses,
        )

        self.engine_api_client = EngineApiClient(
            server_url=self._server_url, api_key=self._api_key
        )

    def _fetch_lineage(self, app_ids: List[str]) -> KeyedData:
        callback = self.rest_api_client.data_lineage
        return _fetch_on_apps(app_ids, callback, self.display_progress)

    def _fetch_measures(self, app_ids: List[str]) -> KeyedData:
        callback = self.engine_api_client.measures
        return _fetch_on_apps(app_ids, callback, self.display_progress)

    def fetch(
        self, asset: QlikAsset, *, app_ids: List[str] = None
    ) -> Union[ListedData, KeyedData]:
        """
        Given a QlikAsset, returns the corresponding data using the
        appropriate client.

        Note:
            QlikAsset.LINEAGE and QlikAsset.MEASURES must be provided a
            scope on app_ids
        """
        if asset in SCOPED_ASSETS and not app_ids:
            raise MissingAppsScopeError(asset)

        if asset == QlikAsset.MEASURES:
            assert app_ids  # can't be False as we priorly checked
            return self._fetch_measures(app_ids)

        if asset == QlikAsset.LINEAGE:
            assert app_ids  # can't be False as we priorly checked
            return self._fetch_lineage(app_ids)

        return self.rest_api_client.get(asset)
