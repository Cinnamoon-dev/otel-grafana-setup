import uvicorn, logging
from fastapi import FastAPI
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from app.controllers import instrumentationController
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

app = FastAPI()

app.include_router(instrumentationController.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=False, host="0.0.0.0")
