import gdown
import zipfile
from src.utils import PipelineStage

class ExtractStage(PipelineStage):
    """Download stage for the pipeline.

    Args:
        PipelineStage (obj):  Basic structure for all pipeline stages.
    """
    def execute(self, data=None):
        """Execute the download stage of the pipeline.

        Args:
            None

        Returns:
            str: Name of the downloaded file.
        """
        try:
            file_id = self.config['file_id']
            url = f"https://drive.google.com/uc?id={file_id}"
            output_filename = self.config['output_filename']
            self.logger.info(f"Baixando dados de: {url}")
            gdown.download(url, 
                           output=output_filename, 
                           quiet=False, 
                           use_cookies=True)
            return output_filename
        except Exception as e:
            self.logger.error(f"Erro ao baixar dados: {e}")
            raise

class UnzipStage(PipelineStage):
    """Unzip stage for the pipeline.

    Args:
        PipelineStage (obj):  Basic structure for all pipeline stages.
    """
    
    def execute(self, data=None):
        """Execute unzip stage

        Args:
            None
        Returns:
            str: path to the unzipped files
        """
        self.logger.info(f"Config: {self.config}")
        zipfilename = self.config.get('zipfilename')
        try:
            self.logger.info(f"Descomprimindo: {zipfilename}")
            with zipfile.ZipFile(zipfilename, 'r') as zip_ref:
                zip_ref.extractall(self.config.get('path'))
            return self.config.get('path')
        except Exception as e:
            self.logger.error(f"Erro ao descomprimir: {e}")
            raise