# TAPRA-2026

Projeto de Azure Functions desenvolvido para a atividade da disciplina, contendo funções com **Timer Trigger** e **HTTP Trigger**, escritas em Python (Programming Model v2).

## Integrantes da equipe

- Nome completo 1
- Nome completo 2
- Nome completo 3

> Substitua a lista acima pelos nomes reais dos integrantes da equipe.

## Estrutura do projeto

```
TAPRA-2026/
├── function_app.py       # Todas as functions do projeto
├── host.json             # Configuração da Function App
├── requirements.txt      # Dependências Python
├── local.settings.json   # Configurações locais (não versionar em produção)
└── README.md
```

## Funções implementadas

| Função | Tipo | Descrição |
|---|---|---|
| `timer_log_trigger` | Timer Trigger | Executa em intervalo (padrão: a cada 1 minuto) e apenas imprime um log no terminal. |
| `http_get_trigger` | HTTP Trigger (GET) | Recebe um parâmetro `nome` via query string na URL e imprime/retorna essa informação. |
| `http_echo_trigger` | HTTP Trigger (GET) | Função auxiliar: recebe um parâmetro `info` e retorna essa informação junto com um texto de identificação. |
| `timer_caller_trigger` | Timer Trigger | Executa em intervalo (padrão: a cada 2 minutos) e faz uma chamada HTTP para `http_echo_trigger`, logando a resposta recebida. |

## Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- [Azure Functions Core Tools v4](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) (para publicar no Azure)
- Conta no Azure (para deploy)

## Como executar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/<seu-usuario>/TAPRA-2026.git
   cd TAPRA-2026
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux/Mac
   .venv\Scripts\activate         # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a Function App localmente:
   ```bash
   func start
   ```

5. Teste a função HTTP em outro terminal ou no navegador:
   ```
   http://localhost:7071/api/hello?nome=SeuNome
   ```

6. Observe no terminal onde o `func start` está rodando:
   - Os logs da `timer_log_trigger` (a cada 1 minuto).
   - Os logs da `timer_caller_trigger` (a cada 2 minutos), que chama a `http_echo_trigger` e imprime a resposta recebida.

## Deploy no Azure

1. Login no Azure:
   ```bash
   az login
   ```

2. Crie os recursos necessários (Resource Group, Storage Account e Function App):
   ```bash
   az group create --name rg-tapra-2026 --location eastus

   az storage account create --name sttapra2026 --location eastus --resource-group rg-tapra-2026 --sku Standard_LRS

   az functionapp create --resource-group rg-tapra-2026 --consumption-plan-location eastus \
     --runtime python --runtime-version 3.10 --functions-version 4 \
     --name tapra-2026-func --storage-account sttapra2026 --os-type linux
   ```

3. Publique o código:
   ```bash
   func azure functionapp publish tapra-2026-func
   ```

4. Configure a app setting `ECHO_FUNCTION_URL` apontando para a URL pública da função `http_echo_trigger` publicada (necessário para a `timer_caller_trigger` funcionar em produção):
   ```bash
   az functionapp config appsettings set --name tapra-2026-func --resource-group rg-tapra-2026 \
     --settings ECHO_FUNCTION_URL="https://tapra-2026-func.azurewebsites.net/api/echo"
   ```

## Referências

- [Documentação oficial - HTTP trigger no Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger)
- [Documentação oficial - Timer trigger no Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer)
