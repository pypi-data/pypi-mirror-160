from typing import Any, Callable, List, Optional, Tuple

from .exceptions import StopFlow
from .utils import normalize_executable, Executable


__all__ = 'Pipeline', 'StraightPipeline',

Context = dict
Step = Callable[..., Any]


class Pipeline:
    START = object()
    FINISH = object()

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def next(self, current, context: Context) -> Tuple[Any, Optional[Step]]:
        raise NotImplementedError()

    def prepare_context(self, context: Context) -> Context:
        return context

    def handle_result(self, step: Step, result: Any, context: Context) -> Any:
        if result is None:
            return context

        if isinstance(result, dict):
            context.update(result)

        return context

    def execute_step(self, step: Step, context: Context) -> Any:
        return step(context)

    def __call__(self, context: Context) -> Context:
        context = self.prepare_context(context)
        current = self.START

        while current != self.FINISH:
            try:
                current = self.next(current, context)
                result = self.execute_step(current, context)
            except StopFlow as e:
                result = e.result
                current = self.FINISH

            context = self.handle_result(current, result, context)

        return context


StraightPipelineSteps = List[Executable]
StraightStep = Tuple[int, Optional[Step]]


class StraightPipeline(Pipeline):
    pipeline: StraightPipelineSteps

    def execute_step(self, step: StraightStep, context: Context) -> Any:
        return step[1](context)

    def next(self, current, context: Context) -> StraightStep:
        index = -1

        if current is not self.START:
            index, _ = current

        if index + 1 >= len(self.pipeline):
            raise StopFlow(None)

        index += 1

        return index, normalize_executable(self.pipeline[index])
