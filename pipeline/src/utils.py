import pandas as pd
import logging
from abc import ABC, abstractmethod

class PipelineStage(ABC):
    # Base para pipeline
    def __init__(self, config):
        self.config = config
        self.config['pipeline_folder'] = 'pipeline/'
        self.config['raw_data_folder'] = 'raw_data/'
        self.config['curated_data_folder'] = 'curated_data/'
        self.config['analytics_data_folder'] = 'analytics_data/'
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self):
        pass