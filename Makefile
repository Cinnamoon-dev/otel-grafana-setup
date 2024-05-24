dry_run:
	python3 main.py
	
run:
	opentelemetry-instrument --traces_exporter console --metrics_exporter console --logs_exporter console --service_name otel_test python3 main.py

run_collector:
	opentelemetry-instrument --traces_exporter otlp --metrics_exporter otlp --logs_exporter otlp --service_name otel_test python3 main.py
	
collector:
	docker run -p 4317:4317 -p 4318:4318 -p 55679:55679 -v ./config/opentelemetry/otel-collector-config.yaml:/etc/otelcol-contrib/config.yaml otel/opentelemetry-collector-contrib
