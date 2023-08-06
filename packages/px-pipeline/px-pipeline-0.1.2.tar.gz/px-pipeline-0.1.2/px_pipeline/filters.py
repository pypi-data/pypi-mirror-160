from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from enum import Enum

from .utils import Executable
from .pipelines import StraightPipeline, Pipeline, Context


__all__ = 'Filter', 'FilterLayer',


class FilterLayer(int, Enum):
    PRECEDE = 100
    AVERAGE = 500
    FINAL = 900


class Filter:
    Layer = FilterLayer
    INCREMENT: Decimal = Decimal('0.0000000000001')

    default_priority: int = 10
    pipeline_class: Pipeline = StraightPipeline
    pipeline: Pipeline
    version: Tuple[int, int]
    registry: Dict[Executable, Tuple[int, int]]

    def __init__(
        self,
        initial: List[Executable] = [],
        pipeline_class: Optional[Pipeline] = None,
        default_priority: Optional[int] = None,
    ):
        self.pipeline_class = pipeline_class or self.pipeline_class
        self.default_priority = default_priority or self.default_priority
        self.version = [0, self.INCREMENT]
        self.registry = {}

        self.add_multiple(initial)

    def is_fresh(self) -> bool:
        cached, current = self.version

        return cached == current

    def resolve_pipeline(self):
        if self.is_fresh():
            return self.pipeline

        self.pipeline = self.pipeline_class(
            sorted(self.registry, key=self.order_key)
        )
        self.version[0] = self.version[1]

        return self.pipeline

    def order_key(self, entry: Executable) -> Tuple:
        return self.registry[entry]

    def add(
        self,
        fn: Executable,
        priority: Optional[int] = None,
        layer: Optional[int] = None,
    ):
        if fn in self.registry:
            raise ValueError(
                f'Handler "{fn}" already registered. Remove it to add again.'
            )

        self.version[1] += self.INCREMENT
        priority = Decimal(priority) if priority is not None else self.default_priority

        self.registry[fn] = (
            layer if layer is not None else self.Layer.AVERAGE,
            priority + self.version[1],
        )

    def add_multiple(
        self,
        fns: List[Executable],
        priority: Optional[int] = None,
        layer: Optional[int] = None,
    ):
        for item in fns:
            self.add(item, priority=priority, layer=layer)

    def remove(self, fn: Executable):
        if fn not in self.registry:
            raise ValueError(f'Handler "{fn}" not registered.')

        self.registry.pop(fn)

    def __call__(self, context: Context) -> Context:
        return self.resolve_pipeline()(context)
