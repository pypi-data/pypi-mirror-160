from .summarization import SummarizationPipeline


class Pipeline(object):
    """
    Base class to use pipeline object
    """

    def __init__(self,
                 task: str,
                 **kwargs):
        if task == 'summarization':
            self.pipeline = SummarizationPipeline(**kwargs)

    def __call__(self,
                 **kwargs):
        return self.pipeline(**kwargs)


