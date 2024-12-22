def download_ibovespa():

    import requests
    import pandas as pd
    import os

    diretorio_final = r"C:\Users\Pichau\Documents\MBA\download"

    # URL of the webpage
    url = "https://br.investing.com/indices/bovespa-historical-data"

    # Send the HTTP request
    response = requests.get(url)

    # Read the table from the HTML content
    tables = pd.read_html(response.content)

    df = tables[0]

    df['Data'] = pd.to_datetime(df['Data'], format = '%d.%m.%Y')

    df['Data'] = df['Data'].dt.strftime('%Y-%m-%d')

    df = df[['Data', 'Último', 'Abertura', 'Máxima', 'Mínima']]

    df.rename(columns = {'Data': 'dt_dia',
                    'Último': 'vlr_ibov_fechamento',
                    'Abertura': 'vlr_ibov_abertura',
                    'Máxima': 'vlr_ibov_maxima',
                    'Mínima': 'vlr_ibov_minima'}, inplace = True)
    

    # Lendo o arquivo histórico salvo no diretorio de download
    caminho_histórico = os.path.join(diretorio_final, 'hist_ibovespa.csv')

    df_hist = pd.read_csv(caminho_histórico, sep = ';')

    df_final = pd.concat([df, df_hist])

    df_final.drop_duplicates(subset = ['dt_dia'], inplace = True)

    caminho_final = os.path.join(diretorio_final, 'hist_ibovespa.csv')
    df_final.to_csv(caminho_final, sep=';', index=False)

    caminho_final = os.path.join(diretorio_final, 'ibovespa.csv')
    df_final.to_csv(caminho_final, sep=';', index=False)

    return print('Ibovespa atualizado com sucesso')

download_ibovespa()