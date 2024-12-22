# Arquivo criado para ter as funções que serão chamadas no scheduler

class download_databases:
    @staticmethod
    def download_bacen_sources(diretorio_download, diretorio_final):

        import pyautogui
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        import os
        import time
        import pandas as pd

        # ---- Download do arquivo da Balança de Pagamentos

        # Configurações do ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": diretorio_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)


        code_sgs.send_keys("22707")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        # -------- TRATAMENTO DO ARQUIVO E DIRECIONAMENTO PARA UMA PASTA

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        balanca = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        balanca = balanca.drop(balanca.index[-1])
        balanca.rename(columns = {'22707 - Balança comercial - Balanço de Pagamentos - mensal - saldo - US$ (milhões)': 'vlr_balanca_pagamentos',
                                'Data': 'dt_dia'}, inplace= True)

        balanca['dt_dia'] = pd.to_datetime(balanca['dt_dia'], format = '%m/%Y')
        balanca['dt_dia'] = balanca['dt_dia'].dt.strftime('%Y-%m-%d')

        balanca['vlr_balanca_pagamentos'] = [x.replace('.', '') for x in balanca['vlr_balanca_pagamentos']]
        balanca['vlr_balanca_pagamentos'] = [x.replace(',', '.') for x in balanca['vlr_balanca_pagamentos']]
        balanca['vlr_balanca_pagamentos'] = balanca['vlr_balanca_pagamentos'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'balanca_pagamentos.csv')
        balanca.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo da Balança de Pagamentos atualizado com sucesso')

        # ---- Download do arquivo do IPCA

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)


        code_sgs.send_keys("433")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo IPCA e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        ipca = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        ipca = ipca.drop(ipca.index[-1])
        ipca.rename(columns = {'433 - Índice nacional de preços ao consumidor-amplo (IPCA) - Var. % mensal': 'perc_ipca',
                                'Data': 'dt_dia'}, inplace= True)

        ipca['dt_dia'] = pd.to_datetime(ipca['dt_dia'], format = '%m/%Y')
        ipca['dt_dia'] = ipca['dt_dia'].dt.strftime('%Y-%m-%d')

        ipca['perc_ipca'] = [x.replace(',', '.') for x in ipca['perc_ipca']]
        ipca['perc_ipca'] = ipca['perc_ipca'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'ipca.csv')
        ipca.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo da IPCA atualizado com sucesso')

        # ---- Download do arquivo do Euro

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)


        code_sgs.send_keys("21619")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo do EURO e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        euro = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        euro = euro.drop(euro.index[-1])
        euro.rename(columns = {'21619 - Taxa de câmbio - Livre - Euro (venda) - R$/u.m.c.': 'tx_euro',
                                'Data': 'dt_dia'}, inplace= True)

        euro['dt_dia'] = pd.to_datetime(euro['dt_dia'], format = '%d/%m/%Y')
        euro['dt_dia'] = euro['dt_dia'].dt.strftime('%Y-%m-%d')
        euro['tx_euro'] = [x.replace(',', '.') for x in euro['tx_euro']]
        euro['tx_euro'] = euro['tx_euro'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'euro.csv')
        euro.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo do EURO atualizado com sucesso')

        # ---- Download do arquivo do IBC BR

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("24363")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo do IBC BR e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        ibcbr = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        ibcbr = ibcbr.drop(ibcbr.index[-1])
        ibcbr.rename(columns = {'24363 - Índice de Atividade Econômica do Banco Central - IBC-Br - Índice': 'vlr_ibc_br',
                                'Data': 'dt_dia'}, inplace= True)

        ibcbr['dt_dia'] = pd.to_datetime(ibcbr['dt_dia'], format = '%m/%Y')
        ibcbr['dt_dia'] = ibcbr['dt_dia'].dt.strftime('%Y-%m-%d')

        ibcbr['vlr_ibc_br'] = [x.replace(',', '.') for x in ibcbr['vlr_ibc_br']]
        ibcbr['vlr_ibc_br'] = ibcbr['vlr_ibc_br'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'ibc_br.csv')
        ibcbr.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo do IBC-Br atualizado com sucesso')

        # ---- Download do arquivo do Dolar

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("1")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo do Dólar e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        dolar = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        dolar = dolar.drop(dolar.index[-1])
        dolar.rename(columns = {'1 - Taxa de câmbio - Livre - Dólar americano (venda) - diário - u.m.c./US$': 'tx_cambio_dolar',
                                'Data': 'dt_dia'}, inplace= True)

        dolar['dt_dia'] = pd.to_datetime(dolar['dt_dia'], format = '%d/%m/%Y')
        dolar['dt_dia'] = dolar['dt_dia'].dt.strftime('%Y-%m-%d')
        dolar['tx_cambio_dolar'] = [x.replace(',', '.') for x in dolar['tx_cambio_dolar']]
        dolar['tx_cambio_dolar'] = dolar['tx_cambio_dolar'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'dolar.csv')
        dolar.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo do Dólar atualizado com sucesso')

        # ---- Download do arquivo do PIB Brasil

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("4380")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo do PIB Brasil e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        pib_brasil = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        pib_brasil = pib_brasil.drop(pib_brasil.index[-1])
        pib_brasil.rename(columns = {'4380 - PIB mensal - Valores correntes (R$ milhões) - R$ (milhões)': 'vlr_pib',
                                'Data': 'dt_dia'}, inplace= True)

        pib_brasil['dt_dia'] = pd.to_datetime(pib_brasil['dt_dia'], format = '%m/%Y')
        pib_brasil['dt_dia'] = pib_brasil['dt_dia'].dt.strftime('%Y-%m-%d')

        pib_brasil['vlr_pib'] = [x.replace('.', '') for x in pib_brasil['vlr_pib']]
        pib_brasil['vlr_pib'] = [x.replace(',', '.') for x in pib_brasil['vlr_pib']]
        pib_brasil['vlr_pib'] = pib_brasil['vlr_pib'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'pib.csv')
        pib_brasil.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo do PIB atualizado com sucesso')

        # ---- Download do arquivo da Libra

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("21623")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo da Libra e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        libra = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        libra = libra.drop(libra.index[-1])
        libra.rename(columns = {'21623 - Taxa de câmbio - Livre - Libra Esterlina (venda) - R$/u.m.c.': 'tx_libra',
                                'Data': 'dt_dia'}, inplace= True)

        libra['dt_dia'] = pd.to_datetime(libra['dt_dia'], format = '%d/%m/%Y')
        libra['dt_dia'] = libra['dt_dia'].dt.strftime('%Y-%m-%d')
        libra['tx_libra'] = [x.replace(',', '.') for x in libra['tx_libra']]
        libra['tx_libra'] = libra['tx_libra'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'libra.csv')
        libra.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo do Libra atualizado com sucesso')

        # ---- Download do arquivo das Reservas Internacionais

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("13621")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo das Reservas Internacionais e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        reservas = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        reservas = reservas.drop(reservas.index[-1])
        reservas.rename(columns = {'13621 - Reservas internacionais - Total - diária - US$ (milhões)': 'vlr_reservas_internacionais',
                                'Data': 'dt_dia'}, inplace= True)

        reservas['dt_dia'] = pd.to_datetime(reservas['dt_dia'], format = '%d/%m/%Y')
        reservas['dt_dia'] = reservas['dt_dia'].dt.strftime('%Y-%m-%d')
        reservas['vlr_reservas_internacionais'] = [x.replace(',', '.') for x in reservas['vlr_reservas_internacionais']]
        reservas['vlr_reservas_internacionais'] = reservas['vlr_reservas_internacionais'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'reservas_internacionais.csv')
        reservas.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo das Reservas Internacionais atualizado com sucesso')

        # ---- Download do arquivo da SELIC

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("1178")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo da SELIC e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        selic = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        selic = selic.drop(selic.index[-1])
        selic.rename(columns = {'1178 - Taxa de juros - Selic anualizada base 252 - % a.a.': 'perc_selic_anualizada',
                                'Data': 'dt_dia'}, inplace= True)

        selic['dt_dia'] = pd.to_datetime(selic['dt_dia'], format = '%d/%m/%Y')
        selic['dt_dia'] = selic['dt_dia'].dt.strftime('%Y-%m-%d')
        selic['perc_selic_anualizada'] = [x.replace(',', '.') for x in selic['perc_selic_anualizada']]
        selic['perc_selic_anualizada'] = selic['perc_selic_anualizada'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'selic.csv')
        selic.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo da SELIC atualizado com sucesso')

        # ---- Download do arquivo das Viagens

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

        time.sleep(5)

        pyautogui.press('enter')

        time.sleep(10)

        # Preencher o campo de código e avançar
        code_sgs = driver.find_element(By.ID, "txCodigo")

        time.sleep(2)

        code_sgs.send_keys("22740")
        code_sgs.send_keys(Keys.ENTER)

        time.sleep(5)

        # Procura o botão para marcar a série
        botao_marcar_todos = driver.find_element(By.CSS_SELECTOR, 'div#botaoMarcar input[type="button"][onclick*="javascript:marcarDesmarcarTodos(true);"]')

        botao_marcar_todos.click()
        time.sleep(5)

        # Procura o botão pra procurar series
        botao_consultar_series = driver.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Consultar séries"]')

        botao_consultar_series.click()
        time.sleep(5)

        datainicio = driver.find_element(By.ID, "dataInicio")
        datainicio.clear()
        datainicio.send_keys("01")
        datainicio.send_keys("01")
        datainicio.send_keys("2011")
        time.sleep(5)

        # Procura o botão pelo seletor CSS com base no valor do botão
        botao_visualizar_valores = driver.find_element(By.CSS_SELECTOR, 'input[value="Visualizar valores"]')
        botao_visualizar_valores.click()
        time.sleep(5)

        # Procura o botão de download
        botao_baixar = driver.find_element(By.CSS_SELECTOR, '[title="Transferir arquivo para o computador do usuário"]')
        botao_baixar.click()
        time.sleep(10)

        driver.quit()

        #  ----- Tratamento do arquivo das Viagens e direcionamento para a pasta

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('STP-')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        viagens = pd.read_csv(caminho_arquivo, sep = ';', encoding = 'latin-1')
        viagens = viagens.drop(viagens.index[-1])
        viagens.rename(columns = {'22740 - Viagens - mensal - líquido - US$ (milhões)': 'vlr_viagens',
                                'Data': 'dt_dia'}, inplace= True)

        viagens['dt_dia'] = pd.to_datetime(viagens['dt_dia'], format = '%m/%Y')
        viagens['dt_dia'] = viagens['dt_dia'].dt.strftime('%Y-%m-%d')

        viagens['vlr_viagens'] = [x.replace('.', '') for x in viagens['vlr_viagens']]
        viagens['vlr_viagens'] = [x.replace(',', '.') for x in viagens['vlr_viagens']]
        viagens['vlr_viagens'] = viagens['vlr_viagens'].astype(float)

        caminho_final = os.path.join(diretorio_final, 'viagens.csv')
        viagens.to_csv(caminho_final, sep=';', index=False)

        print('Arquivo das Viagens atualizado com sucesso')

        return print('Download dos arquivos do BACEN finalizado com sucesso!')
    
    @staticmethod
    def download_esalq(diretorio_download, diretorio_final):

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        import os
        import time
        import pandas as pd
        import xlrd

        # Configurações do ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": diretorio_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        ############### DOWNLOAD AÇÚCAR #####################
        
        # Indicando o site que o driver vai abrir
        driver.get('https://www.cepea.esalq.usp.br/br/indicador/series/acucar.aspx?id=53')

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('CEPEA_')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        with open(caminho_arquivo, 'rb') as f:
            workbook = xlrd.open_workbook(file_contents=f.read(), ignore_workbook_corruption=True)
            sheet = workbook.sheet_by_index(0)
            
            # Pula as 3 primeiras linhas
            data = [sheet.row_values(row_idx) for row_idx in range(sheet.nrows)][3:]
            
            # Define a quarta linha como cabeçalho e as demais como dados
            df = pd.DataFrame(data[1:], columns=data[0])  # data[0] contém os cabeçalhos

        df = df[['Data', 'À vista R$']]
        df.rename(columns = {'À vista R$': 'vlr_acucar_brl',
                                'Data': 'dt_dia'}, inplace= True)

        df['dt_dia'] = pd.to_datetime(df['dt_dia'], format = '%d/%m/%Y')
        df['dt_dia'] = df['dt_dia'].dt.strftime('%Y-%m-%d')

        caminho_final = os.path.join(diretorio_final, 'acucar.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do Açúcar atualizada com sucesso')

        ############### DOWNLOAD SOJA #####################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www.cepea.esalq.usp.br/br/indicador/series/soja.aspx?id=92')

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('CEPEA_')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        with open(caminho_arquivo, 'rb') as f:
            workbook = xlrd.open_workbook(file_contents=f.read(), ignore_workbook_corruption=True)
            sheet = workbook.sheet_by_index(0)
            
            # Pula as 3 primeiras linhas
            data = [sheet.row_values(row_idx) for row_idx in range(sheet.nrows)][3:]
            
            # Define a quarta linha como cabeçalho e as demais como dados
            df = pd.DataFrame(data[1:], columns=data[0])  # data[0] contém os cabeçalhos

        df = df[['Data', 'À vista R$']]
        df.rename(columns = {'À vista R$': 'vlr_soja_brl',
                                'Data': 'dt_dia'}, inplace= True)

        df['dt_dia'] = pd.to_datetime(df['dt_dia'], format = '%d/%m/%Y')
        df['dt_dia'] = df['dt_dia'].dt.strftime('%Y-%m-%d')

        caminho_final = os.path.join(diretorio_final, 'soja.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do Soja atualizada com sucesso')

        ############### DOWNLOAD BOI GORDO #####################
        
        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www.cepea.esalq.usp.br/br/indicador/series/boi-gordo.aspx?id=2')

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('CEPEA_')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        with open(caminho_arquivo, 'rb') as f:
            workbook = xlrd.open_workbook(file_contents=f.read(), ignore_workbook_corruption=True)
            sheet = workbook.sheet_by_index(0)
            
            # Pula as 3 primeiras linhas
            data = [sheet.row_values(row_idx) for row_idx in range(sheet.nrows)][3:]
            
            # Define a quarta linha como cabeçalho e as demais como dados
            df = pd.DataFrame(data[1:], columns=data[0])  # data[0] contém os cabeçalhos

        df = df[['Data', 'À vista R$']]
        df.rename(columns = {'À vista R$': 'vlr_boi_gordo_brl',
                                'Data': 'dt_dia'}, inplace= True)

        df['dt_dia'] = pd.to_datetime(df['dt_dia'], format = '%d/%m/%Y')
        df['dt_dia'] = df['dt_dia'].dt.strftime('%Y-%m-%d')

        caminho_final = os.path.join(diretorio_final, 'boi_gordo.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do Boi Gordo atualizado com sucesso')

        ############### DOWNLOAD MILHO #####################
        
        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Indicando o site que o driver vai abrir
        driver.get('https://www.cepea.esalq.usp.br/br/indicador/series/milho.aspx?id=77')

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('CEPEA_')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        caminho_arquivo = os.path.join(diretorio_download, arquivo_mais_recente)

        with open(caminho_arquivo, 'rb') as f:
            workbook = xlrd.open_workbook(file_contents=f.read(), ignore_workbook_corruption=True)
            sheet = workbook.sheet_by_index(0)
            
            # Pula as 3 primeiras linhas
            data = [sheet.row_values(row_idx) for row_idx in range(sheet.nrows)][3:]
            
            # Define a quarta linha como cabeçalho e as demais como dados
            df = pd.DataFrame(data[1:], columns=data[0])  # data[0] contém os cabeçalhos

        df = df[['Data', 'À vista R$']]
        df.rename(columns = {'À vista R$': 'vlr_milho_brl',
                                'Data': 'dt_dia'}, inplace= True)

        df['dt_dia'] = pd.to_datetime(df['dt_dia'], format = '%d/%m/%Y')
        df['dt_dia'] = df['dt_dia'].dt.strftime('%Y-%m-%d')

        caminho_final = os.path.join(diretorio_final, 'milho.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do Milho atualizado com sucesso')

        return print('Arquivos da ESALQ baixados com sucesso!')
    
    @staticmethod
    def download_fred(diretorio_download, diretorio_final):

        import pyautogui
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        import os
        import time
        import pandas as pd
        import xlrd

        # Configurações do ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": diretorio_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        ########### DOWNLOAD MINÉRIO DE FERRO ######################

        # Indicando o site que o driver vai abrir
        driver.get('https://fred.stlouisfed.org/series/PIORECRUSDM')
        driver.maximize_window()

        time.sleep(5)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "download-button")

        download_button.click()

        time.sleep(5)

        # Localiza o botão pelo ID
        download_csv = driver.find_element(By.ID, "download-data-csv")

        download_csv.click()

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('PIORECRUSDM')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',')

        df.rename(columns = {'PIORECRUSDM': 'vlr_minerio_ferro', 'observation_date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'minerio_ferro.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do Minério de Ferro atualizada com sucesso')

        ########### DOWNLOAD ATIVIDADE ECONôMICA EUA ######################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://fred.stlouisfed.org/series/USPHCI')
        driver.maximize_window()

        time.sleep(5)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "download-button")

        download_button.click()

        time.sleep(5)

        # Localiza o botão pelo ID
        download_csv = driver.find_element(By.ID, "download-data-csv")

        download_csv.click()

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('USPHCI')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',')

        df.rename(columns = {'USPHCI': 'vlr_usphci', 'observation_date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'usphci.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do USPHCI atualizada com sucesso')

        ########### DOWNLOAD JUROS FED ######################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://fred.stlouisfed.org/series/FEDFUNDS')
        driver.maximize_window()

        time.sleep(5)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "download-button")

        download_button.click()

        time.sleep(5)

        # Localiza o botão pelo ID
        download_csv = driver.find_element(By.ID, "download-data-csv")

        download_csv.click()

        time.sleep(15)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('FEDFUNDS')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',')

        df.rename(columns = {'FEDFUNDS': 'tx_juros_fed', 'observation_date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'fedfunds.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do FED Funds atualizada com sucesso')

        return print('Arquivos do FRED baixados com sucesso!')
    
    @staticmethod
    def download_macrotrends(diretorio_download, diretorio_final):

        import pyautogui
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        import os
        import time
        import pandas as pd
        import xlrd

        # Configurações do ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": diretorio_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        ############## DONWLOAD PIB EUROPA ############################

        # Indicando o site que o driver vai abrir
        driver.get('https://www.macrotrends.net/global-metrics/countries/EMU/euro-area/gdp-gross-domestic-product')
        driver.maximize_window()

        time.sleep(30)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "dataDownload")

        # Rolar até o elemento
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", download_button)

        time.sleep(2)

        download_button.click()

        time.sleep(5)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('euro-area-gdp')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',', skiprows = 8)

        df = df[['Date', ' GDP (Billions of US $)', ' Per Capita (US $)']]

        df.rename(columns = {' GDP (Billions of US $)': 'vlr_pib_europa',
                    ' Per Capita (US $)': 'vlr_pib_per_capita_europa',
                    'Date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'pib_europa.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('PIB EUROPA atualizado com sucesso')

        ############## DONWLOAD INFLAÇÃO EUA ############################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www.macrotrends.net/global-metrics/countries/usa/united-states/inflation-rate-cpi#google_vignette')
        driver.maximize_window()

        time.sleep(30)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "dataDownload")

        # Rolar até o elemento
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", download_button)

        time.sleep(2)

        download_button.click()

        time.sleep(5)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('united-states-inflation-rate')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',', skiprows = 8)

        df = df[['Date', ' GDP (Billions of US $)']]

        df.rename(columns = {' GDP (Billions of US $)': 'vlr_inflacao_eua',
                    'Date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'inflacao_eua.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Inflação EUA atualizado com sucesso')

        ############## DONWLOAD INFLAÇÃO CHINA ############################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www.macrotrends.net/global-metrics/countries/chn/china/inflation-rate-cpi')
        driver.maximize_window()

        time.sleep(30)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "dataDownload")

        # Rolar até o elemento
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", download_button)

        time.sleep(2)

        download_button.click()

        time.sleep(5)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('china-inflation')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',', skiprows = 8)

        df = df[['Date', ' GDP (Billions of US $)']]

        df.rename(columns = {' GDP (Billions of US $)': 'vlr_inflacao_china',
                    'Date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'inflacao_china.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Inflação China atualizado com sucesso')

        ############## DONWLOAD INFLAÇÃO EUROPA ############################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www.macrotrends.net/global-metrics/countries/EMU/euro-area/inflation-rate-cpi')
        driver.maximize_window()

        time.sleep(30)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "dataDownload")

        # Rolar até o elemento
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", download_button)

        time.sleep(2)

        download_button.click()

        time.sleep(5)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('euro-area-inflation-rate')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',', skiprows = 8)

        df = df[['Date', ' GDP (Billions of US $)']]

        df.rename(columns = {' GDP (Billions of US $)': 'vlr_inflacao_europa',
                    'Date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'inflacao_europa.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Inflação Europa atualizado com sucesso')

        ############## DONWLOAD PIB CHINA ############################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Indicando o site que o driver vai abrir
        driver.get('https://www.macrotrends.net/global-metrics/countries/chn/china/gdp-gross-domestic-product')
        driver.maximize_window()

        time.sleep(30)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "dataDownload")

        # Rolar até o elemento
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", download_button)

        time.sleep(2)

        download_button.click()

        time.sleep(5)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('china-gdp-gross')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',', skiprows = 8)

        df = df[['Date', ' GDP (Billions of US $)', ' Per Capita (US $)']]

        df.rename(columns = {' GDP (Billions of US $)': 'vlr_pib_china',
                    ' Per Capita (US $)': 'vlr_pib_per_capita_china',
                    'Date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'pib_china.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('PIB China atualizado com sucesso')

        ############## DONWLOAD PIB EUA ############################

        # Iniciar o ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Indicando o site que o driver vai abrir
        driver.get('https://www.macrotrends.net/global-metrics/countries/usa/united-states/gdp-gross-domestic-product')
        driver.maximize_window()

        time.sleep(30)

        # Localiza o botão pelo ID
        download_button = driver.find_element(By.ID, "dataDownload")

        # Rolar até o elemento
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", download_button)

        time.sleep(2)

        download_button.click()

        time.sleep(5)

        driver.quit()

        # Lista todos os arquivo no diretório
        arquivos = os.listdir(diretorio_download)

        # Encontre o arquivo do Dolar
        arquivos_stp = [arquivo for arquivo in arquivos if arquivo.startswith('united-states-gdp')]

        if arquivos_stp:
            arquivos_stp.sort(key = lambda x: os.path.getmtime(os.path.join(diretorio_download, x)), reverse=True)

        # Seleciona o arquivo mais recente
        arquivo_mais_recente = arquivos_stp[0]

        # Lê o arquivo em pandas
        df_path = os.path.join(diretorio_download, arquivo_mais_recente)

        df = pd.read_csv(df_path, sep = ',', skiprows = 8)

        df = df[['Date', ' GDP (Billions of US $)', ' Per Capita (US $)']]

        df.rename(columns = {' GDP (Billions of US $)': 'vlr_pib_eua',
                    ' Per Capita (US $)': 'vlr_pib_per_capita_eua',
                    'Date': 'dt_dia'}, inplace= True)

        caminho_final = os.path.join(diretorio_final, 'pib_eua.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('PIB EUA atualizado com sucesso')

        return print('Arquivos do MACRO TRENDS baixados com sucesso!')
    
    @staticmethod
    def download_ipeadata(diretorio_final):
        
        import pandas as pd
        import os

        # URL da tabela
        url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"

        # Tenta ler todas as tabelas na página
        tables = pd.read_html(url)

        df = tables[2]

        # Remove as primeiras linhas
        df.columns = df.iloc[0]  # Usa a segunda linha como nomes das colunas
        df = df[1:]  # Exclui as linhas acima dos dados reais

        # Reseta o índice
        df.reset_index(drop=True, inplace=True)

        df.rename(columns = {'PreÃ§o - petrÃ³leo bruto - Brent (FOB)': 'vlr_petroleo_usd',
                        'Data': 'dt_dia'}, inplace= True)

        df['dt_dia'] = pd.to_datetime(df['dt_dia'], format = '%d/%m/%Y')
        df['dt_dia'] = df['dt_dia'].dt.strftime('%Y-%m-%d')

        df['vlr_petroleo_usd'] = df['vlr_petroleo_usd'].astype(float)/100

        caminho_final = os.path.join(diretorio_final, 'petroleo.csv')
        df.to_csv(caminho_final, sep=';', index=False)

        print('Curva do Petróleo atualizada com sucesso')

        return('Arquivos IPEA DATA baixados com sucesso!')
    
    @staticmethod
    def download_ibovespa(diretorio_final):

        import requests
        import pandas as pd
        import os

        try:

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

        except:

            # URL of the webpage
            url = "https://br.investing.com/indices/bovespa-historical-data"

            # Send the HTTP request
            response = requests.get(url)

            # Read the table from the HTML content
            tables = pd.read_html(response.content)

            df = tables[0]

            df['Unnamed: 0'] = pd.to_datetime(df['Unnamed: 0'], format = '%d.%m.%Y')

            df['Unnamed: 0'] = df['Unnamed: 0'].dt.strftime('%Y-%m-%d')

            df = df[['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']]

            df.rename(columns = {'Unnamed: 0': 'dt_dia',
                            'Unnamed: 1': 'vlr_ibov_fechamento',
                            'Unnamed: 2': 'vlr_ibov_abertura',
                            'Unnamed: 3': 'vlr_ibov_maxima',
                            'Unnamed: 4': 'vlr_ibov_minima'}, inplace = True)
            

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


    @staticmethod
    def download_investing(diretorio_final):
        import pandas as pd
        import requests
        import os

        # URL of the webpage
        url = "https://br.investing.com/economic-calendar/brazilian-foreign-exchange-flows-764"

        # Add headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Send the HTTP request
        response = requests.get(url, headers=headers)

        # Read the table from the HTML content
        tables = pd.read_html(response.content)

        df = tables[0]

        df['Lançamento'] = pd.to_datetime(df['Lançamento'], format = '%d.%m.%Y')
        df = df[['Lançamento', 'Atual']]
        df = df[1:]  # Exclui as linhas acima dos dados reais
        df['Atual'] = df['Atual'].str.replace('B', '')
        df['Atual'] = df['Atual'].str.replace(',', '.').astype(float)
        df.rename(columns = {'Atual': 'vlr_fluxo_cambial_bi',
                                'Lançamento': 'dt_dia'}, inplace= True)

        df['dt_dia'] = df['dt_dia'].dt.strftime('%Y-%m-%d')

        # Lendo o arquivo histórico salvo no diretorio de download
        caminho_histórico = os.path.join(diretorio_final, 'hist_fluxo_cambial.csv')

        df_hist = pd.read_csv(caminho_histórico, sep = ';')

        df_final = pd.concat([df, df_hist])
        df_final.drop_duplicates(inplace = True)

        caminho_final = os.path.join(diretorio_final, 'hist_fluxo_cambial.csv')
        df_final.to_csv(caminho_final, sep=';', index=False)

        caminho_final = os.path.join(diretorio_final, 'fluxo_cambial.csv')
        df_final.to_csv(caminho_final, sep=';', index=False)

        return print('Fluxo Cambial atualizado com sucesso')
    
    @staticmethod
    def limpar_arquivos(diretorio_download, prefixos):

        import os

        arquivos = os.listdir(diretorio_download)
        for arquivo in arquivos:
            if any(arquivo.startswith(prefixo) for prefixo in prefixos):
                caminho_arquivo = os.path.join(diretorio_download, arquivo)
                try:
                    os.remove(caminho_arquivo)
                    print(f'Arquivo removido: {caminho_arquivo}')
                except Exception as e:
                    print(f'Erro ao tentar remover o arquivo {caminho_arquivo}: {e}')

