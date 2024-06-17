import uvicorn, logging
from random import randint
from fastapi import FastAPI
from opentelemetry import trace, metrics

# TODO
# Fazer uso da biblioteca logging para exportar os logs para o Loki
logger = logging.getLogger()

tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

roll_counter = meter.create_counter("dice.rolls", unit="rolls", description="The number of rolls by roll value")

app = FastAPI()

@app.get("/rolldice")
async def roll_dice(player: str = ""):
    if len(player) > 0:
        return f"{player} rolled the dice! Result: {randint(1, 6)}"
    return f"Result: {randint(1, 6)}"

@app.get("/manual_rolldice")
async def manual_rolldice(player: str = ""):
    with tracer.start_as_current_span("roll") as roll_span:
        result = randint(1,  6)

        roll_span.set_attribute("player", player)
        roll_span.set_attribute("roll_result", result)
        roll_counter.add(1, {"roll.value": result})

        if len(player) > 0:
            return f"{player} rolled the dice! Result: {result}"
        return f"Result: {result}"
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=False, host="0.0.0.0")
