# Import
from OpenGL.GL import *
from OpenGL.GLUT import * 
from OpenGL.GLU import * 
import random
import time

# Global Variables
WINDOW_WIDTH=500
WINDOW_HEIGHT=500
ball_speed=0.5            
points_list=[]         
ball_size=6
blinking_state=False     
blink_start_time=0       
original_colors={}        
pause=False

# Animation

def animate():
    global points_list, pause
    
    if pause==True:
        glutPostRedisplay()
        return
    
    for point in points_list:

        point['x']+=(point['dir_x']*ball_speed)
        point['y']+=(point['dir_y']*ball_speed)
        
        if point['x']<=0:
            point['x']=0
            point['dir_x']=1
        
        elif point['x']>=WINDOW_WIDTH:
            point['x']=WINDOW_WIDTH
            point['dir_x']=-1
        
        if point['y']<=0:
            point['y']=0
            point['dir_y']=1 
        
        elif point['y']>=WINDOW_HEIGHT:
            point['y']=WINDOW_HEIGHT
            point['dir_y']=-1 
    
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global pause
    if key==b' ':
        pause=not(pause)
    glutPostRedisplay()

def special_key_listener(key,x,y):
    global ball_speed, pause

    if pause==True:
        return
    
    if key==GLUT_KEY_UP:
            ball_speed*=2
    elif key==GLUT_KEY_DOWN:
            ball_speed/=2

    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    global points_list, ball_speed, blinking_state, blink_start_time, original_colors, pause

    if pause==True:
        return
    
    if button==GLUT_RIGHT_BUTTON and state==GLUT_DOWN:
        point_x, point_y=convert_coordinate(x, y)
        color=(random.random(), random.random(), random.random())
        direction_x=random.choice([-1, 1])
        direction_y=random.choice([-1, 1]) 
        

        new_point={'x': point_x, 'y': point_y, 'color': color, 'dir_x': direction_x, 'dir_y': direction_y}
        
        points_list.append(new_point)
        
        if blinking_state==True:
            original_colors[len(points_list)-1]=color
    
    elif button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:

        blinking_state=not(blinking_state)
        
        if blinking_state==True:           
            blink_start_time=time.time()
            original_colors={} 
            for i, point in enumerate(points_list):
                original_colors[i]=point['color']

        else:
            for i, point in enumerate(points_list):
                if i in original_colors:
                    point['color']=original_colors[i]
            original_colors={}   


# Helper Functions

def convert_coordinate(x, y):
    a=x
    b=WINDOW_HEIGHT-y
    return a, b

def blink():
    global blinking_state, blink_start_time, points_list, original_colors
    
    if blinking_state==True:
        current_time=time.time()
        elapsed_time=current_time-blink_start_time
        blink_state=int(elapsed_time*2)%2           
        
        for i, point in enumerate(points_list):

            if blink_state==0:
                point['color']=original_colors.get(i, point['color'])

            else:
                point['color']=(0.0, 0.0, 0.0)

# Drawing

def draw_point(x, y, color=(1.0, 1.0, 1.0)):
    global ball_size
    glColor3f(*color)
    glPointSize(ball_size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Essential Functions

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def display():
    global blinking_state

    if blinking_state==True:
        blink()
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    for point in points_list:
        draw_point(point['x'], point['y'], point['color'])

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"The Amazing Box")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)

    glutMainLoop()

if __name__=="__main__":
    main()