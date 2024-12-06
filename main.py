from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()

movement_motors = MotorPair('C', 'F')
neck_morter = Motor('E')

color_sensor_center = ColorSensor('B')
color_sensor_left = ColorSensor('A')
color_sensor_right = ColorSensor('D')

BLACK = 60 #60
TurnOut = 25
TurnInside = -6
Speed = 50 #30

# Default_speed
movement_motors.set_default_speed(Speed)

GO = True
DETECT = False

#neck potision initialize
#neck_morter.run_to_position(340)
#neck_morter.run_for_degrees(20,100)
#neck_morter.run_for_degrees(20,100)
neck_morter.run_to_position(0)
hub.light_matrix.show_image('TARGET')


hub.speaker.beep(60, 0.5)


while GO:
    if color_sensor_center.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_N')
        #if color_sensor_left.get_reflected_light() <= BLACK:
        #    movement_motors.start_tank(-TurnS/2,TurnS/2)
        #if color_sensor_right.get_reflected_light() <= BLACK:
        #    movement_motors.start_tank(TurnS/2,-TurnS/2)
        #movement_motors.start_tank(0,0)

        movement_motors.start(speed=Speed)
    elif color_sensor_left.get_reflected_light() <= BLACK and color_sensor_right.get_reflected_light() <= BLACK:
        movement_motors.start_tank(0,0)
        hub.light_matrix.show_image('CHESSBOARD')
        degree = 90
        neck_morter.run_to_position(355)
        DETECT1 = True
        DETECT2 = False
        back_cycle = 0
        neck_roll = 0
        roll_direction = 1
        while DETECT1:
            if color_sensor_center.get_reflected_light() <= BLACK:
                hub.light_matrix.show_image('SMILE')
                neck_morter.run_to_position(0)
                if roll_direction != 1:
                    hub.light_matrix.show_image('CLOCK3')

                    while color_sensor_center.get_reflected_light() > BLACK:
                        movement_motors.start_tank(TurnOut,TurnInside)

                    movement_motors.start(speed=Speed)
                    wait_for_seconds(0.3)
                    movement_motors.start(speed = 0)

                else:
                    hub.light_matrix.show_image('CLOCK9')

                    while color_sensor_center.get_reflected_light() > BLACK:
                        movement_motors.start_tank(TurnInside,TurnOut)

                    movement_motors.start(speed=Speed)
                    wait_for_seconds(0.3)
                    movement_motors.start(speed = 0)
                DETECT1 = False
            else:
                if neck_roll < 5:
                    neck_roll += 1
                    neck_morter.run_for_degrees(roll_direction*10,100)
                elif roll_direction == 1:
                    hub.light_matrix.write(roll_direction)
                    neck_roll = 0
                    roll_direction = -1
                    neck_morter.run_to_position(5)
                else:
                    hub.light_matrix.show_image('CHESSBOARD')
                    DETECT1 = False
                    DETECT2 = True
                    neck_morter.run_to_position(0)
                    
                    while color_sensor_center.get_reflected_light() > BLACK:
                        back_cycle += 1
                        movement_motors.start(speed=-20)
                    movement_motors.start(speed=0)
                    for i in range(back_cycle):
                        movement_motors.start(speed=10)
                        color_sensor_center.get_reflected_light()
                    movement_motors.start(speed=0)


        if DETECT2:
            right = 0
            left = 0

            neck_morter.run_to_position(270)
            for i in range(6):
                if color_sensor_center.get_reflected_light() <= BLACK:
                    right += 1
                neck_morter.run_for_degrees(6,100)
            hub.light_matrix.write(right)
            
            neck_morter.run_to_position(60)
            for i in range(6):
                if color_sensor_center.get_reflected_light() <= BLACK:
                    left += 1
                neck_morter.run_for_degrees(6,100)
            hub.light_matrix.write(left)

            neck_morter.run_to_position(0)

            if fabs(left-right) > 1:
                sign = int(copysign(1, left-right))

                if sign==1 : hub.light_matrix.show_image('CLOCK9')
                if sign==-1 : hub.light_matrix.show_image('CLOCK3')

                #探索前の位置に戻す
                for i in range(back_cycle):
                        movement_motors.start(speed=13)
                        color_sensor_center.get_reflected_light()
                movement_motors.start(speed=0)

                turn_cycle = 0

                returnTurn = sign*15
                while color_sensor_center.get_reflected_light() > BLACK:
                    #movement_motors.start_tank(-TurnS/2,TurnS/2)
                    movement_motors.start_tank(-returnTurn, returnTurn)
                    turn_cycle += 1
                
                wait_for_seconds(0.1)
                movement_motors.start_tank(0, 0)

                #回り過ぎた時の回避
                if turn_cycle > 380:
                    GO = False
                neck_morter.run_to_position(0)
    
                wait_for_seconds(0.5)
                DETECT2 = False

            else:
                DETECT2 = False
                GO = False
                neck_morter.run_to_position(0)
                break


            '''
            neck_morter.run_to_position(60)
            left1 = (color_sensor_center.get_reflected_light() <= BLACK)
            neck_morter.run_to_position(30)
            left2 = (color_sensor_center.get_reflected_light() <= BLACK)
            
            neck_morter.run_to_position(0)

            if right2 and left2:
                DETECT2 = False
                GO = False
                break
            elif right2:
                while color_sensor_center.get_reflected_light() > BLACK:
                    movement_motors.start_tank(TurnS,-TurnS)
                DETECT2 = False
            elif left2:
                while color_sensor_center.get_reflected_light() > BLACK:
                    movement_motors.start_tank(-TurnS,TurnS)
                DETECT2 = False
            else:
                DETECT2 = False
            '''            
                
        movement_motors.start(speed=0)
        

        
    elif color_sensor_left.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_NW')
        movement_motors.start_tank(TurnInside,TurnOut)
        #movement_motors.start_tank(-5,10)
    elif color_sensor_right.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_NE')
        movement_motors.start_tank(TurnOut,TurnInside)
        #movement_motors.start_tank(10,-5)
    else:
        hub.light_matrix.show_image('ARROW_S')
        movement_motors.start(speed=Speed)

movement_motors.start(speed=0)
hub.light_matrix.show_image('YES')

for i in range(60,80,4):
    hub.speaker.beep(i, 0.2)
for i in range(70,90,4):
    hub.speaker.beep(i, 0.2)
for i in range(80,100,4):
    hub.speaker.beep(i, 0.2)
hub.speaker.beep(100,0.7)

hub.light_matrix.show_image('ASLEEP')


