# Import
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random as rd

# Global Variables
total_drops=220
list_rain_drops=[]
rain_speed=10
wind_rain_direction=0.0
day_night=0.0

# Animation
def animate():
    global list_rain_drops,wind_rain_direction
    for drop in list_rain_drops:
        drop[0]+=wind_rain_direction*0.2
        drop[1]-=rain_speed

        drop[0]%=1000

        if drop[1]<0:      
            drop[0]=rd.uniform(0,1000)
            drop[1]=rd.uniform(600,700)

    glutPostRedisplay()

def keyboardListener(key, x, y):
    global day_night
    if key==b'n':
        day_night-=0.1
        day_night=min(1.0,day_night)
    if key==b'd':
        day_night+=0.1
        day_night=max(0.0,day_night)

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global wind_rain_direction
    
    if key==GLUT_KEY_RIGHT:
        if wind_rain_direction<60:
            wind_rain_direction+=10
        
    if key==GLUT_KEY_LEFT:
        if wind_rain_direction>-60:
            wind_rain_direction-=10
         
    glutPostRedisplay() 

# Helper Function
def populateRain():
    global list_rain_drops
    for r in range(total_drops):
        x=rd.uniform(0,1000)
        y=rd.uniform(0,600)
        list_rain_drops.append([x,y])

# Drawing
def draw_rain():
    rain_color=[(0.5,0.7,1.0),(0.5,0.5,0.5)]
    glLineWidth(1)
    glBegin(GL_LINES)
    for drop in list_rain_drops:
        a,b,c=rd.choice(rain_color)
        glColor3f(a,b,c)
        glVertex2f(drop[0],drop[1])
        glVertex2f(drop[0]+wind_rain_direction,drop[1]-35)
    glEnd()

def draw_background():
    glColor3f(day_night,day_night,day_night)
    glBegin(GL_TRIANGLES)
    glVertex2f(0,450)
    glVertex2f(1000,450)
    glVertex2f(1000,600)
    glEnd()

    glColor3f(day_night,day_night,day_night)
    glBegin(GL_TRIANGLES)
    glVertex2f(0,450)
    glVertex2f(1000,600)
    glVertex2f(0,600)
    glEnd()

def draw_fields():
    glColor3f(0.60,0.45,0.14)
    glBegin(GL_TRIANGLES)
    glVertex2f(0,0)
    glVertex2f(1000,0)
    glVertex2f(1000,450)
    glEnd()

    glColor3f(0.60, 0.45, 0.14)
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0)
    glVertex2f(1000, 450)
    glVertex2f(0, 450)
    glEnd()

def draw_trees():
    for i in range(0,1000,50):
        glColor3f(0.45, 0.85, 0.25)
        glBegin(GL_TRIANGLES)
        glVertex2d(i+50,350)
        glVertex2d(i+25, 440)
        glVertex2d(i,350)
        glEnd()

def house_body():
    glColor3f(0.97, 0.94, 0.90)
    glBegin(GL_TRIANGLES)
    glVertex2f(675, 250)
    glVertex2f(675, 370)
    glVertex2f(325, 250)
    glEnd() 

    glColor3f(0.97, 0.94, 0.90)
    glBegin(GL_TRIANGLES)
    glVertex2f(675, 370)
    glVertex2f(325, 370)
    glVertex2f(325, 250)
    glEnd()


def house_shed():
    glColor3f(0.47, 0.17, 0.81)
    glBegin(GL_TRIANGLES)
    glVertex2d(700,370)
    glVertex2d(500, 470)
    glVertex2d(300,370)
    glEnd()

def house_door():
    glColor3f(0.36, 0.65, 0.94)
    glBegin(GL_TRIANGLES)
    glVertex2f(530, 250)
    glVertex2f(530, 340)
    glVertex2f(470, 250)
    glEnd() 

    glColor3f(0.36, 0.65, 0.94)
    glBegin(GL_TRIANGLES)
    glVertex2f(530, 340)
    glVertex2f(470, 340)
    glVertex2f(470, 250)
    glEnd() 

    #Door Knob
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(7)            
    glBegin(GL_POINTS)     
    glVertex2f(518, 295)        
    glEnd()  

def house_window():
    #left window
    glColor3f(0.36, 0.65, 0.94)
    glBegin(GL_TRIANGLES)
    glVertex2f(400, 295)
    glVertex2f(400, 340)
    glVertex2f(450, 340)
    glEnd() 

    glColor3f(0.36, 0.65, 0.94)
    glBegin(GL_TRIANGLES)
    glVertex2f(400, 295)
    glVertex2f(450, 295)
    glVertex2f(450, 340)
    glEnd() 

    # railing
    glColor3f(0.0, 0.0, 0.0)  
    glLineWidth(3)        
    glBegin(GL_LINES)     
    glVertex2f(450, 317.5)
    glVertex2f(400, 317.5)
    glVertex2f(425, 295)
    glVertex2f(425, 340)
    glEnd()

    #right window
    glColor3f(0.36, 0.65, 0.94)
    glBegin(GL_TRIANGLES)
    glVertex2f(550, 295)
    glVertex2f(550, 340)
    glVertex2f(600, 340)
    glEnd() 

    glColor3f(0.36, 0.65, 0.94)
    glBegin(GL_TRIANGLES)
    glVertex2f(550, 295)
    glVertex2f(600, 295)
    glVertex2f(600, 340)
    glEnd() 

    # railing
    glColor3f(0.0, 0.0, 0.0)  
    glLineWidth(3)        
    glBegin(GL_LINES)     
    glVertex2f(575, 340)
    glVertex2f(575, 295)
    glVertex2f(550, 317.5)
    glVertex2f(600, 317.5)
    glEnd()

# Essential Functions

def setup_projection():
    glViewport(0, 0, 1000, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    draw_background()
    draw_fields()
    draw_trees()
    house_body()
    house_shed()
    house_door()
    house_window()
    draw_rain()

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(1000,600)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"House in Rainfall")

    populateRain()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)

    glutMainLoop()

if __name__=="__main__":
    main()