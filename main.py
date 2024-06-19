import uvicorn, logging
from random import randint
from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# ----------------------------------------------------------------------------------------
# Configuração de export de logs para o OTEL Collector
# Na prática é só anexar o OTLP Handler para o root logger, o fluxo do final para o comeÇo é:
# root logger anexá-lo ao root logger <- Criar um Handler a partir do LoggerProvider <- Adicionar um Exporter e um Processor ao LoggerProvider <- LoggerProvider

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "otel_loki_test_service_name",
            "service.instance.id": "instance-1"
        }
    )
)

# Setando o logger_provider que foi criado como o LoggerProvider global
set_logger_provider(logger_provider)

# Criando uma instancia do OTLPLogExporter sem autenticação
exporter = OTLPLogExporter(insecure=True)

# Adicionando um BatchLogRecordProcessor ao LoggerProvider
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# Criando um LoggingHandler com esse logger_provider e o log level setado para NOTSET
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

# Anexando o Handler do OTLP ao root logger
logging.getLogger().addHandler(handler)
# ----------------------------------------------------------------------------------------


tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

log_counter = meter.create_counter("dice.roll.type", unit="rolls", description="The type of roll by roll value")
roll_counter = meter.create_counter("dice.rolls", unit="rolls", description="The number of rolls by roll value")

app = FastAPI()

def roll():
    return randint(1, 6)

@app.get("/roll")
async def roll_dice(player: str = ""):
    if len(player) > 0:
        return f"{player} rolled the dice! Result: {roll()}"
    return f"Result: {roll()}"

@app.get("/manual_roll")
async def manual_rolldice(player: str = ""):
    with tracer.start_as_current_span("roll") as roll_span:
        result = roll()

        if result < 3:
            logging.error(msg="level=error msg=\"A value below average appeared\"")
            log_counter.add(1, {"type.value": "below average"})
        if result == 3:
            logging.warning(msg="level=warn msg=\"A average value appeared\"")
            log_counter.add(1, {"type.value": "average"})
        if result > 3:
            logging.info(msg="level=info msg=\"A value above average appeared\"")
            log_counter.add(1, {"type.value": "above average"})

        roll_span.set_attribute("player", player)
        roll_span.set_attribute("roll_result", result)
        roll_counter.add(1, {"roll.value": result})

        if len(player) > 0:
            return f"{player} rolled the dice! Result: {result}"
        return f"Result: {result}"

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=False, host="0.0.0.0")
