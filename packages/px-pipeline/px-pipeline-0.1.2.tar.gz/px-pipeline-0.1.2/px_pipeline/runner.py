from logging import getLogger

from .pipelines import *


logger = getLogger(__name__)

logger.warn('Do not use px_pipeline.runner directly. It\'s deprecated.')
