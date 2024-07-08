from opentelemetry import trace, metrics

tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")

log_counter = meter.create_counter("dice.roll.type", unit="rolls", description="The type of roll by roll value")
roll_counter = meter.create_counter("dice.rolls", unit="rolls", description="The number of rolls by roll value")

def instance_update(instance, request_json):
  """
  This function updates every key received from the request in an instance of a table, if the key exists in that table.
  
  Example: The table User has three columns (id, name, email) and the request object has five fields (name, age, bloodType, email, address).
  The updated fields in the instance will be (name, email).

  The parameter instance should be a query from a table. 

  `instance = User.query.get(id)`
  """

  instance_keys: list[str] = list(instance.to_dict().keys())

  for key in instance_keys:
    if key in request_json and request_json[key] is not None:
      setattr(instance, key, request_json.get(key))
  
  if request_json.get("email") is not None:
    setattr(instance, 'email', request_json.get("email").lower())
  
  #if request_json.get("password") is not None:
  #  setattr(instance, 'password', bcrypt_context.hash(request_json.get("password")))