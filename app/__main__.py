import asyncio

from . import bot_main


try:
  loop = asyncio.get_event_loop()
except RuntimeError as error:
  print(error)
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

loop.run_until_complete(bot_main(loop))