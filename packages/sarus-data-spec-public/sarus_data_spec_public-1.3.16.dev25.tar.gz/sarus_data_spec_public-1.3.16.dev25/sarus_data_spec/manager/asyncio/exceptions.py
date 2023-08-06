from functools import wraps
from typing import Any, Callable, Optional
import sys
import traceback


class SarusComputationError(Exception):
    ...


class SarusPropagatedError(Exception):
    """This class registers information about a root exception."""

    def __init__(self, text: Optional[str] = None) -> None:
        if text is None:
            exc, val, tb = sys.exc_info()
            try:
                kernel = get_ipython()  # type: ignore # noqa
                lines = kernel.InteractiveTB.structured_traceback(exc, val, tb)
            except Exception:
                lines = traceback.format_exception(
                    exc,
                    val,
                    tb,
                )
            self.text = "\n".join(lines)
        else:
            self.text = text


def unwrap_propagated_error(fn: Callable) -> Callable:
    """This will catch the propagated error and display only two errors.
    The originally catched errors and the computation error.
    All propagated errors will be omitted."""

    @wraps(fn)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except SarusPropagatedError as e:
            comp_error = SarusComputationError(
                f"Error when computing {fn.__name__}\n\n{e.text}"
            )
            raise comp_error from None

    return wrapped
