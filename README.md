# otel-grafana-setup
Repositório de configuração base para integração de uma API Python + OTEL Collector + Grafana Tempo

### Stack
- Auto-Instrumentation
- OTEL Collector
- Prometheus
- Loki
- Tempo
- Grafana

### Collector
A configuração base vai ser:

#### Receiver
Vai ser o Collector padrão então será: otlp

#### Exporter
É possível mandar direto para o banco do Prometheus configurando apenas a porta que o banco está localizado.