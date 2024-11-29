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

GO = True
DETECT = False

#neck potision initialize
neck_morter.run_to_position(340)
neck_morter.run_for_degrees(20,100)
neck_morter.run_for_degrees(20,100)
neck_morter.run_to_position(0)
hub.light_matrix.show_image('TARGET')
wait_for_seconds(1)


hub.speaker.beep(60, 0.5)


while GO:
    if color_sensor_center.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_N')
        movement_motors.start(speed=Speed)
    elif color_sensor_left.get_reflected_light() <= BLACK and color_sensor_right.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('CHESSBOARD')
        degree = 80
        neck_morter.run_to_position(280)
        DETECT = True
        neck_roll = -16
        #wait_for_seconds(1)
        while DETECT:
            if color_sensor_center.get_reflected_light() <= BLACK:
                hub.light_matrix.show_image('SMILE')
                neck_morter.run_to_position(0)
                if neck_roll < 0:
                    hub.light_matrix.show_image('CLOCK3')
                    while color_sensor_center.get_reflected_light() > BLACK:
                        movement_motors.start_tank(TurnS,-TurnS)
                    movement_motors.start(speed=Speed)
                    wait_for_seconds(0.1)
                    movement_motors.start(speed = 0)
                else:
                    hub.light_matrix.show_image('CLOCK9')
                    while color_sensor_center.get_reflected_light() > BLACK:
                        movement_motors.start_tank(-TurnS,TurnS)
                    movement_motors.start(speed=Speed)
                    wait_for_seconds(0.1)
                    movement_motors.start(speed = 0)
                DETECT = False
            else:
                if neck_roll < 17:
                    neck_roll += 1
                    neck_morter.run_for_degrees(5,100)
                    #wait_for_seconds(1)
                else:
                    DETECT = False
                    GO = False
                    break
    elif color_sensor_left.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_NW')
        movement_motors.start_tank(-TurnS,TurnS)
    elif color_sensor_right.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_NE')
        movement_motors.start_tank(TurnS,-TurnS)
    else:
        hub.light_matrix.show_image('ARROW_N')
        movement_motors.start(speed=Speed)
    
movement_motors.start(speed=0)
hub.light_matrix.show_image('YES')


hub.light_matrix.show_image('ASLEEP')