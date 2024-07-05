import logging
from random import randint
from fastapi import APIRouter
from opentelemetry import trace
from app import tracer, log_counter, roll_counter

router = APIRouter(prefix="/test")

def roll():
    return randint(1, 6)

def result_logging(result: int):
    if result < 3:
        logging.error(msg="level=error msg=\"A value below average appeared\"")
        log_counter.add(1, {"type.value": "below average"})
    if result == 3:
        logging.warning(msg="level=warn msg=\"A average value appeared\"")
        log_counter.add(1, {"type.value": "average"})
    if result > 3:
        logging.info(msg="level=info msg=\"A value above average appeared\"")
        log_counter.add(1, {"type.value": "above average"})

@router.get("/roll")
async def roll_dice(player: str = ""):
    if len(player) > 0:
        return f"{player} rolled the dice! Result: {roll()}"
    return f"Result: {roll()}"

@router.get("/manual_roll")
async def manual_rolldice(player: str = ""):
    with tracer.start_as_current_span("roll") as roll_span:
        result = roll()

        result_logging(result)

        roll_span.set_attribute("player", player)
        roll_span.set_attribute("roll_result", result)
        roll_counter.add(1, {"roll.value": result})

        if len(player) > 0:
            return f"{player} rolled the dice! Result: {result}"
        return f"Result: {result}"

@router.get("/deco_roll")
@tracer.start_as_current_span("deco_roll")
async def decorated_rolldice(player: str = ""):
    result = roll()

    result_logging(result)

    trace.get_current_span().set_attribute("player", player)
    trace.get_current_span().set_attribute("roll_result", result)
    roll_counter.add(1, {"roll.value": result})

    if len(player) > 0:
        return f"{player} rolled the dice! Result: {result}"
    return f"Result: {result}"