name = data.get('name', 'world')
logger.warning("Hello {}".format(name))
hass.bus.fire(name, { "wow": "from a Python script!" })
