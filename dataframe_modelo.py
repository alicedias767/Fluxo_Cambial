class dataframe_modelo:

    @staticmethod
    def dataframe_modelo(diretorio_final, diretorio_modelo):

        import os
        import pandas as pd
        import numpy as np

        def processar_arquivos(diretorio_final):

            # Listar todos os arquivos no diretório
            arquivos = os.listdir(diretorio_final)
            
            # Filtrar os arquivos que não começam com 'hist_'
            arquivos_para_processar = [arquivo for arquivo in arquivos if not arquivo.startswith('hist_') and arquivo.endswith('.csv')]

            # Dicionário para armazenar os DataFrames
            dataframes = {}

            # Processar cada arquivo
            for arquivo in arquivos_para_processar:
                # Nome do arquivo sem extensão
                nome_dataframe = os.path.splitext(arquivo)[0]

                # Caminho completo do arquivo
                caminho_arquivo = os.path.join(diretorio_final, arquivo)

                try:
                    # Ler o arquivo CSV em um DataFrame
                    df = pd.read_csv(caminho_arquivo, sep=';')

                    # Armazenar o DataFrame no dicionário
                    dataframes[nome_dataframe] = df

                    print(f"Arquivo '{arquivo}' lido com sucesso.")
                except Exception as e:
                    print(f"Erro ao ler o arquivo '{arquivo}': {e}")

            return dataframes

        dataframes = processar_arquivos(diretorio_final)

        # Visualizar os nomes dos DataFrames criados
        print("DataFrames criados:", list(dataframes.keys()))

        # Dataframes Dias Úteis
        # Listo quais são todos os dataframes que tem o período em dias úteis

        acucar = dataframes['acucar']
        boigordo = dataframes['boi_gordo']
        ibovespa = dataframes['ibovespa']
        libra = dataframes['libra']
        milho = dataframes['milho']
        # petroleo = dataframes['petroleo']
        reservas = dataframes['reservas_internacionais']
        selic = dataframes['selic']
        soja = dataframes['soja']
        euro = dataframes['euro']
        dolar = dataframes['dolar']

        list_df_dias = [acucar, boigordo, ibovespa, libra, milho, reservas, selic, soja, euro, dolar]

        def unir_dataframes(lista_dataframes):

            # Começar com o primeiro DataFrame
            df_unificado = lista_dataframes[0]
            
            # Iterar pelos demais DataFrames na lista
            for df in lista_dataframes[1:]:
                df_unificado = pd.merge(df_unificado, df, on='dt_dia', how='inner')
            
            return df_unificado
        
        # Unir todos os DataFrames

        df_dias = unir_dataframes(list_df_dias)

        # Dataframes semanais
        fluxocambial = dataframes['fluxo_cambial']

        y = fluxocambial

        # Dataframes mensais
        fedfunds = dataframes['fedfunds']
        minerio_ferro = dataframes['minerio_ferro']
        usphci = dataframes['usphci']
        ipca = dataframes['ipca']
        pib_brasil = dataframes['pib']
        viagens = dataframes['viagens']
        balanca = dataframes['balanca_pagamentos']

        list_mes = [fedfunds, minerio_ferro, usphci, ipca, pib_brasil, viagens, balanca]

        # Unir todos os DataFrames

        df_mes = unir_dataframes(list_mes)
        # Dataframes anuais
        inflacao_china = dataframes['inflacao_china']
        inflacao_eua = dataframes['inflacao_eua']
        inflacao_europa = dataframes['inflacao_europa']
        pib_china = dataframes['pib_china']
        pib_eua = dataframes['pib_eua']
        pib_europa = dataframes['pib_europa']
        list_ano = [inflacao_china, inflacao_eua, inflacao_europa, pib_china, pib_eua, pib_europa]

        # Unir todos os DataFrames

        df_ano = unir_dataframes(list_ano)

        # Tratando os dataframes
        # Para os arquivos que estão em frequências de dia útil, vamos trazer o fluxo cambial como um join left para pegar em quais tiveram anúncio do fluxo cambial

        df1 = pd.merge(df_dias, y, on = 'dt_dia', how='left')

        # Obter a data mínima e máxima
        data_minima = y['dt_dia'].min()
        data_maxima = y['dt_dia'].max()
        df2 = df1[(df1['dt_dia'] >= data_minima) & (df1['dt_dia'] <= data_maxima)]

        # Identificar índices com valores não nulos de `vlr_fluxo_cambial_bi`
        valid_indices = df2[df2['vlr_fluxo_cambial_bi'].notna()].index

        # Lista inicial com as colunas a serem processadas
        colunas_a_processar = [col for col in df2.columns if col not in ['dt_dia', 'vlr_fluxo_cambial_bi']]

        # Gerando colunas para os dias que há divulgação do Fluxo cambial

        ################# MÉDIA ############################

        # Ordenar o DataFrame pela data
        df2 = df2.sort_values(by='dt_dia')

        # Função para calcular a média com base nos dias válidos
        def calcular_media(df, colunas, indices):
            for col in colunas:
                col_mean = []
                for idx in indices:
                    dia_atual = df.loc[idx, 'dt_dia']
                    idx_anterior = df.loc[df['dt_dia'] < dia_atual, 'vlr_fluxo_cambial_bi'].last_valid_index()
                    
                    if idx_anterior is not None:  # Verificação de índice anterior válido
                        dias_validos = df.loc[idx_anterior+1:idx, 'dt_dia'].tolist()
                        media = df.loc[df['dt_dia'].isin(dias_validos), col].mean()
                        col_mean.append(media)
                    else:
                        col_mean.append(None)  # Adicionar None se não houver índice anterior válido
                
                df[f'{col}_mean'] = pd.Series(col_mean, index=indices)

        # Calcular a média para cada coluna a processar
        calcular_media(df2, colunas_a_processar, valid_indices)

        ##################### MÁXIMA ##############################

        # Ordenar o DataFrame pela data
        df2 = df2.sort_values(by='dt_dia')

        # Função para calcular a média com base nos dias válidos
        def calcular_maxima(df, colunas, indices):
            for col in colunas:
                col_mean = []
                for idx in indices:
                    dia_atual = df.loc[idx, 'dt_dia']
                    idx_anterior = df.loc[df['dt_dia'] < dia_atual, 'vlr_fluxo_cambial_bi'].last_valid_index()
                    
                    if idx_anterior is not None:  # Verificação de índice anterior válido
                        dias_validos = df.loc[idx_anterior+1:idx, 'dt_dia'].tolist()
                        media = df.loc[df['dt_dia'].isin(dias_validos), col].max()
                        col_mean.append(media)
                    else:
                        col_mean.append(None)  # Adicionar None se não houver índice anterior válido
                
                df[f'{col}_max'] = pd.Series(col_mean, index=indices)

        # Calcular a média para cada coluna a processar
        calcular_maxima(df2, colunas_a_processar, valid_indices)

        ###################### MÍNIMA ################################

        # Ordenar o DataFrame pela data
        df2 = df2.sort_values(by='dt_dia')

        # Função para calcular a média com base nos dias válidos
        def calcular_minima(df, colunas, indices):
            for col in colunas:
                col_mean = []
                for idx in indices:
                    dia_atual = df.loc[idx, 'dt_dia']
                    idx_anterior = df.loc[df['dt_dia'] < dia_atual, 'vlr_fluxo_cambial_bi'].last_valid_index()
                    
                    if idx_anterior is not None:  # Verificação de índice anterior válido
                        dias_validos = df.loc[idx_anterior+1:idx, 'dt_dia'].tolist()
                        media = df.loc[df['dt_dia'].isin(dias_validos), col].min()
                        col_mean.append(media)
                    else:
                        col_mean.append(None)  # Adicionar None se não houver índice anterior válido
                
                df[f'{col}_min'] = pd.Series(col_mean, index=indices)

        # Calcular a média para cada coluna a processar
        calcular_minima(df2, colunas_a_processar, valid_indices)

        # Com isso temos o dataframe com as seguintes colunas:

        # 1. Valores das features no dia de anúncio (valor real da feature);
        # 2. Valores das médias entre os dias de anúncio, incluindo o dia do anúncio das features (médias das features);
        # 3. Valores máximo entre os dias de anúncio, incluindo o dia do anúncio das features (máximo das features);
        # 4. Valores mínimo entre os dias de anúncio, incluindo o dia do anúncio das features (mínimo das features);

        # Ajustando o dataframe mensal
        # Gerar todas as datas diárias entre o mínimo e o máximo 
        min_date = df_mes['dt_dia'].min() 
        max_date = df_mes['dt_dia'].max() 

        all_dates = pd.date_range(start=min_date, end=max_date, freq='D') 
        df_mes['dt_dia'] = pd.to_datetime(df_mes['dt_dia'], format = '%Y-%m-%d')

        # Reindexar o DataFrame para incluir todas as datas e propagar os valores mensais 
        df_mes_2 = df_mes.set_index('dt_dia').reindex(all_dates, method='ffill').reset_index() 
        df_mes_2.rename(columns={'index': 'dt_dia'}, inplace=True)

        # Ajustando o dataframe Anual
        # Gerar todas as datas diárias entre o mínimo e o máximo 

        min_date = df_ano['dt_dia'].min() 
        max_date = df_ano['dt_dia'].max() 

        all_dates = pd.date_range(start=min_date, end=max_date, freq='D') 
        df_ano['dt_dia'] = pd.to_datetime(df_ano['dt_dia'], format = '%Y-%m-%d')

        # Reindexar o DataFrame para incluir todas as datas e propagar os valores mensais 
        df_ano_2 = df_ano.set_index('dt_dia').reindex(all_dates, method='ffill').reset_index() 
        df_ano_2.rename(columns={'index': 'dt_dia'}, inplace=True)

        # Unindo os Dataframes
        list_dfs = [df2, df_mes_2, df_ano_2]
        df_mes_2['dt_dia'] = df_mes_2['dt_dia'].astype(str)
        df_ano_2['dt_dia'] = df_ano_2['dt_dia'].astype(str)

        # Unir todos os DataFrames

        df_3 = pd.merge(df2, df_mes_2, on='dt_dia', how='left')
        df_4 = pd.merge(df_3, df_ano_2, on='dt_dia', how='left')

        # Dropando NA segundo a série do vlr_fluxo_cambial_bi e dando ffill() para os valores restantes
        # Dropar linhas onde 'vlr_fluxo_cambial_bi' é NA e aplicar ffill() nas demais colunas 

        df_4.dropna(subset=['vlr_fluxo_cambial_bi'], inplace=True)
        df_4.ffill(inplace=True)
        df_4.bfill(inplace=True)

        # ids = df_4["dt_dia"]
        # df_4[ids.isin(ids[ids.duplicated()])].sort_values("dt_dia")

        # Salvando o dataframe resultante em arquivo no diretório escolhido

        caminho_final = os.path.join(diretorio_modelo, 'df_modelo.xlsx')
        df_4.to_excel(caminho_final, index = False)

        print('Dataframe com as features expandidas e tratadas criado com sucesso!')
