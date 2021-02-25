from ev3sim.code_helpers import wait_for_tick, CommandSystem

wait_for_tick()

# Your code goes here!
x = 0
y = 0
CommandSystem.send_command(CommandSystem.TYPE_CUSTOM, f"Position: x: {x}, y: {y}")
CommandSystem.send_command(CommandSystem.TYPE_DRAW, {
    "obj": {
        "name": "Circle",
        "fill": "#ff0000",
        "position": [x, y],
        "radius": 2,
        "zPos": 20,
    },
    "key": "prediction_sphere",
})
