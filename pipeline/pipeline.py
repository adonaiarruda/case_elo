import logging
import src.get_data as get_data
import src.clean_data as clean_data
import src.analytics as analytics


class Pipeline:
    """Pipeline object
    """
    def __init__(self, name, stages):
        """_summary_

        Args:
            name (str): Pipeline name
            stages (list(PipelineStage): stages to run
        """
        self.name = name
        self.stages = stages
        self.logger = logging.getLogger(name)

    def execute(self):
        """ Execute pipeline to solve the case
        """
        self.logger.info(f"Iniciando pipeline: {self.name}")
        data = None
        for stage in self.stages:
            data = stage.execute(data)
        self.logger.info(f"Pipeline {self.name} concluído com sucesso!")

# Configuração do logger
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configurações do pipeline
config_extraction = {'file_id': "1GINDasXHcESqGYMX6KuhEGzCZEx71wHg", 
                   'output_filename': 'raw_data.zip'
                   }
config_unzip = {'path': 'pipeline',
                'zipfilename': 'raw_data.zip'
                }

config_cleaning = {
    'demographics_filename' : 'DemographicData_ZCTAs.csv',
    'economics_filename' : 'EconomicData_ZCTAs.csv',
    'geographic_filename': 'df_geocode.csv',
    'exams_filename': 'exams_data.csv',
    'transactional_filename': 'transactional_data.csv'
}
config_analytics = {'output_filename': 'proposed_zctas.txt'}

# Criar etapas do pipeline
get_data_stage = get_data.ExtractStage(config_extraction)
unzip_stage = get_data.UnzipStage(config_unzip)
cleaning_stage = clean_data.CleaningStage(config_cleaning)
analytics_stage = analytics.AnalyticsStage(config_analytics)

# Cria pipeline
pipeline = Pipeline(
    name = "Rede de Laboratórios",
    stages = [
        get_data_stage, 
        unzip_stage,
        cleaning_stage,
        analytics_stage
        ]
)

# Executa o pipeline
pipeline.execute()
