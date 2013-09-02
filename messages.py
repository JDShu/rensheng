"""
Methods to transforms data into strings that are sent from the server to the client.
"""

from enums import MessageIds

def tick_message(tick, command_buffer):
    tick_data = [str(MessageIds.TICK), str(tick)] + [c.serialize() for c in command_buffer]
    return ":".join(tick_data)

def game_data(serialized_data):
    return "%d:%s" %(MessageIds.LOAD, serialized_data)
