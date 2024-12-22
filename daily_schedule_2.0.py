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

    # Horário inicial
    start_time = "14:13"

    # Lista de tarefas a serem agendadas
    tasks = [
        # Baixa os arquivos origem
        partial(download_databases.download_bacen_sources, diretorio_download, diretorio_final),
        partial(download_databases.download_esalq, diretorio_download, diretorio_final),
        partial(download_databases.download_fred, diretorio_download, diretorio_final),
        partial(download_databases.download_macrotrends, diretorio_download, diretorio_final),
        partial(download_databases.download_ipeadata, diretorio_final),
        partial(download_databases.download_ibovespa, diretorio_final),
        partial(download_databases.download_investing, diretorio_final),

        # Deleta os arquivos do Download
        partial(download_databases.limpar_arquivos, diretorio_download, [
            'STP', 'CEPEA', 'USPHCI', 'FEDFUNDS', 'PIORECRUSDM', 
            'euro-area-gdp', 'united-states-inflation', 'china-inflation-rate', 
            'euro-area-inflation', 'china-gdp', 'united-states-gdp'
        ]),

        # Gera o Dataframe inicial resultante dos arquivos acima
        partial(dataframe_modelo.dataframe_modelo, diretorio_final, diretorio_modelo),

        # Gera os arquivos após a seleção de atributos para cada modelo
        partial(selecao_atributos.selecao_atributos, diretorio_modelo),

        # Gera as previsoes
        partial(previsoes.previsoes, diretorio_modelo, diretorio_output)

    ]

    # Função para converter string de tempo para minutos
    def convert_to_minutes(time_str):
        h, m = map(int, time_str.split(':'))
        return h * 60 + m

    # Função para converter minutos para string de tempo
    def convert_to_time_str(minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    # Agendar tarefas com intervalos de 2 minutos
    current_time = convert_to_minutes(start_time)
    for task in tasks:
        schedule.every().day.at(convert_to_time_str(current_time)).do(task)
        current_time += 2

    print("Agendador iniciado. Tarefas rodarão nos horários definidos.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Iniciar o agendador
if __name__ == "__main__":
    schedule_tasks()
