import pandas as pd
import logging
from abc import ABC, abstractmethod

class PipelineStage(ABC):
    """Superclass for all pipeline stages. 
    Basic structure for all pipeline stages.

    Args:
        ABC (obj): Abstract Base Class lib
    """
    # Base para pipeline
    def __init__(self, config):
        """Pipeline stage initialization

        Args:
            config (dict): conigs to run the pipeline stage
        """
        self.config = config
        self.config['pipeline_folder'] = 'pipeline/'
        self.config['raw_data_folder'] = 'raw_data/'
        self.config['curated_data_folder'] = 'curated_data/'
        self.config['analytics_data_folder'] = 'analytics_data/'
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self):
        pass