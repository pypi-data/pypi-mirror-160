#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from typing import Mapping, Type

from airbyte_cdk.sources.declarative.checks.check_stream import CheckStream
from airbyte_cdk.sources.declarative.checks.connection_checker import ConnectionChecker
from airbyte_cdk.sources.declarative.datetime.min_max_datetime import MinMaxDatetime
from airbyte_cdk.sources.declarative.declarative_stream import DeclarativeStream
from airbyte_cdk.sources.declarative.decoders.decoder import Decoder
from airbyte_cdk.sources.declarative.decoders.json_decoder import JsonDecoder
from airbyte_cdk.sources.declarative.extractors.http_selector import HttpSelector
from airbyte_cdk.sources.declarative.extractors.record_selector import RecordSelector
from airbyte_cdk.sources.declarative.interpolation.interpolated_string import InterpolatedString
from airbyte_cdk.sources.declarative.requesters.error_handlers.default_error_handler import DefaultErrorHandler
from airbyte_cdk.sources.declarative.requesters.error_handlers.error_handler import ErrorHandler
from airbyte_cdk.sources.declarative.requesters.error_handlers.http_response_filter import HttpResponseFilter
from airbyte_cdk.sources.declarative.requesters.http_requester import HttpRequester
from airbyte_cdk.sources.declarative.requesters.paginators.no_pagination import NoPagination
from airbyte_cdk.sources.declarative.requesters.paginators.paginator import Paginator
from airbyte_cdk.sources.declarative.requesters.request_options.interpolated_request_options_provider import (
    InterpolatedRequestOptionsProvider,
)
from airbyte_cdk.sources.declarative.requesters.request_options.request_options_provider import RequestOptionsProvider
from airbyte_cdk.sources.declarative.requesters.requester import Requester
from airbyte_cdk.sources.declarative.retrievers.retriever import Retriever
from airbyte_cdk.sources.declarative.retrievers.simple_retriever import SimpleRetriever
from airbyte_cdk.sources.declarative.schema.json_schema import JsonSchema
from airbyte_cdk.sources.declarative.schema.schema_loader import SchemaLoader
from airbyte_cdk.sources.declarative.states.dict_state import DictState
from airbyte_cdk.sources.declarative.states.state import State
from airbyte_cdk.sources.declarative.stream_slicers.single_slice import SingleSlice
from airbyte_cdk.sources.declarative.stream_slicers.stream_slicer import StreamSlicer
from airbyte_cdk.sources.streams.core import Stream

DEFAULT_IMPLEMENTATIONS_REGISTRY: Mapping[Type, Type] = {
    Requester: HttpRequester,
    Retriever: SimpleRetriever,
    SchemaLoader: JsonSchema,
    HttpSelector: RecordSelector,
    ConnectionChecker: CheckStream,
    ErrorHandler: DefaultErrorHandler,
    Decoder: JsonDecoder,
    State: DictState,
    StreamSlicer: SingleSlice,
    RequestOptionsProvider: InterpolatedRequestOptionsProvider,
    Paginator: NoPagination,
    HttpResponseFilter: HttpResponseFilter,
    Stream: DeclarativeStream,
    MinMaxDatetime: MinMaxDatetime,
    InterpolatedString: InterpolatedString,
}
