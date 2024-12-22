class selecao_atributos:
    @staticmethod
    def selecao_atributos(diretorio_modelo):
    
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np
        from sklearn.preprocessing import StandardScaler, KBinsDiscretizer
        from sklearn.decomposition import PCA
        from sklearn.model_selection import train_test_split
        from sklearn.feature_selection import SelectFromModel
        from lightgbm import LGBMClassifier
        from sklearn.metrics import accuracy_score
        import statsmodels.api as sm
        from xgboost import XGBClassifier
        import os

        modelo = os.path.join(diretorio_modelo, 'df_modelo.xlsx')
        df = pd.read_excel(modelo)
        df.info()

        dia_atual_de_previsão = df['dt_dia'].max()

        # Criar um DataFrame com o valor máximo 
        df_dia_atual = pd.DataFrame({'dia_atual_de_previsao': [dia_atual_de_previsão]}) 

        # Salvar o DataFrame como CSV 

        df_dia_atual.to_csv(os.path.join(diretorio_modelo, 'dia_atual_previsao.csv'), sep=';', index=False)

        # Analisando o dataframe, vemos que ele foi tratado de forma a não ter nenhum dado faltante.
        # Sobre as séries tem si, é necessário fazer uma análise a parte que será feita para cada uma.

        # Como os atributos da série são séries financeiras, não faz sentido uma análise de outliers, pois os modelos desenvolvidos devem ser capazes de aprender sobre esses outliers.
        # Por isso, o desenvolvimento foi feito para a análise de correlação entre os dados e a série alvo (vlr_fluxo_cambial_bi)
        # Lista com as novas ordens de colunas
        nova_ordem = ['dt_dia', 'vlr_fluxo_cambial_bi'] + [col for col in df.columns if col not in ['dt_dia', 'vlr_fluxo_cambial_bi']]

        # Reordenar o DataFrame
        df1 = df[nova_ordem]

        # Definir 'dt_dia' como índice
        df1.set_index('dt_dia', inplace=True)

        target = 'vlr_fluxo_cambial_bi'
        
        # Seleção dos atributos
        # ARIMAX (AutoRegressive Integrated Moving Average with Exogenous Variables)

        predictors = [col for col in df1.columns if col != target]

        # Função para ajustar ARIMAX e calcular AIC
        def fit_arimax(endog, exog, order=(1, 0, 1)):
            """Ajusta um modelo ARIMAX e retorna o AIC"""
            try:
                model = sm.tsa.ARIMA(endog, order=order, exog=exog).fit()
                return model.aic, model
            except Exception as e:
                return float('inf'), None

        # Forward Stepwise
        def stepwise_forward_selection(data, target, predictors, order=(1, 0, 1)):
            """Realiza seleção de variáveis forward stepwise para ARIMAX"""
            selected = []  # Variáveis selecionadas
            remaining = list(predictors)  # Variáveis disponíveis
            best_aic = float('inf')  # Melhor AIC encontrado
            best_model = None

            while remaining:
                aic_with_candidates = []
                for candidate in remaining:
                    # Ajustar modelo com variável candidata
                    exog = data[selected + [candidate]]
                    aic, model = fit_arimax(data[target], exog, order=order)
                    aic_with_candidates.append((aic, candidate, model))
                
                # Encontrar a melhor variável candidata
                aic_with_candidates.sort()
                best_new_aic, best_candidate, best_candidate_model = aic_with_candidates[0]

                # Verificar se houve melhoria no AIC
                if best_new_aic < best_aic:
                    best_aic = best_new_aic
                    selected.append(best_candidate)
                    remaining.remove(best_candidate)
                    best_model = best_candidate_model
                    print(f"Adicionada variável: {best_candidate}, AIC: {best_aic}")
                else:
                    # Interromper se o AIC não melhorar
                    break

            return selected, best_model

        # Executar a seleção
        selected_variables, final_model = stepwise_forward_selection(
            data=df1, 
            target=target, 
            predictors=predictors
        )

        # Resultados
        print("\nVariáveis Selecionadas:", selected_variables)
        print("Resumo do Modelo Final:")
        print(final_model.summary())

        # Adicionar a variável alvo à lista de colunas selecionadas
        columns_to_keep = selected_variables + ['vlr_fluxo_cambial_bi']

        # Filtrar o DataFrame inicial com as colunas selecionadas
        df_arimax_filtrado = df1[columns_to_keep].reset_index(drop = True)

        caminho_final = os.path.join(diretorio_modelo, 'df_arimax_filtrado.xlsx')
        df_arimax_filtrado.to_excel(caminho_final, index = False)
        
        # LSTM (Long Short-Term Memory)
        
        # Separar variáveis independentes (X) e dependente (y)
        X = df1.drop(columns=['vlr_fluxo_cambial_bi'])  # Remove a variável alvo
        y = df1['vlr_fluxo_cambial_bi']

        # Normalizar os dados
        scaler = StandardScaler()
        X_normalizado = scaler.fit_transform(X)

        # Aplicar PCA, mantendo 99% da variância explicada
        pca = PCA(n_components=0.99, random_state=42)
        X_pca = pca.fit_transform(X_normalizado)

        # Mostrar a quantidade de componentes selecionados
        print(f"Número de componentes selecionados: {X_pca.shape[1]}")

        # Variância explicada por componente
        print("Variância explicada acumulada:", np.cumsum(pca.explained_variance_ratio_))

        # Verificar a contribuição dos atributos originais para os novos componentes
        componentes = pd.DataFrame(pca.components_, columns=X.columns)
        print("Contribuição dos atributos para cada componente principal:")
        componentes.tail()

        # Criar um DataFrame com os componentes principais
        df_lstm = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(X_pca.shape[1])])
        df_lstm['vlr_fluxo_cambial_bi'] = y.reset_index(drop=True)
        df_lstm.tail()

        caminho_final = os.path.join(diretorio_modelo, 'df_lstm.xlsx')
        df_lstm.to_excel(caminho_final, index = False)
        
        # LightGBM
        
        # Separar os dados em features (X) e alvo (y)
        X = df1.drop('vlr_fluxo_cambial_bi', axis=1)
        y = df1['vlr_fluxo_cambial_bi']

        # Dividir em conjunto de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Normalizar os dados

        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Se o alvo é contínuo, discretize-o em classes
        kbins = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')  # Ajuste o número de bins conforme necessário
        y_train_binned = kbins.fit_transform(y_train.values.reshape(-1, 1)).flatten()
        y_test_binned = kbins.transform(y_test.values.reshape(-1, 1)).flatten()

        # Treinamento inicial com LightGBM
        lgbm_model = LGBMClassifier()
        lgbm_model.fit(X_train_scaled, y_train_binned)

        # Avaliação inicial
        y_pred = lgbm_model.predict(X_test_scaled)
        y_pred_binned = kbins.transform(y_pred.reshape(-1, 1)).flatten()  # Transformar previsões para discretizado
        accuracy_initial = accuracy_score(y_test_binned, y_pred_binned)

        # Seleção de atributos com base em feature importance
        sfm = SelectFromModel(lgbm_model, threshold="mean")  # Seleciona features com importância maior ou igual à média
        sfm.fit(X_train_scaled, y_train_binned)

        # Atributos selecionados
        selected_features = X_train.columns[sfm.get_support()]

        # Treinamento com atributos selecionados
        X_train_selected = sfm.transform(X_train_scaled)
        X_test_selected = sfm.transform(X_test_scaled)

        lgbm_model_selected = LGBMClassifier()
        lgbm_model_selected.fit(X_train_selected, y_train_binned)

        # Avaliação com atributos selecionados
        y_pred_selected = lgbm_model_selected.predict(X_test_selected)
        accuracy_selected = accuracy_score(y_test_binned, y_pred_selected)

        print(f"Accuracy inicial com classes discretizadas: {accuracy_initial}")
        print(f"Atributos selecionados: {selected_features}")
        print(f"Accuracy com atributos selecionados: {accuracy_selected}")

        # Filtrar o dataframe com os atributos selecionados
        df_light_gbm = df1[selected_features].reset_index(drop=True)
        df_light_gbm['vlr_fluxo_cambial_bi'] = y.reset_index(drop=True)

        caminho_final = os.path.join(diretorio_modelo, 'df_light_gbm.xlsx')
        df_light_gbm.to_excel(caminho_final, index = False)
        
        # XGBoost
        
        # Discretizar os valores contínuos em intervalos
        y_discretized = pd.cut(y, bins=5, labels=False)

        # Dividir em conjunto de treino e teste 
        X_train, X_test, y_train, y_test = train_test_split(X, y_discretized, test_size=0.2, random_state=42)

        # Normalizar os dados
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Treinamento inicial com XGBoost
        xgb_model = XGBClassifier()
        xgb_model.fit(X_train_scaled, y_train)

        # Avaliação inicial
        y_pred = xgb_model.predict(X_test_scaled)
        accuracy_initial = accuracy_score(y_test, y_pred)

        # Seleção de atributos com base em feature importance
        sfm = SelectFromModel(xgb_model, threshold=0.01)
        sfm.fit(X_train_scaled, y_train)

        # Atributos selecionados
        selected_features = X.columns[sfm.get_support()]

        # Treinamento com atributos selecionados
        X_train_selected = sfm.transform(X_train_scaled)
        X_test_selected = sfm.transform(X_test_scaled)

        xgb_model_selected = XGBClassifier()
        xgb_model_selected.fit(X_train_selected, y_train)

        # Avaliação com atributos selecionados
        y_pred_selected = xgb_model_selected.predict(X_test_selected)
        accuracy_selected = accuracy_score(y_test, y_pred_selected)

        # Exibindo os resultados
        print(f'Accuracy Inicial: {accuracy_initial}')
        print(f'Accuracy com Atributos Selecionados: {accuracy_selected}')
        print(f'Atributos Selecionados: {selected_features}')

        # Filtrar o dataframe com os atributos selecionados
        df_xgboost = df1[selected_features].reset_index(drop = True)
        df_xgboost['vlr_fluxo_cambial_bi'] = y.reset_index(drop=True)
        
        caminho_final = os.path.join(diretorio_modelo, 'df_xgboost.xlsx')
        df_xgboost.to_excel(caminho_final, index = False)