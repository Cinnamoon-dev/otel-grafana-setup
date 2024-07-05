from opentelemetry import trace, metrics

tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

log_counter = meter.create_counter("dice.roll.type", unit="rolls", description="The type of roll by roll value")
roll_counter = meter.create_counter("dice.rolls", unit="rolls", description="The number of rolls by roll value")