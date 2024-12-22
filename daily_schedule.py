import schedule
import time
from download_databases import download_databases
from dataframe_modelo import dataframe_modelo
from selecao_atributos import selecao_atributos
from previsoes import previsoes
from functools import partial

diretorio_download = r"C:\Users\Pichau\Downloads"
diretorio_final = r"C:\Users\Pichau\Documents\MBA\download"
diretorio_modelo = r"C:\Users\Pichau\Documents\MBA"
diretorio_output = r'C:\Users\Pichau\Documents\MBA\outputs'

def schedule_tasks():

    # Agendar downloads
    schedule.every().day.at("11:18").do(partial(download_databases.download_bacen_sources, diretorio_download, diretorio_final))
    schedule.every().day.at("11:20").do(partial(download_databases.download_esalq, diretorio_download, diretorio_final))
    schedule.every().day.at("11:22").do(partial(download_databases.download_fred, diretorio_download, diretorio_final))
    schedule.every().day.at("11:24").do(partial(download_databases.download_macrotrends, diretorio_download, diretorio_final))
    schedule.every().day.at("11:26").do(partial(download_databases.download_ipeadata, diretorio_final))
    schedule.every().day.at("08:32").do(partial(download_databases.download_ibovespa, diretorio_final))
    schedule.every().day.at("11:30").do(partial(download_databases.download_investing, diretorio_final))

    # Lista de prefixos que deseja excluir
    prefixos_para_excluir = [
        'STP', 'CEPEA', 'USPHCI', 'FEDFUNDS', 'PIORECRUSDM', 
        'euro-area-gdp', 'united-states-inflation', 'china-inflation-rate', 
        'euro-area-inflation', 'china-gdp', 'united-states-gdp']
    
    schedule.every().day.at("11:32").do(partial(download_databases.limpar_arquivos, diretorio_download, prefixos_para_excluir))

    # Atualizar o dataframe que é usado no modelo

    schedule.every().day.at("11:34").do(partial(dataframe_modelo.dataframe_modelo, diretorio_final, diretorio_modelo))

    # Gera os dataframes com os atributos selecionados para cada tipo de modelo

    schedule.every().day.at("19:46").do(partial(selecao_atributos.selecao_atributos, diretorio_modelo))

    # Gera os dataframes com os atributos selecionados para cada tipo de modelo

    schedule.every().day.at("14:43").do(partial(previsoes.previsoes, diretorio_modelo, diretorio_output))

    print("Agendador iniciado. Tarefas rodarão nos horários definidos.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Iniciar o agendador
if __name__ == "__main__":
    schedule_tasks()