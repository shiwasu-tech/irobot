from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()

movement_motors = MotorPair('C', 'F')
neck_morter = Motor('E')

color_sensor_center = ColorSensor('B')
color_sensor_left = ColorSensor('A')
color_sensor_right = ColorSensor('D')

BLACK = 60
TurnS = 10 #10
Speed = 30 #30

# Default_speed
movement_motors.set_default_speed(Speed)


hub.speaker.beep(60, 0.5)
GO = True

while GO:
    if color_sensor_center.get_reflected_light() <= BLACK:
        movement_motors.start(speed=Speed)
    elif color_sensor_left.get_reflected_light() <= BLACK and color_sensor_right.get_reflected_light() <= BLACK:
        neck_morter.run_for_degrees(15,60)
        if color_sensor_center.get_reflected_light() <= BLACK:
            neck_morter.run_to_degrees_counted(-15,60)
            movement_motors.start_tank(TurnS,-TurnS)
            continue
        neck_morter.run_for_degrees(30,60)
        if color_sensor_center.get_reflected_light() <= BLACK:
            movement_motors.start_tank(-TurnS,TurnS)
            neck_morter.run_for_degrees(15,60)
            continue
        break
    elif color_sensor_left.get_reflected_light() <= BLACK:
        movement_motors.start_tank(-TurnS,TurnS)
    elif color_sensor_right.get_reflected_light() <= BLACK:
        movement_motors.start_tank(TurnS,-TurnS)
    else: 
        movement_motors.start(speed=Speed)
    
movement_motors.start(speed=0)
hub.light_matrix.show_image('YES')
wait_for_seconds(3)