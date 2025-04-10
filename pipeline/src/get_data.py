import gdown
import zipfile
from src.utils import PipelineStage

class ExtractStage(PipelineStage):
    def execute(self, data=None):
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
    
    def execute(self, data=None):
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