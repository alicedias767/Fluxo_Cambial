class previsoes:
    @staticmethod
    def previsoes(diretorio_modelo, diretorio_output):

        import os
        import numpy as np
        import pandas as pd
        import statsmodels as sm
        import matplotlib.pyplot as plt
        from statsmodels.tsa.arima_process import arma_generate_sample
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
        from statsmodels.tsa.seasonal import seasonal_decompose
        from matplotlib import pyplot
        from pmdarima import auto_arima
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        from sklearn.model_selection import train_test_split
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        from tensorflow.keras.layers import LSTM
        from sklearn.preprocessing import MinMaxScaler
        from tensorflow.keras.layers import LSTM, Dense
        from statsmodels.tsa.stattools import adfuller
        from xgboost import XGBRegressor
        import lightgbm as lgb

        # Função para salvar gráficos
        def salvar_grafico(fig, caminho_pasta, nome_arquivo):
            if not os.path.exists(caminho_pasta):
                os.makedirs(caminho_pasta)
            fig.savefig(os.path.join(caminho_pasta, nome_arquivo), bbox_inches='tight')

        path_arimax = os.path.join(diretorio_modelo, 'df_arimax_filtrado.xlsx')
        path_lstm = os.path.join(diretorio_modelo, 'df_lstm.xlsx')
        path_lightgbm = os.path.join(diretorio_modelo, 'df_light_gbm.xlsx')
        path_xgboost = os.path.join(diretorio_modelo, 'df_xgboost.xlsx')

        df_arimax = pd.read_excel(path_arimax)
        df_lstm = pd.read_excel(path_lstm)
        df_lightgbm = pd.read_excel(path_lightgbm)
        df_xgboost = pd.read_excel(path_xgboost)

        ###################################################################################################
        #                                              ARIMAX                                             #
        ###################################################################################################
        # Coluna alvo
        coluna_alvo = 'vlr_fluxo_cambial_bi' 

        # Encontrar colunas diferentes da coluna de referência
        colunas_diferentes = df_arimax.columns[df_arimax.ne(df_arimax[coluna_alvo], axis=0).any()] 

        # Filtrar o DataFrame pelas colunas diferentes 
        X = df_arimax[colunas_diferentes] # Variáveis exógenas

        y = df_arimax['vlr_fluxo_cambial_bi']  # Variável alvo
        
        series = pd.Series(y)

        # 1. Análise visual
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(series, label="Série Temporal")
        ax.set_title("Série Temporal com Tendência")
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "arimax_serie_temporal_tendencia.png")

        # 2. Função para executar o teste ADF
        def adf_test(series, alpha=0.05):
            result = adfuller(series)
            print("Teste de Dickey-Fuller Aumentado (ADF):")
            print(f"Estatística ADF: {result[0]:.4f}")
            print(f"Valor-p: {result[1]:.4f}")
            print(f"Número de Lags Utilizados: {result[2]}")
            print(f"Número de Observações: {result[3]}")
            for key, value in result[4].items():
                print(f"Valor Crítico {key}: {value:.4f}")
            if result[1] < alpha:
                print("Conclusão: Rejeitamos H0. A série é estacionária.")
            else:
                print("Conclusão: Não rejeitamos H0. A série não é estacionária.")

        # Executando o teste ADF
        adf_test(series)

        # 3. Transformação para estacionariedade (Differencing)
        series_diff = series.diff().dropna()

        # Plot da Série Estacionarizada
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(series_diff, label="Série Após Differencing")
        ax.set_title("Série Temporal Estacionarizada")
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "arimax_serie_temporal_estacionaria.png")

        # Dividir os dados em treinamento e teste
        # Definindo o tamanho do conjunto de teste
        tamanho_teste = 30

        # Divisão dos dados
        x_treino, x_teste = X[:-tamanho_teste], X[-tamanho_teste:]
        y_treino, y_teste = y[:-tamanho_teste], y[-tamanho_teste:]

        # Exibindo as formas dos dados divididos
        x_treino.shape, x_teste.shape, y_treino.shape, y_teste.shape

        # Ajustando o modelo ARIMA com variáveis exógenas

        stepwise_fit = auto_arima(y_treino, exogenous=x_treino,
                                start_p=0, start_q=0,
                                max_p=4, max_q=4,
                                seasonal=False, d=None, trace=True,
                                error_action='ignore', suppress_warnings=True,
                                stepwise=True)
        
        # Sumário do modelo
        print(stepwise_fit.summary())

        # Previsão com o modelo ARIMA (SARIMAX) usando as variáveis exógenas
        model = SARIMAX(y_treino, exog=x_treino,
                        order=stepwise_fit.order,   
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        
        # Ajustando o modelo
        model_fit = model.fit(disp=False)

        # Fazendo previsões para o conjunto de teste
        previsoes = model_fit.forecast(steps=len(y_teste), exog=x_teste)

        # Visualizando os resultados
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(y_treino, label='Treino')
        ax.plot(y_teste.index, y_teste, label='Teste')
        ax.plot(y_teste.index, previsoes, label='Previsão')
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "arimax_previsão_teste.png")

        # Prevendo o próximo ponto com base nos últimos dados
        proxima_previsao_arimax = model_fit.forecast(steps=1, exog=[X.iloc[-1].values])

        print(f"Previsão para o próximo ponto: {proxima_previsao_arimax.iloc[0].round(2)} Bilhões")

        # Cálculo de MAE e MSE
        mae_arimax = mean_absolute_error(y_teste, previsoes)
        mse_arimax = mean_squared_error(y_teste, previsoes)

        print(f"Mean Absolute Error (MAE) - ARIMAX: {mae_arimax}")
        print(f"Mean Squared Error (MSE) - ARIMAX: {mse_arimax}")

        ###################################################################################################
        #                                              LSTM                                               #
        ###################################################################################################

        df = df_lstm.copy()

        # Normalizando os dados (exceto a coluna de índice, se houver)
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df.values)

        # Convertendo os dados normalizados de volta para um DataFrame
        scaled_df = pd.DataFrame(scaled_data, columns=df.columns, index=df.index)

        # Função para criar sequências
        def create_sequences(data, target_col, sequence_length):
            X, y = [], []
            for i in range(len(data) - sequence_length):
                X.append(data[i:i+sequence_length, :-1])  # Todas as colunas menos a alvo
                y.append(data[i+sequence_length, target_col])  # Próximo valor da coluna alvo
            return np.array(X), np.array(y)
        
        # Configurando o tamanho da janela de observação (30 semanas)
        sequence_length = 30
        target_col = df.columns.get_loc("vlr_fluxo_cambial_bi")  # Índice da coluna alvo

        # Criando as sequências
        X, y = create_sequences(scaled_data, target_col, sequence_length)

        # Dividindo em treino e teste
        train_size = int(len(X) * 0.9)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Construindo o modelo LSTM
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25, activation='relu'))
        model.add(Dense(1))
        
        # Compilando o modelo
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Treinando o modelo
        history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test), shuffle=False)

        # Fazendo previsões no conjunto de teste
        y_pred = model.predict(X_test)

        # Revertendo a normalização para os valores reais
        y_test_rescaled = scaler.inverse_transform(np.concatenate((X_test[:, -1, :], y_test.reshape(-1, 1)), axis=1))[:, -1]
        y_pred_rescaled = scaler.inverse_transform(np.concatenate((X_test[:, -1, :], y_pred), axis=1))[:, -1]

        # Visualizando os resultados
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(y_test_rescaled, label="Valores Reais")
        ax.plot(y_pred_rescaled, label="Previsões LSTM")
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "lstm_previsoes_1.png")

        # Fazendo a previsão do próximo valor
        last_sequence = scaled_data[-sequence_length:, :-1]  # Última sequência para prever o próximo
        last_sequence = np.expand_dims(last_sequence, axis=0)  # Ajustando para a entrada do modelo

        next_prediction = model.predict(last_sequence)
        next_prediction_rescaled_lstm_1 = scaler.inverse_transform(np.concatenate((last_sequence[0, -1, :], next_prediction), axis=None).reshape(1, -1))[:, -1]

        print(f"Previsão para o próximo valor: {next_prediction_rescaled_lstm_1[0].round(2)} Bilhões")

        # Cálculo de MAE e MSE
        mae_lstm_1 = mean_absolute_error(y_test_rescaled, y_pred_rescaled)
        mse_lstm_1 = mean_squared_error(y_test_rescaled, y_pred_rescaled)

        print(f"Mean Absolute Error (MAE): {mae_lstm_1}")
        print(f"Mean Squared Error (MSE): {mse_lstm_1}")

        # Reavaliando os parâmetros e fazendo novas previsões

        # Testando diferentes parâmetros para a LSTM
        melhor_mae_lstm = float('inf')
        melhor_parametros_lstm = None

        for units in [25, 50, 75]:
            for batch_size in [16, 32]:
                for layers in [1, 2]:  # Número de camadas LSTM
                    try:
                        model = Sequential()
                        for _ in range(layers):
                            model.add(LSTM(units, return_sequences=True if layers > 1 else False, input_shape=(X_train.shape[1], X_train.shape[2])))
                        model.add(Dense(25, activation='relu'))
                        model.add(Dense(1))
                        
                        model.compile(optimizer='adam', loss='mean_squared_error')
                        model.fit(X_train, y_train, epochs=10, batch_size=batch_size, verbose=0, shuffle=False)
                        
                        y_pred = model.predict(X_test)
                        y_pred_rescaled = scaler.inverse_transform(
                            np.concatenate((X_test[:, -1, :], y_pred), axis=1))[:, -1]
                        
                        mae = mean_absolute_error(y_test_rescaled, y_pred_rescaled)
                        
                        if mae < melhor_mae_lstm:
                            melhor_mae_lstm = mae
                            melhor_parametros_lstm = (units, batch_size, layers)
                    except Exception as e:
                        print(f"Erro com parâmetros (units={units}, batch_size={batch_size}, layers={layers}): {e}")

        print(f"Melhores parâmetros: {melhor_parametros_lstm} com MAE: {melhor_mae_lstm}")

        # Reconstruindo o modelo com os melhores parâmetros
        if melhor_parametros_lstm:
            units, batch_size, trash = melhor_parametros_lstm
            final_model = Sequential()
            final_model.add(LSTM(units, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
            final_model.add(LSTM(units, return_sequences=False))
            final_model.add(Dense(25, activation='relu'))
            final_model.add(Dense(1))
            
            final_model.compile(optimizer='adam', loss='mean_squared_error')
            final_model.fit(X_train, y_train, epochs=20, batch_size=batch_size, shuffle=False)
            
            # Avaliação final
            y_pred = final_model.predict(X_test)
            y_pred_rescaled = scaler.inverse_transform(
                np.concatenate((X_test[:, -1, :], y_pred), axis=1))[:, -1]
            
            mae_final_lstm = mean_absolute_error(y_test_rescaled, y_pred_rescaled)
            mse_final_lstm = mean_squared_error(y_test_rescaled, y_pred_rescaled)

            # Fazendo a previsão do próximo valor com o modelo final
            last_sequence = scaled_data[-sequence_length:, :-1]  # Última sequência para prever o próximo
            last_sequence = np.expand_dims(last_sequence, axis=0)  # Ajustando para a entrada do modelo
            next_prediction = final_model.predict(last_sequence)
            next_prediction_rescaled_2 = scaler.inverse_transform(
            np.concatenate((last_sequence[0, -1, :], next_prediction), axis=None).reshape(1, -1))[:, -1]

        # Visualizando os resultados
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(y_test_rescaled, label="Valores Reais")
        ax.plot(y_pred_rescaled, label="Previsões LSTM")
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "lstm_previsoes_2.png")

        print(f"Modelo final - MAE: {mae_final_lstm}, MSE: {mse_final_lstm}")
        print(f"Previsão para o próximo valor (modelo final): {next_prediction_rescaled_2[0].round(2)} Bilhões")

        ###################################################################################################
        #                                           LIGHT GBM                                             #
        ###################################################################################################

        df = df_lightgbm.copy()

        # Configuração do tamanho da janela deslizante (exemplo: 30 observações passadas)
        window_size = 30

        # Função para criar janelas deslizantes
        def create_features_and_labels(data, target_col, window_size):
            X, y = [], []
            for i in range(len(data) - window_size):
                X.append(data[i:i + window_size, :-1])  # Todas as colunas menos a target
                y.append(data[i + window_size, target_col])  # Próximo valor da coluna alvo
            return np.array(X), np.array(y)
        
        # Preparando os dados
        target_col = df.columns.get_loc("vlr_fluxo_cambial_bi")
        X, y = create_features_and_labels(df.values, target_col, window_size)

        # Ajustando para o formato esperado pelo LightGBM
        X = X.reshape(X.shape[0], -1)  # Transformando em formato 2D

        # Divisão em treino e teste (90% treino, 10% teste)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        # Criando Dataset do LightGBM
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_valid = lgb.Dataset(X_test, y_test, reference=lgb_train)

        # Parâmetros do modelo
        params = {
            'objective': 'regression',
            'metric': 'mae',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.1,
            'feature_fraction': 0.8,
            'seed': 42
        }

        # Configuração manual do early stopping
        num_boost_round = 1000
        early_stopping_rounds = 10
        best_score = float("inf")
        best_iteration = 0

        # Loop manual de validação cruzada
        cv_results = []
        for i in range(num_boost_round):
            model = lgb.train(
                params,
                lgb_train,
                num_boost_round=i + 1,
                valid_sets=[lgb_train, lgb_valid]
            )
            valid_score = model.best_score['valid_1']['l1']
            cv_results.append(valid_score)

            if valid_score < best_score:
                best_score = valid_score
                best_iteration = i + 1
            elif i - best_iteration >= early_stopping_rounds:
                print(f"Parando no round {i + 1} devido ao early stopping.")
                break

        print(f"Melhor número de iterações: {best_iteration}")
        print(f"Melhor score de validação: {best_score}")

        # Treinando o modelo final com o número ideal de iterações
        model = lgb.train(
            params,
            lgb_train,
            num_boost_round=best_iteration
        )

        # Fazendo previsões no conjunto de teste
        y_pred = model.predict(X_test)

        # Avaliando o modelo
        mae_lgb = mean_absolute_error(y_test, y_pred)
        mse_lgb = mean_squared_error(y_test, y_pred)

        print(f"Mean Absolute Error (MAE) - LightGBM: {mae_lgb}")
        print(f"Mean Squared Error (MSE) - LightGBM: {mse_lgb}")

        # Visualizando os resultados
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(y_test, label="Valores Reais")
        ax.plot(y_pred, label="Previsões LightGBM")
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "lightgbm_previsoes.png")

        # Fazendo previsão do próximo valor
        last_sequence = df.values[-window_size:, :-1]  # Última janela deslizante
        next_prediction_lgb = model.predict(last_sequence.reshape(1, -1))

        print(f"Previsão para o próximo valor: {next_prediction_lgb[0].round(2)} Bilhões")

        ###################################################################################################
        #                                           XGBoost                                               #
        ###################################################################################################

        # Supondo que df_final seja o DataFrame com os dados após PCA
        df = df_xgboost.copy()

        # Configuração do tamanho da janela deslizante (exemplo: 30 observações passadas)
        window_size = 30

        # Função para criar janelas deslizantes
        def create_features_and_labels(data, target_col, window_size):
            X, y = [], []
            for i in range(len(data) - window_size):
                X.append(data[i:i + window_size, :-1])  # Todas as colunas menos a target
                y.append(data[i + window_size, target_col])  # Próximo valor da coluna alvo
            return np.array(X), np.array(y)
        
        # Preparando os dados
        target_col = df.columns.get_loc("vlr_fluxo_cambial_bi")
        X, y = create_features_and_labels(df.values, target_col, window_size)

        # Ajustando para o formato esperado pelo XGBoost
        X = X.reshape(X.shape[0], -1)  # Transformando em formato 2D

        # Divisão em treino e teste (90% treino, 10% teste)
        train_size = int(len(X) * 0.9)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Criando e treinando o modelo XGBoost
        xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
        xgb_model.fit(X_train, y_train)

        # Fazendo previsões no conjunto de teste
        y_pred = xgb_model.predict(X_test)

        # Avaliando o modelo
        mae_xgb = mean_absolute_error(y_test, y_pred)
        mse_xgb = mean_squared_error(y_test, y_pred)

        print(f"Mean Absolute Error (MAE) - XGBoost: {mae_xgb}")
        print(f"Mean Squared Error (MSE) - XGBoost: {mse_xgb}")

        # Visualizando os resultados
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(y_test, label="Valores Reais")
        ax.plot(y_pred, label="Previsões XGBoost")
        ax.legend()

        # Salvar o gráfico
        salvar_grafico(fig, diretorio_output, "xgboost_previsoes.png")

        # Fazendo previsão do próximo valor
        last_sequence = df.values[-window_size:, :-1]  # Última janela deslizante
        next_prediction = xgb_model.predict(last_sequence.reshape(1, -1))

        # Arredondando o resultado para 2 casas decimais
        predicted_value_rounded = np.round(next_prediction[0], 2)

        print(f"Previsão para o próximo valor: {predicted_value_rounded.round(2)} Bilhões")


        print('\n\n\n\n\n\n --------------------- Resultados Finais dos Modelos -------------------------------------')

        df_dia_atual = pd.read_csv(os.path.join(diretorio_modelo, 'dia_atual_previsao.csv'), sep = ';')
        print(f'O dia máximo do Dataframe é {df_dia_atual['dia_atual_de_previsao'].max()}')
        print('Portanto a previsão é para o próximo dia que está na tabela do Fluxo Cambial no site da Investing')

        print('\n ------------------------------ Resultados ARIMAX --------------------------------------------')
        # A previsão é uma Series; para acessar o valor, use .iloc[0] para obter o primeiro elemento

        # Executando o teste ADF
        print('Verificando estacionariedade da série')
        adf_test(series)

        # Printando as informações do modelo escolhido pelo auto_arima
        print("\nModelo escolhido:", stepwise_fit.order)

        print('\nResultados e previsões do ARIMAX:')

        print(f"Previsão para o próximo ponto: {proxima_previsao_arimax.iloc[0].round(2)} Bilhões")
        print(f"Mean Absolute Error (MAE) - ARIMAX: {mae_arimax}")
        print(f"Mean Squared Error (MSE) - ARIMAX: {mse_arimax}")

        print('\n ------------------------------ Resultados LSTM --------------------------------------------')
        
        print('\nResultados e previsões do LSTM antes da revisão dos parâmetros')
        print(f"Previsão para o próximo valor: {next_prediction_rescaled_lstm_1[0].round(2)} Bilhões")
        print(f"Mean Absolute Error (MAE): {mae_lstm_1}")
        print(f"Mean Squared Error (MSE): {mse_lstm_1}")

        print('\nParâmetros com o melhor MAE encontrados e utilizados para a segunda rodadada de treinamentos')
        print(f"Melhores parâmetros: {melhor_parametros_lstm} com MAE: {melhor_mae_lstm}")

        print('\nResultados e previsões do LSTM após a revisão dos parâmetros')
        print(f"Previsão para o próximo valor: {next_prediction_rescaled_2[0].round(2)} Bilhões")
        print(f"Mean Absolute Error (MAE): {mae_final_lstm}")
        print(f"Mean Squared Error (MSE): {mse_final_lstm}")

        print('\n ------------------------------ Resultados LIGHT GBM --------------------------------------------')

        print(f"Melhor número de iterações: {best_iteration}")
        print(f"Melhor score de validação: {best_score}")

        print(f"Mean Absolute Error (MAE) - LightGBM: {mae_lgb}")
        print(f"Mean Squared Error (MSE) - LightGBM: {mse_lgb}")
        print(f"Previsão para o próximo valor: {next_prediction_lgb[0].round(2)} Bilhões")

        print('\n ------------------------------ Resultados XGBoost --------------------------------------------')
        
        print(f"Previsão para o próximo valor: {predicted_value_rounded.round(2)} Bilhões")
        print(f"Mean Absolute Error (MAE) - XGBoost: {mae_xgb}")
        print(f"Mean Squared Error (MSE) - XGBoost: {mse_xgb}")

