#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from functools import lru_cache
from typing import Any, Mapping, MutableMapping, Optional, Union

import requests
from airbyte_cdk.sources.declarative.interpolation.interpolated_string import InterpolatedString
from airbyte_cdk.sources.declarative.requesters.error_handlers.default_error_handler import DefaultErrorHandler
from airbyte_cdk.sources.declarative.requesters.error_handlers.error_handler import ErrorHandler
from airbyte_cdk.sources.declarative.requesters.error_handlers.response_status import ResponseStatus
from airbyte_cdk.sources.declarative.requesters.request_options.interpolated_request_options_provider import (
    InterpolatedRequestOptionsProvider,
)
from airbyte_cdk.sources.declarative.requesters.request_options.request_options_provider import RequestOptionsProvider
from airbyte_cdk.sources.declarative.requesters.requester import HttpMethod, Requester
from airbyte_cdk.sources.declarative.types import Config
from airbyte_cdk.sources.streams.http.auth import HttpAuthenticator, NoAuth


class HttpRequester(Requester):
    def __init__(
        self,
        *,
        name: str,
        url_base: InterpolatedString,
        path: InterpolatedString,
        http_method: Union[str, HttpMethod] = HttpMethod.GET,
        request_options_provider: Optional[RequestOptionsProvider] = None,
        authenticator: HttpAuthenticator = None,
        error_handler: Optional[ErrorHandler] = None,
        config: Config,
    ):
        if request_options_provider is None:
            request_options_provider = InterpolatedRequestOptionsProvider(config=config)
        elif isinstance(request_options_provider, dict):
            request_options_provider = InterpolatedRequestOptionsProvider(config=config, **request_options_provider)
        self._name = name
        self._authenticator = authenticator or NoAuth()
        self._url_base = url_base
        self._path: InterpolatedString = path
        if type(http_method) == str:
            http_method = HttpMethod[http_method]
        self._method = http_method
        self._request_options_provider = request_options_provider
        self._error_handler = error_handler or DefaultErrorHandler()
        self._config = config

    def get_authenticator(self):
        return self._authenticator

    def get_url_base(self):
        return self._url_base.eval(self._config)

    def get_path(self, *, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any], next_page_token: Mapping[str, Any]) -> str:
        kwargs = {"stream_state": stream_state, "stream_slice": stream_slice, "next_page_token": next_page_token}
        path = self._path.eval(self._config, **kwargs)
        return path

    def get_method(self):
        return self._method

    # use a tiny cache to limit the memory footprint. It doesn't have to be large because we mostly
    # only care about the status of the last response received
    @lru_cache(maxsize=10)
    def should_retry(self, response: requests.Response) -> ResponseStatus:
        # Cache the result because the HttpStream first checks if we should retry before looking at the backoff time
        return self._error_handler.should_retry(response)

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        return self._request_options_provider.request_params(stream_state, stream_slice, next_page_token)

    def request_headers(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        return self._request_options_provider.request_headers(stream_state, stream_slice, next_page_token)

    def request_body_data(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Optional[Union[Mapping, str]]:
        return self._request_options_provider.request_body_data(stream_state, stream_slice, next_page_token)

    def request_body_json(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Optional[Mapping]:
        return self._request_options_provider.request_body_json(stream_state, stream_slice, next_page_token)

    def request_kwargs(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        return self._request_options_provider.request_kwargs(stream_state, stream_slice, next_page_token)

    @property
    def cache_filename(self) -> str:
        # FIXME: this should be declarative
        return f"{self._name}.yml"

    @property
    def use_cache(self) -> bool:
        # FIXME: this should be declarative
        return False
