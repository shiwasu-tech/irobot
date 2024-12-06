from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

#init hub, motors, sensors
hub = PrimeHub()
movement_motors = MotorPair('C', 'F')
neck_morter = Motor('E')
color_sensor_center = ColorSensor('B')
color_sensor_left = ColorSensor('A')
color_sensor_right = ColorSensor('D')

#set parameters
BLACK = 60 #60
TurnOut = 25
TurnInside = -6
Speed = 50 #30

#set default speed
movement_motors.set_default_speed(Speed)

#GO，DETECT flag
GO = True
DETECT = False

#neck potision initialize
neck_morter.run_to_position(0)
hub.light_matrix.show_image('TARGET')

#start sound
hub.speaker.beep(60, 0.5)

#main loop
while GO:

    #if center is black, go forward
    if color_sensor_center.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_N')
        movement_motors.start(speed=Speed)

    #if left and right are black, detect T-junction, L-junction, crossroad
    elif color_sensor_left.get_reflected_light() <= BLACK and color_sensor_right.get_reflected_light() <= BLACK:
        movement_motors.start_tank(0,0)
        hub.light_matrix.show_image('CHESSBOARD')
        neck_morter.run_to_position(355)
        DETECT1 = True
        DETECT2 = False
        back_cycle = 0
        neck_roll = 0
        roll_direction = 1

        #loop for first detection
        #if exited from this loope, it's crossroad
        while DETECT1:
            
            #if neck(moving centor censor) is black, it's L-junction and turn correctly
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

            #if neck is white, move neck
            else:

                #turn neck (355 to 305) and (5 to 55)
                if neck_roll < 5:
                    neck_roll += 1
                    neck_morter.run_for_degrees(roll_direction*10,100)
                
                #change turn direction
                elif roll_direction == 1:
                    hub.light_matrix.write(roll_direction)
                    neck_roll = 0
                    roll_direction = -1
                    neck_morter.run_to_position(5)

                #if neck have turned and coouldn't detect black, start second detection
                else:
                    hub.light_matrix.show_image('CHESSBOARD')
                    DETECT1 = False
                    DETECT2 = True
                    neck_morter.run_to_position(0)
                    
                    #move back to the position before detection
                    #this make the robot to detect correctly
                    while color_sensor_center.get_reflected_light() > BLACK:
                        back_cycle += 1
                        movement_motors.start(speed=-20)
                    movement_motors.start(speed=0)
                    for i in range(back_cycle):
                        movement_motors.start(speed=10)
                        color_sensor_center.get_reflected_light()
                    movement_motors.start(speed=0)

        #loop for second detection
        #if exited from this loope, it's L-junction
        #if not, it's T-junction and end main loop
        if DETECT2:

            #count black on right and left
            right = 0
            left = 0

            #detect right side
            neck_morter.run_to_position(270)
            for i in range(6):
                if color_sensor_center.get_reflected_light() <= BLACK:
                    right += 1
                neck_morter.run_for_degrees(6,100)
            hub.light_matrix.write(right)
            
            #detect left side
            neck_morter.run_to_position(60)
            for i in range(6):
                if color_sensor_center.get_reflected_light() <= BLACK:
                    left += 1
                neck_morter.run_for_degrees(6,100)
            hub.light_matrix.write(left)

            neck_morter.run_to_position(0)

            #compare right and left count
            if fabs(left-right) > 1:
                sign = int(copysign(1, left-right))

                if sign==1 : hub.light_matrix.show_image('CLOCK9')
                if sign==-1 : hub.light_matrix.show_image('CLOCK3')

                #return to the position before detection
                #this make the robot to turn correctly
                for i in range(back_cycle):
                        movement_motors.start(speed=13)
                        color_sensor_center.get_reflected_light()
                movement_motors.start(speed=0)
                turn_cycle = 0
                returnTurn = sign*15

                #turn until center sensor detect black
                while color_sensor_center.get_reflected_light() > BLACK:
                    movement_motors.start_tank(-returnTurn, returnTurn)
                    turn_cycle += 1
                wait_for_seconds(0.1)
                movement_motors.start_tank(0, 0)

                #if turned too much, it's T-junction and end main loop
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
                
        movement_motors.start(speed=0)
        
    #if left side is black, turn left    
    elif color_sensor_left.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_NW')
        movement_motors.start_tank(TurnInside,TurnOut)

    #if right side is black, turn right    
    elif color_sensor_right.get_reflected_light() <= BLACK:
        hub.light_matrix.show_image('ARROW_NE')
        movement_motors.start_tank(TurnOut,TurnInside)
    
    #if all white, just go forward
    else:
        hub.light_matrix.show_image('ARROW_S')
        movement_motors.start(speed=Speed)

#stop motors and show image
movement_motors.start(speed=0)
hub.light_matrix.show_image('YES')

#end sound
for i in range(60,80,4):
    hub.speaker.beep(i, 0.2)
for i in range(70,90,4):
    hub.speaker.beep(i, 0.2)
for i in range(80,100,4):
    hub.speaker.beep(i, 0.2)
hub.speaker.beep(100,0.7)

hub.light_matrix.show_image('ASLEEP')
#all done

