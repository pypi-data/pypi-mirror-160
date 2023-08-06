class PipelineError(Exception):
    """
    Base class for exceptions in this module.
    """
    pass


class StopFlow(PipelineError):
    """
    Raised when a flow should be stopped immediately.
    """

    def __init__(self, result, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.result = result
