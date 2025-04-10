from src.utils import PipelineStage
import os
import pandas as pd
import numpy as np

class CleaningStage(PipelineStage):
    def execute(self, data=None):
        """Execute the cleaning stage of the pipeline.            

        Returns:
            dict: A dictionary containing the cleaned DataFrames related to the case solution.
        """
        try:
            # Lógica de limpeza de dados
            self.logger.info("Iniciando limpeza de dados")

            # Importa dados
            data = self.import_data()
            # Limpa dados transacionais
            data['transactional_data'] = self.clean_transactional_data(data['transactional_data'])

            # Limpa dados de exames
            data['exams_data'] = self.clean_exams_data(data['exams_data'])

            # Limpa dados demográficos
            data['demographic_data'] = self.clean_demographic_data(data['demographic_data'])

            # Limpa dados econômicos
            data['economic_data'] = self.clean_economic_data(data['economic_data'])
            
            # Limpa dados geográficos
            data['geographic_data'] = self.clean_geographic_data(data['geographic_data'])

            self.logger.info("Limpeza de dados concluída com sucesso")

            return data
        except Exception as e:
            self.logger.error(f"Erro ao limpar dados: {e}")
            raise

    def read_csv(self, filename, sep=',', index_col=None):
        """ standartize reading csv files

        Args:
            filename (str): file to read
            sep (str, optional): ; or ,. default = ','.
            index_col (int, optional): index column. Default = None.

        Returns:
            pd.dataframe: loaded dataframe
        """
        try:
            self.logger.info(f"Lendo arquivo: {filename}")
            filepath = os.path.join(self.config.get('pipeline_folder'),
                                         self.config.get('raw_data_folder'),
                                         filename
                                         )
            
            df = pd.read_csv(filepath, 
                             sep=sep, 
                             index_col=index_col)
            return df
        
        except Exception as e:
            self.logger.error(f"Erro ao ler o arquivo {filename}: {e}")
            raise

    def import_data(self):
        """Import data used in the case solution

        Returns:
            dict: A dictionary containing DataFrames related to the case solution.
        """
        try:
            data = {}
            data['transactional_data'] = self.read_csv(self.config.get('transactional_filename'), 
                                                       sep=';')
            data['exams_data'] = self.read_csv(self.config.get('exams_filename'), 
                                               index_col=0)
            data['economic_data'] = self.read_csv(self.config.get('economics_filename'),
                                                   index_col=0)
            data['geographic_data'] = self.read_csv(self.config.get('geographic_filename'),
                                                   index_col=0)
            data['demographic_data'] = self.read_csv(self.config.get('demographics_filename'),
                                                     index_col=0)

            return data

        except Exception as e:
            self.logger.error(f"Erro ao importar dados: {e}")
            raise
            
    def clean_transactional_data(self, df_transactional):
        """Clean transactional data int the pipeline

        Args:
            df_transactional (pd.Dataframe): Transactional data

        Returns:
            pd.DataFrame: Cleaned transactional data
        """
        try:
            # Gênero
            df_transactional = df_transactional[df_transactional["Gender"] != 'I']
            df_transactional['is_male'] = df_transactional["Gender"] == 'M'
            # Testing costs
            df_transactional['Testing Cost'] = df_transactional['Testing Cost'].str.replace(',',
                                                                                            '.').astype(float)
            # Datas
            df_transactional["Date of birth"] = pd.to_datetime(df_transactional["Date of birth"], 
                                                                    format='%d/%m/%Y %H:%M:%S', 
                                                                    errors='coerce')
            df_transactional["Date of service"] = pd.to_datetime(df_transactional["Date of service"], 
                                                                      format='%Y-%m-%d', 
                                                                      errors='coerce')
            df_transactional["Date of birth"].fillna(df_transactional['Date of birth'].median(), 
                                                          inplace=True)
            df_transactional['age_at_service'] = (df_transactional['Date of service'].dt.year - 
                                                       df_transactional['Date of birth'].dt.year).astype(int)
            
            df_transactional.loc[df_transactional['age_at_service'] > 110, 
                                 'age_at_service'] = 108

            # reduzir dados desnecessários para reduzir tamanho na memória
            df_transactional.drop(['Date of birth'], axis=1, inplace=True)
            df_transactional.drop(['Date of service'], axis=1, inplace=True)
            df_transactional.drop(['Gender'], axis=1, inplace=True)
            return df_transactional
        except Exception as e:
            self.logger.error(f"Erro ao limpar dados transacionais: {e}")
            raise

    def clean_exams_data(self, df_exams):
        """Clean exams data in the pipeline

        Args:
            df_exams (pd.Dataframe): Data from exams

        Returns:
            pd.DataFrame: Cleaned exams data
        """
        try:
            df_exams.drop(['Category'], axis=1, inplace=True)
            df_exams.drop(['Desc Item'], axis=1, inplace=True)

            df_exams.rename(columns={'Testing Cost': 'test_price'}, inplace=True)
        
            return df_exams

        except Exception as e:
            self.logger.error(f"Erro ao limpar dados de exames: {e}")
            raise

    def clean_demographic_data(self, df_demographic):
        """Clean exams data in the pipeline

        Args:
            df_exams (pd.Dataframe): Data from exams

        Returns:
            pd.DataFrame: Cleaned exams data
        """
        try: 
            # Limpeza de dados demográficos
            # Remove áreas sem população
            df_demographic = df_demographic[df_demographic["TotalPopulation"] > 10]
            
            # Gênero
            sex_ratio_median = df_demographic["SexRatio(males per 100 females)"].median()
            df_demographic["SexRatio(males per 100 females)"].fillna(sex_ratio_median, 
                                                                    inplace=True)
            # Winsorization
            lower_limit = np.percentile(df_demographic['SexRatio(males per 100 females)'], 2)
            upper_limit = np.percentile(df_demographic['SexRatio(males per 100 females)'], 98)
            df_demographic['SexRatio(males per 100 females)'] = np.clip(df_demographic['SexRatio(males per 100 females)'], 
                                                                            lower_limit, 
                                                                            upper_limit)
            
            # Idade 
            age_ranges = {
                "Population_Under5Years": 2.5,
                "Population_5to9Years": 7.5,
                "Population_10to14Years": 12.5,
                "Population_15to19Years": 17.5,
                "Population_20to24Years": 22.5,
                "Population_25to34Years": 30,
                "Population_35to44Years": 40,
                "Population_45to54Years": 50,
                "Population_55to59Years": 57.5,
                "Population_60to64Years": 62.5,
                "Population_65to74Years": 70,
                "Population_75to84Years": 80,
                "Population_85YearsAndOver": 90
            }
            # Calcular a média ponderada
            weighted_sum = sum(df_demographic[age_range] * weight for age_range, weight in age_ranges.items())
            mean_age = weighted_sum / df_demographic["TotalPopulation"]
            df_demographic["MedianAgeInYears"].fillna(mean_age, inplace=True)

            # renomeando colunas para facilitar análise
            df_demographic.rename(columns={"SexRatio(males per 100 females)": "male_female_ratio",
                                            "GeographicAreaName": "Geographic Area Name"
            }, inplace=True)

            return df_demographic
        except Exception as e:
            self.logger.error(f"Erro ao limpar dados demográficos: {e}")
            raise
    
    def clean_economic_data(self, df_economic):
        try:
            # Limpeza de dados econômicos
            # Remove duplicatas
            df_economic = df_economic.drop_duplicates()

            # total de residências
            households_info_columns = list(df_economic.columns)
            households_info_columns.remove('Geographic Area Name')
            households_info_columns.remove('id')

            df_economic["TotalHouseholds"] =  df_economic[households_info_columns].sum(axis=1)

            df_economic = df_economic[df_economic["TotalHouseholds"] > 0]

            # Receita média
            households_income_median_ranges = {
                "TotalHouseholds_LessThan$10.000": 5000,
                "TotalHouseholds_$10.000to$14.999": 12500,
                "TotalHouseholds_$15.000to$24.999": 20000,
                "TotalHouseholds_$25.000to$34.999": 30000,
                "TotalHouseholds_$35.000to$49.999": 42500,
                "TotalHouseholds_$50.000to$74.999": 62000,
                "TotalHouseholds_$75.000to$99.999": 87000,
                "TotalHouseholds_$100.000to$149.999": 125000,
                "TotalHouseholds_$150.000to$199.999": 175000,
                "TotalHouseholds_$200.000OrMore": 300000
            }
            # Calcular a média ponderada
            weighted_sum = sum(df_economic[income_range] * weight for income_range, weight in households_income_median_ranges.items())
            mean_income = weighted_sum / df_economic["TotalHouseholds"]
            df_economic["WeightedMeanIncome"] = mean_income

            # Normalização
            df_economic[households_info_columns] = df_economic[households_info_columns].div(df_economic["TotalHouseholds"], axis=0)


            # reduzir numero de casas decimais
            df_economic[households_info_columns] = df_economic[households_info_columns].round(4)
            df_economic["WeightedMeanIncome"] = df_economic["WeightedMeanIncome"].round(4)

            return df_economic
        except Exception as e:
            self.logger.error(f"Erro ao limpar dados econômicos: {e}")
            raise
    def clean_geographic_data(self, df_geographic):
        try:
            # Remove NAs
            df_geographic = df_geographic.dropna(subset=['Zipcode'])

            # Transformação de ZCTAs
            df_geographic["Geographic Area Name"] = df_geographic["Zipcode"].apply(lambda x: 
                                                       f"ZCTA5 {int(x):05d}" 
                                                       if pd.notna(x) else x)

            return df_geographic
        except Exception as e:
            self.logger.error(f"Erro ao limpar dados geográficos: {e}")
            raise