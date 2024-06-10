import uvicorn
from random import randint
from fastapi import FastAPI
from opentelemetry import trace, metrics

tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller_meter")

roll_counter = meter.create_counter("dice_rolls", unit="rolls", description="The number of rolls by roll value")

app = FastAPI()

@app.get("/rolldice")
def roll_dice(player: str = None):
    if player:
        return f"{player} rolled the dice! Result: {randint(1, 6)}"
    return f"Result: {randint(1, 6)}"

@app.get("/manual_rolldice")
def manual_rolldice(player: str = None):
    with tracer.start_as_current_span("roll") as roll_span:
        result = randint(1,  6)

        roll_span.set_attribute("player", player)
        roll_span.set_attribute("roll_result", result)
        roll_counter.add(1, {"roll_value": result})

        if player:
            return f"{player} rolled the dice! Result: {result}"
        return f"Result: {result}"
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
