import uvicorn
from fastapi import FastAPI
from random import randint

app = FastAPI()

@app.get("/rolldice")
def roll_dice(player: str = None):
    if player:
        return f"{player} rolled the dice! Result: {randint(1, 6)}"
    return f"Result: {randint(1, 6)}"

@app.get("/manual_rolldice")
def manual_rolldice(player: str = None):
    # TODO
    # Criar meter e tracer para salvar as métricas
    # Salvar valor do dado num atributo do span
    # Criar um counter para salvar a quantidade de cada valor da rodada do dado numa métricas (quantos ums quantos dois quantos cincos)
    # Adicionar os atributos player name e dice value ao trace
    if player:
        return f"{player} rolled the dice! Result: {randint(1, 6)}"
    return f"Result: {randint(1, 6)}"
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)
