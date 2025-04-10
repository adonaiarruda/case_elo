import pandas as pd
import numpy as np
import os

from src.utils import PipelineStage


class AnalyticsStage(PipelineStage):
    def execute(self, data):
        """Execute the analytics stage of the pipeline.

        Args:
            data (dict): A dictionary containing DataFrames related to the case solution.
        """
        try:
            self.logger.info(f"Executando estágio de análise")

            # Realiza agregações
            df_zcta = self.agregations(data)

            self.logger.info(f"Dados agregados: \n{df_zcta.head()}")
            # monta recomendações
            proposed_zctas = self.make_recomendation(df_zcta, 
                                               data['demographic_data'])
            
            # Exporta resultados
            self.export_recomendations(proposed_zctas)

            return
            
        except Exception as e:
            self.logger.error(f"Erro no estágio de análise: {e}")
            raise

    def agregations(self, data):
        """Perform data aggregations and transformations on analytics data.

        Args:
            data (dict): A dictionary containing DataFrames related to the case solution.

        Returns:
            pd.DataFrame: A DataFrame containing aggregated and transformed data
        """
        try:
            self.logger.info(f"Realizando agregações")

            # Combina custo e receita dos exames
            df_intermediate = pd.merge(
                data['transactional_data'],
                data['exams_data'],
                on='CodItem',
                how='left'
            )
            df_intermediate['exam_profit'] = (df_intermediate['Testing Cost'] - 
                                              df_intermediate['test_price'])
            
            # Combina com dados geográficos
            df_intermediate = pd.merge(
                df_intermediate,
                data['geographic_data'],
                on='Lab Id',
                how='left'
            )

            # Agrega informações de laboratórios e ZCTAs
            df_intermediate = df_intermediate.reset_index().groupby('Geographic Area Name').agg(
                total_services=('Service Id', 'count'),
                total_revenue=('Testing Cost', 'sum'),
                number_of_different_exams=('CodItem', 'count'),
                number_of_patients=('Patient Id', 'nunique'),
                age=('age_at_service', 'median'),
                is_male=('is_male', 'mean'),  
                total_cost=('test_price', 'sum'),
                total_profit=('exam_profit', 'sum'),
                number_of_labs=('Lab Id', 'nunique'),
            ).reset_index()
            

            # Combina informações econômicas
            df_intermediate = pd.merge(df_intermediate, 
                        data['economic_data'][['Geographic Area Name', 
                                               'TotalHouseholds', 
                                               'WeightedMeanIncome']], 
                        on='Geographic Area Name', 
                        how='left')
            # Combina informações demográficas
            df_intermediate = pd.merge(
                df_intermediate,
                data['demographic_data'][
                    [
                        'Geographic Area Name',
                        'TotalPopulation',
                        'male_female_ratio',
                        'MedianAgeInYears'
                    ]
                ],
                on='Geographic Area Name',
                how='left'
            )

            # Transformação logaritma no lucro 
            df_intermediate['total_profit_log'] = np.log(df_intermediate['total_profit'])

            return df_intermediate
    
        except Exception as e:
            self.logger.error(f"Erro ao realizar agregações: {e}")
            raise
    
    def make_recomendation(self, df_zcta, df_demographic):
        """Recommendations ZCTAs to implement new laboratories

        Args:
            df_zcta (pd.dataframe): aggregated data
            df_demographic (pd.dataframe): demographic data

        Returns:
            list: ZCTAs recommended
        """

        try:
            self.logger.info(f"Realizando recomendações")
            # Lógica de recomendação

            # ZCTAs com laboratório implementado
            zctas_with_labs = df_zcta["Geographic Area Name"].unique()

            # ZCTAs com maior população total
            proposed_zctas = df_demographic[
                    ~df_demographic["Geographic Area Name"].isin(zctas_with_labs)
                ].sort_values(
                    "TotalPopulation", ascending=False
                ).head(3)['Geographic Area Name'].tolist()
            
            self.logger.info(f"ZCTAs recomendadas: {proposed_zctas}")

            return proposed_zctas
            
        except Exception as e:
            self.logger.error(f"Erro ao realizar recomendações: {e}")
            raise
    
    def export_recomendations(self, proposed_zctas):
        """Export as txt file

        Args:
            proposed_zctas (list): zctas recommended
        """
        try:

            output_dir = os.path.join(
                self.config.get('pipeline_folder'),
                self.config.get('analytics_data_folder')
            )
            os.makedirs(output_dir, exist_ok=True)

            self.logger.info(f"Exportando recomendações")

            output_path = os.path.join(
                output_dir,
                self.config.get('output_filename')
            )

            with open(output_path, 'w') as f:
                for zcta in proposed_zctas:
                    f.write(f"{zcta}\n")
        
            self.logger.info(f"Recomendações exportadas com sucesso para {self.config.get('output_filename')}")
            return
        except Exception as e:
            self.logger.error(f"Erro ao exportar recomendações: {e}")
            raise