from typing import Any, Optional

import elasticapm.contrib.opentracing
import lightstep
from elasticapm import Client
from opentracing import ScopeManager, Tracer
from opentracing import set_global_tracer as _set_global_tracer
from opentracing.scope_managers import ThreadLocalScopeManager


def set_global_tracer(tracer: Tracer) -> None:
    """Set this tracer as the global opentracing tracer"""
    _set_global_tracer(tracer)


def initialize_elastic_apm_tracer(
    component_name: str, scope_manager: ScopeManager = ThreadLocalScopeManager(), **config: Any
) -> None:
    """Initialize Elastic APM tracer

    :param component_name: Name of component as it will be shown in Lightstep traces
    :param scope_manager: Scope manager
    :param access_token: Lightstep access token. Required for use in production, as Lightstep requires authentication
    :param **config: Additional arguments passed to the Elastic APM Client config

    Initializes a global Elastic APM tracer. This method should be called on application startup.
    If a thread local scope manager is not sufficient, provide one with the `scope_manager` argument.
    Do not provide `access_token` while in development mode.
    """
    tracer = elasticapm.contrib.opentracing.Tracer(client_instance=Client(**config), scope_manager=scope_manager)
    set_global_tracer(tracer)


def initialize_lightstep_tracer(
    component_name: str, scope_manager: ScopeManager = ThreadLocalScopeManager(), access_token: Optional[str] = None
) -> None:
    """Initialize Lightstep tracer

    :param component_name: Name of component as it will be shown in Lightstep traces
    :param scope_manager: Scope manager
    :param access_token: Lightstep access token. Required for use in production, as Lightstep requires authentication

    Initializes a global Lightstep tracer. This method should be called on application startup.
    If a thread local scope manager is not sufficient, provide one with the `scope_manager` argument.
    Do not provide `access_token` while in development mode.
    """
    if access_token is None:
        access_token = "developer"  # nosec
        collector_host = "localhost"
        collector_port = 8360
        collector_encryption = "none"
        use_http = True
    else:
        collector_host = "lightstep-collector.internal-services"
        collector_port = 80
        collector_encryption = "none"
        use_http = False
    tracer = lightstep.Tracer(
        component_name=component_name,
        collector_host=collector_host,
        collector_port=collector_port,
        use_http=use_http,
        use_thrift=True,
        collector_encryption=collector_encryption,
        access_token=access_token,
        scope_manager=scope_manager,
    )
    set_global_tracer(tracer)
