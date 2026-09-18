import azure.functions as func
import logging
import os
import json
import urllib.request
import urllib.parse

app = func.FunctionApp()

# URL da função "echo" (http_echo_trigger) que a timer_caller vai chamar.
# Em execução local, o valor padrão já funciona (mesmo host, porta 7071).
# Em produção (Azure), configure a app setting ECHO_FUNCTION_URL com a URL pública
# da função http_echo_trigger (ex: https://<sua-function-app>.azurewebsites.net/api/echo).
ECHO_FUNCTION_URL = os.environ.get(
    "ECHO_FUNCTION_URL",
    "http://localhost:7071/api/echo"
)


# ---------------------------------------------------------------------------
# 1) TIMER TRIGGER - apenas imprime um log no terminal
# ---------------------------------------------------------------------------
# Expressão CRON padrão do Azure Functions: "{segundo} {minuto} {hora} {dia} {mes} {dia-da-semana}"
# O exemplo abaixo executa a cada 1 minuto. Ajuste conforme necessário.
@app.function_name(name="timer_log_trigger")
@app.timer_trigger(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=True)
def timer_log_trigger(myTimer: func.TimerRequest) -> None:
    logging.info("Timer Trigger executado! Este e apenas um log de exemplo. [TAPRA-2026]")


# ---------------------------------------------------------------------------
# 2) HTTP TRIGGER - recebe um parametro via GET (query string) e "imprime na tela"
#    (loga no terminal e retorna a mesma informacao na resposta HTTP)
# ---------------------------------------------------------------------------
@app.function_name(name="http_get_trigger")
@app.route(route="hello", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def http_get_trigger(req: func.HttpRequest) -> func.HttpResponse:
    nome = req.params.get("nome")

    if not nome:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = None
        if req_body:
            nome = req_body.get("nome")

    if nome:
        mensagem = f"Parametro recebido via GET: {nome}"
        logging.info(mensagem)
        return func.HttpResponse(mensagem, status_code=200)
    else:
        return func.HttpResponse(
            "Passe um parametro 'nome' na query string. Exemplo: /api/hello?nome=Fulano",
            status_code=400
        )


# ---------------------------------------------------------------------------
# 3) HTTP TRIGGER (auxiliar/"echo") - recebe uma informacao e retorna essa
#    informacao + um texto de identificacao. Sera chamada pela timer_caller_trigger.
# ---------------------------------------------------------------------------
@app.function_name(name="http_echo_trigger")
@app.route(route="echo", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def http_echo_trigger(req: func.HttpRequest) -> func.HttpResponse:
    info = req.params.get("info", "sem-info")
    resposta = f"[http_echo_trigger] Informacao recebida: '{info}' - respondido pela FunctionApp TAPRA-2026"
    logging.info(resposta)
    return func.HttpResponse(resposta, status_code=200)


# ---------------------------------------------------------------------------
# 4) TIMER TRIGGER - faz uma chamada HTTP para a http_echo_trigger,
#    que retorna a informacao enviada + um texto de identificacao.
# ---------------------------------------------------------------------------
@app.function_name(name="timer_caller_trigger")
@app.timer_trigger(schedule="0 */2 * * * *", arg_name="myTimer", run_on_startup=True)
def timer_caller_trigger(myTimer: func.TimerRequest) -> None:
    informacao = "Ola vindo da timer_caller_trigger"
    query = urllib.parse.urlencode({"info": informacao})
    url = f"{ECHO_FUNCTION_URL}?{query}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            corpo = response.read().decode("utf-8")
            logging.info(f"timer_caller_trigger chamou http_echo_trigger com sucesso. Resposta: {corpo}")
    except Exception as e:
        logging.error(f"timer_caller_trigger falhou ao chamar {url}: {e}")
