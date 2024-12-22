# Previsão do Fluxo Cambial Estrangeiro: uma análise de métodos de Machine Learning

O projeto consiste em buscar informações em diversas fontes de dados e tratá-las para realizar previsões da próxima semana de Fluxo Cambial Estrangeiro. As fontes de dados utilizadas foram:

1. Banco Central do Brasil (BACEN): séries diárias da Selic, reservas internacionais, da Libra (GBP), Dólar (USD), Euro (EUR) e séries mensais da balança de pagamentos, IBC-BR, IPCA, PIB do Brasil e Viagens;
2. ESALQ-USP: séries diárias do preço do açúcar, soja, boi gordo e milho;
3. Federal Reserve of St. Louis (FRED): séries mensais da taxa de juros do FED (EUA), da atividade econômica dos EUA, do preço do minério de ferro;
4. MACROTRENDS: séries anuais do PIB e Inflação da Europa, China e Estados Unidos. 
5. IPEADATA: série diária do preço do petróleo;
6. Investing: série diária do Ibovespa;
7. InfoMoney: série diária do Fluxo Cambial Estrangeiro.

Os scripts definidos como daily_schedule.py tem a mesma funcionalidade, a diferença que no 2.0 é necessário passar somente o horário de início do script.
Recomendação: Usar o 2.0 para quando o código estiver em produção e o daily_schedule.py para desenvolvimento.

Os modelos testados para essa série temporal foram ARIMAX, LSTM, LIGHT GBM e XGBoost.

Os outputs do Script são:

a) Outputs em imagens na pasta de outputs;
b) Arquivos tratados na pasta de downloads;
c) Dataframe dos arquivos tratados unidos e disponibilizado em excel no diretório modelo;
d) Dataframes criados específicos para cada modelo em excel e disponíveis no diretório modelo;
e) Print no final do código com o MAE, MSE e o valor para a próxima semana para cada um dos modelos.

# Modo de Uso

--> Baixar os arquivos desta pasta;
--> Criar os diretórios como desejar, há uma recomendação na imagem "diretorio_sugestao.png";
--> Colocar os arquivos no diretório do modelo;
--> Executar o script daily_schedule.
