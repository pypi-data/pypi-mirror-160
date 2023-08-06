from dataclasses import dataclass
import os
from typing import Any, Callable, Dict, Optional, TypeVar

from airplane.runtime import RuntimeKind, __AIRPLANE_RUNTIME_ENV_VAR, execute


@dataclass
class TaskConfig:
    """Represents a task configuration."""

    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Any = None
    require_requests: Optional[bool] = None
    allow_self_approvals: Optional[bool] = None
    timeout: Optional[int] = None
    constraints: Optional[Dict[str, str]] = None
    runtime: Optional[RuntimeKind] = None

TOutput = TypeVar('TOutput')
UserFunc = Callable[[Dict[str, Any]], TOutput]

@dataclass
class __Task:
    config: TaskConfig
    base_func: UserFunc
    in_airplane_runtime: bool

    def __call__(self, params: Dict[str, Any]) -> TOutput:
        if self.in_airplane_runtime:
            return execute(self.config.slug, params).output
        return self.base_func(params)


def task(config: TaskConfig, func: UserFunc) -> UserFunc:
    """Wraps a user function as an Airplane task

    Args:
        config: The task configuration.
        func: User function to deploy as an Airplane function.
    """
    runtime_kind = os.environ.get(__AIRPLANE_RUNTIME_ENV_VAR)
    in_airplane_runtime = runtime_kind is not None and runtime_kind != RuntimeKind.DEV.value

    return __Task(config, func, in_airplane_runtime)


h = task(TaskConfig(slug="foo"), lambda params: "Hello!")
print(h({}))
