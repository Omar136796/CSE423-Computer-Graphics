# Imports

from OpenGL.GL import *
from OpenGL.GLUT import * 
from OpenGL.GLU import * 
import random
import time

#Bright Colors

def colors():
    red=random.uniform(0.3, 1.0)
    green=random.uniform(0.3, 1.0)
    blue=random.uniform(0.3, 1.0)
    tup1=(red,green,blue)
    return tup1

# Global Variables

width=500
height=800
left_boundary=((-width)//2)+60
right_boundary=(width//2)-60

point_size=2
counter=0

displacement_x=20
displacement_y=20

x_d=random.randint((-width//2)+displacement_x, (width//2)-displacement_x)
y_d=(height//2)+displacement_y
size_d=10
color_d=colors()
speed_d=3

plate_initial_x=10    # plate initially jei point e thakbe
plate_base_height=-390
plate_width=80
plate_height=15
plate_angle=15
plate_speed=10

paused=False
game_over=False
exit=False
cheat_mode=False
last_time = time.time()

max_speed_d=15
cheat_speed=width*1.2

# Mid Point Line Drawing Algorithm

def findZone(x0,y0,x1,y1):
    dx=x1-x0
    dy=y1-y0
    if(abs(dx)>abs(dy)):
        if dx>0 and dy>0:
            zone=0
        elif dx>0 and dy<0:
            zone=7
        elif dx<0 and dy>0:
            zone=3
        else:
            zone=4
    else:
        if dx>0 and dy>0:
            zone=1
        elif dx>0 and dy<0:
            zone=6
        elif dx<0 and dy>0:
            zone=2
        else:
            zone=5
    return zone

def zoneN_to_zone0(a,b,zone):
    if zone==0:
        x,y=a,b
    elif zone==1:
        x,y=b,a
    elif zone==2:
        x,y=b,-a
    elif zone==3:
        x,y=-a,b
    elif zone==4:
        x,y=-a,-b
    elif zone==5:
        x,y=-b,-a
    elif zone==6:
        x,y=-b,a
    else:
        x,y=a,-b
    
    return x,y

def zone0_to_zoneN(a,b,zone):
    if zone==0:
        x,y=a,b    
    elif zone==1:
        x,y=b,a
    elif zone==2:
        x,y=-b,a
    elif zone==3:
        x,y=-a,b
    elif zone==4:
        x,y=-a,-b
    elif zone==5:
        x,y=-b,-a
    elif zone==6:
        x,y=b,-a
    else:
        x,y=a,-b
    
    return x,y    

def draw_points(color,x,y):
    global point_size
    glColor3f(*color)
    glPointSize(point_size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def MPL(x0,y0,x1,y1,color,zone):
    dx=x1-x0
    dy=y1-y0
    d=(2*dy)-dx
    incE=2*dy
    incNE=2*(dy-dx)

    x=x0
    y=y0

    px,py=zone0_to_zoneN(x,y,zone)
    draw_points(color,px,py)

    while (x<x1):
        if d<=0:
            d+=incE
            x+=1
        else:
            d+=incNE
            x+=1
            y+=1
        px,py=zone0_to_zoneN(x,y,zone)
        draw_points(color,px,py)

def MPL_init(x0,y0,x1,y1,color):
    zone=findZone(x0, y0, x1, y1)

    p0,q0=zoneN_to_zone0(x0,y0,zone)
    p1,q1=zoneN_to_zone0(x1,y1,zone)

    if p0>p1:
        p0,p1=p1,p0
        q0,q1=q1,q0

    MPL(p0,q0,p1,q1,color,zone)

# Collision Algorithm

def AABB_collision(d_x, d_y, plate_initial_x):

    global size_d, plate_width, plate_height, plate_angle, plate_base_height

    diamond_left=d_x-size_d
    diamond_right=d_x+size_d
    diamond_top=d_y+size_d
    diamond_bottom=d_y-size_d
    
    bottom_left_x=plate_initial_x-(plate_width // 2)
    bottom_right_x=plate_initial_x+(plate_width // 2)
    top_left_x=plate_initial_x-(plate_width // 2)-plate_angle
    top_right_x=plate_initial_x+(plate_width // 2)+plate_angle
    
    plate_left=min(bottom_left_x, top_left_x)
    plate_right=max(bottom_right_x, top_right_x)
    plate_bottom=plate_base_height  
    plate_top=plate_bottom + plate_height
    
    if (diamond_left<plate_right and diamond_right>plate_left and diamond_bottom<plate_top and diamond_top>plate_bottom):
        return True
    return False

# Drawing Shapes

def draw_left_arrow():
    MPL_init(-230, 350, -200, 370, (0, 1, 1))
    MPL_init(-230, 350, -200, 330, (0, 1, 1))
    MPL_init(-230, 350, -170, 350, (0, 1, 1))

def draw_pause():
    MPL_init(-10, 370, -10, 330, (1, 0.7, 0))
    MPL_init(10, 370, 10, 330, (1, 0.7, 0))

def draw_play():
    MPL_init(-20, 370, -20, 330, (1, 0.7, 0))
    MPL_init(-20, 330, 20, 350, (1, 0.7, 0))
    MPL_init(-20, 370, 20, 350, (1, 0.7, 0))

def draw_cross():
    MPL_init(190, 370, 230, 330, (1, 0, 0))
    MPL_init(190, 330, 230, 370, (1, 0, 0))

def draw_diamond():
    global x_d, y_d, size_d, color_d
    x=int(x_d)
    y=int(y_d)
    color1=color_d

    MPL_init(x,y+size_d,x-size_d,y,color1)
    MPL_init(x-size_d,y,x,y-size_d,color1)
    MPL_init(x,y-size_d,x+size_d,y,color1)
    MPL_init(x+size_d,y,x,y+size_d,color1)

def draw_plate(color1=(1,1,1)):
    global plate_initial_x, plate_width, plate_height, plate_angle, plate_base_height

    bottom_left_x=plate_initial_x-(plate_width//2)
    bottom_right_x=plate_initial_x+(plate_width//2)
    top_left_x=plate_initial_x-(plate_width//2) - plate_angle
    top_right_x=plate_initial_x+(plate_width//2) + plate_angle

    MPL_init(bottom_left_x, plate_base_height, top_left_x, (plate_base_height+plate_height), color1)
    MPL_init(bottom_right_x, plate_base_height, top_right_x, (plate_base_height+plate_height), color1)
    MPL_init(bottom_left_x, plate_base_height, bottom_right_x, plate_base_height, color1)
    MPL_init(top_left_x, (plate_base_height+plate_height), top_right_x, (plate_base_height+plate_height), color1)

# Animation Functions

def reset():
    global x_d, y_d, size_d, color_d, plate_initial_x, displacement_y, displacement_x, height, width, paused, game_over, exit, counter, speed_d, cheat_mode, max_speed_d

    x_d=random.randint((-width//2)+displacement_x, (width//2)-displacement_x)
    y_d=(height//2)+displacement_y

    size_d=10
    color_d=colors()
    speed_d=3

    plate_initial_x=10

    paused=False
    game_over=False
    exit=False
    cheat_mode=False
    counter=0

    glutPostRedisplay()

def animate():
    global x_d, y_d, game_over, counter, speed_d, last_time, color_d, plate_initial_x, cheat_mode, left_boundary, right_boundary, max_speed_d, cheat_speed, height, width

    if speed_d>max_speed_d:
        speed_d=max_speed_d

    current_time=time.time()
    delta_time=(current_time-last_time)
    last_time=current_time 

    if paused!=True and game_over!=True:   # running state
        y_d-=speed_d*delta_time*60

        if cheat_mode==True:

            plate_movement=cheat_speed*delta_time

            if plate_initial_x<x_d:
                plate_initial_x+=min(plate_movement, abs(x_d-plate_initial_x))
            elif plate_initial_x>x_d:
                plate_initial_x-=min(plate_movement, abs(plate_initial_x-x_d))

            plate_initial_x=max(left_boundary, min(right_boundary, plate_initial_x)) # clamping

        if AABB_collision(x_d,y_d,plate_initial_x)==True:
            counter+=1
            print(f"Score: {counter}")
            x_d=random.randint((-width//2)+displacement_x, (width//2)-displacement_x)
            y_d=(height//2)+displacement_y
            speed_d=min(speed_d+0.2, max_speed_d)
            color_d=colors()

        elif y_d<=-(height//2):
            game_over=True
            print(f"Game Over! Score: {counter}")

    glutPostRedisplay()

def special_key_listener(key, x, y):
    global plate_initial_x, cheat_mode, left_boundary, right_boundary, plate_speed, last_time, paused, game_over

    if paused==True or game_over==True or cheat_mode:
        return
    
    current_time=time.time()
    delta_time=current_time-last_time
    last_time=current_time 

    if key==GLUT_KEY_LEFT:
        plate_initial_x-=(plate_speed*delta_time*60)
        plate_initial_x=max(left_boundary, plate_initial_x)
        
    elif key==GLUT_KEY_RIGHT:
        plate_initial_x+=(plate_speed*delta_time*60)
        plate_initial_x=min(right_boundary, plate_initial_x)

    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global cheat_mode
    
    if key==b'c':
        cheat_mode=not(cheat_mode)
        if cheat_mode==True:
            print("Cheat Mode Activated!")
        else:
            print("Cheat Mode Deactivated!")
    
    glutPostRedisplay()

def convert_coordinate(x,y):
    a=x-(width/2)
    b=(height/2)-y 
    return a,b

def mouse_listener(button, state, x, y):
    global paused, game_over, exit, counter, width, height

    if state==GLUT_DOWN:
        x_gl, y_gl = convert_coordinate(x, y)
        
        if ((-width//2)+15)<=x_gl<=((-width//2)+85) and ((height//2)-80)<=y_gl<=((height//2)-20):
            reset()
            print("Starting over!")

        elif ((-width//2)+230)<=x_gl<=((-width//2)+275) and ((height//2)-75)<=y_gl<=((height//2)-17):
            paused=not(paused)
            if paused==True:
                print("Game Paused")
            else:
                print("Game Resumed")

        elif ((width//2)-70)<=x_gl<=((width//2)-10) and ((height//2)-90)<=y_gl<=((height//2)-20):
            print(f"Goodbye! Score: {counter}")
            reset()
            glutLeaveMainLoop()

################## Necessary Functions ####################

def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-width//2, width//2, -height//2, height//2, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def display():
    global paused, game_over,exit

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    draw_left_arrow()
    draw_cross()

    if paused==True:
        draw_play()
    else:
        draw_pause()

    if game_over==True:
       plate_color=(1.0, 0.0, 0.0)
    else:
       plate_color=(1.0, 1.0, 1.0)

    draw_plate(plate_color)

    if exit!=True and game_over!=True:
        draw_diamond()

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutMainLoop()

if __name__=="__main__":
    main()