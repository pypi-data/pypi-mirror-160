from contextlib import contextmanager
from typing import Any, Dict, Optional, Union

import opentracing
from opentracing import Scope

from cognite.tracing import config


@contextmanager
def span(name: str, tags: Optional[Dict[str, Any]] = None) -> Scope:
    """Contextmanager for wrapping a code block in a trace span

    :param name: Name of the span as it will be shown in traces
    :param tags: Any tags the span should have

    Will wrap a code block in a span.

    Example usage:
    ```python
    with span("process", tags={"request_id": "a-request-id", "user_id": 1}):
        process_function()
        some_other_relevant_function()
    ```
    """
    parent = opentracing.tracer.active_span
    child_of = parent.context if parent is not None else None
    with opentracing.tracer.start_active_span(operation_name=name, child_of=child_of, tags=tags) as scope:
        if parent and hasattr(parent, "tags"):
            for key, value in parent.tags.items():
                if key in config.tags_to_inherit:
                    scope.span.set_tag(key, value)
        try:
            yield scope
        except Exception as e:
            scope.span.log(event="exception", payload=e)
            scope.span.set_tag("error", "true")
            raise


def set_tag_on_span(tag_key: str, tag_value: Union[int, str]) -> None:
    """Add tag to current span

    :param tag_key: The tag key
    :param tag_value: The tag value

    Will add a tag with value to the current span.

    Example usage:
    ```python
    response = do_request()
    set_tag_on_span("request_id", response.request_id)
    set_tag_on_span("request_duration", response.request_duration)
    ```
    """
    parent = opentracing.tracer.active_span
    if parent is not None:
        parent.set_tag(tag_key, tag_value)
