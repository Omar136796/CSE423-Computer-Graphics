from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Given variables
fovY=120
GRID_LENGTH=650

# Arena variables
grid_gap=100
max_border=(GRID_LENGTH-50)
border_height=150

# Camera variables
camera_angle=0
camera_radius=540
camera_height=540
toggle=False

# Player variables
player_x=0
player_y=0
player_movement_angle=0
player_speed=20

# Enemy variable
start_time=time.time()
enemy_speed=0.3
enemy_list=[]
max_enemy=5

# Character shapes
player_body_size=70
player_head_size=18
enemy_body_size=30
enemy_head_size=20 

# Score Stat variables
player_life=5
score=0
bullets_missed=0

# Bullet variables
bullets_list=[]
bullet_size=10
bullet_speed=30

# Game state variable
game_over=False
player_fall_angle=0

# Cheat mode variable
cheat_mode=False
cheat_rotation_speed=4
gun_following=False 
angle_difference_offset=(cheat_rotation_speed//2)

#################### Helper Functions ##############################

def spawn_enemy():
    global max_border, enemy_list

    enemy_x=random.randint(-max_border,max_border)
    enemy_y=random.randint(-max_border,max_border)
    enemy_list.append({"x": enemy_x, "y": enemy_y})

def initialize_enemies():
    global enemy_list, max_enemy

    enemy_list=[]

    for i in range(max_enemy):
        spawn_enemy()

def camera_position():
    global camera_angle, camera_radius, camera_height

    theta=math.radians(camera_angle)
    x=camera_radius*math.cos(theta)
    y=camera_radius*math.sin(theta)

    return (x,y,camera_height)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 800)
 
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_arena():
    global grid_gap

    for i in range(-GRID_LENGTH,GRID_LENGTH,grid_gap):
        even_odd=0
        glBegin(GL_QUADS)
        for j in range(-GRID_LENGTH,GRID_LENGTH,grid_gap):
            even_odd=(i/grid_gap)+(j/grid_gap)
            even_odd=int(even_odd)
            if even_odd%2==0:
                glColor3f(0.7,0.5,0.95)
            else:
                glColor3f(1,1,1)
                
            glVertex3f(i,j,0)
            glVertex3f(i+grid_gap,j,0)
            glVertex3f(i+grid_gap,j+grid_gap,0)
            glVertex3f(i,j+grid_gap,0)   

            even_odd+=1

        glEnd()

def draw_border():
    global border_height

    glBegin(GL_QUADS)

    # left border
    glColor3f(0, 0, 1)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,border_height)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,border_height)

    # right border
    glColor3f(0, 1, 0)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,border_height)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,border_height)

    # top border
    glColor3f(0, 1, 1)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,border_height)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,border_height)
    
    # bottom border
    glColor3f(1, 1, 1)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,border_height)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,border_height)

    glEnd()

def draw_player():
    global player_x, player_y, player_movement_angle, game_over, player_fall_angle, player_body_size, player_head_size

    glPushMatrix() 
    glTranslatef(player_x, player_y, 0)
    
    if game_over==True:
        glRotatef(player_fall_angle, 1, 0, 0) 
    else:
        glRotatef(player_movement_angle, 0, 0, 1)

    # Creating Legs
    glColor3f(0, 0, 1)

    # Left leg
    glPushMatrix()
    glTranslatef(0, -27, 0)        
    gluCylinder(gluNewQuadric(), 6, 15, 40, 220, 120) 
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0, 27, 0)      
    gluCylinder(gluNewQuadric(), 6, 15, 40, 220, 120)
    glPopMatrix()

    # Creating Body
    glPushMatrix()
    glColor3f(0.4, 0.5, 0.2)
    glTranslatef(0, 0, 70)
    glScalef(0.6, 0.9, 1.0)
    glutSolidCube(player_body_size)            
    glPopMatrix()

    # Creating Arms
    glColor3f(0.9, 0.8, 0.6)

    # Right arm
    glPushMatrix()
    glTranslatef(20, -25, 90)      
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 6, 35, 12, 12)
    glPopMatrix()

    # Left arm
    glPushMatrix()
    glTranslatef(20, 25, 90)       
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 6, 35, 12, 12)
    glPopMatrix()

    # Creating Gun
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(20, 0, 85) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 45, 20, 20)
    glPopMatrix()

    # Creating Head
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 120)
    gluSphere(gluNewQuadric(), player_head_size, 12, 12)
    glPopMatrix()

    glPopMatrix() 

def enemy_pulsate(time_elapsed):
    time_elapsed=(time_elapsed%2)
    if 1<time_elapsed:
        time_elapsed=(2-time_elapsed)
    return time_elapsed

def draw_enemy(enemy_x, enemy_y, time_elapsed):
    global game_over, enemy_body_size, enemy_head_size
    
    if game_over==True:
        return

    glPushMatrix() 

    glTranslatef(enemy_x, enemy_y, 0)
    pulsated_time=enemy_pulsate(time_elapsed)
    scaling_factor=1.0+(0.7*pulsated_time)
    glScalef(scaling_factor, scaling_factor, scaling_factor)

    # Enemy Body
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), enemy_body_size, 30, 30)

    # Enemy Head
    glTranslatef(0, 0, 50)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), enemy_head_size, 30, 30)

    glPopMatrix()

def draw_bullets(ammo):
    global bullet_size, game_over
    
    if game_over==True:
        return

    glPushMatrix()
    glTranslatef(ammo["x"], ammo["y"], 85)
    glColor3f(1, 0, 0)  
    glutSolidCube(bullet_size)
    glPopMatrix()

def line_of_sight_check(enemy, gun_angle):
    global player_x, player_y, angle_difference_offset

    distance_x=enemy["x"]-player_x
    distance_y=enemy["y"]-player_y
    angle_in_radian=math.atan2(distance_y, distance_x)
    angle_in_degree=math.degrees(angle_in_radian)
    
    gun_angle=(gun_angle%360)
    angle_in_degree=(angle_in_degree%360) 
    
    angle_diff=abs(gun_angle-angle_in_degree)

    if angle_diff>180:
        angle_diff=(360-angle_diff) 
    
    if angle_diff<=angle_difference_offset:
        return True
    else:
        return False
    
#################### Necessary Functions ##############################

def keyboardListener(key, x, y):
    global player_movement_angle, player_x, player_y, player_speed, max_border, game_over, player_life, score, bullets_missed, enemy_list, bullets_list, player_fall_angle, player_movement_angle, start_time, toggle, cheat_mode, cheat_rotation_speed, gun_following
    
    if key == b'r':
        if game_over==True:
            #Reset
            game_over=False
            player_fall_angle=0
            player_movement_angle=0
            player_x=0
            player_y=0
            player_life=5
            score=0
            bullets_missed=0
            bullets_list=[]
            enemy_list=[]
            toggle=False
            cheat_mode=False
            gun_following=False
            start_time=time.time()
            initialize_enemies()
            print("Game Restarted!")
            return
    
    if key == b'c':
        if not game_over:
            cheat_mode=not(cheat_mode)
            if cheat_mode==True:
                print(f"Cheat Mode: ON")
            else:
                print(f"Cheat Mode: OFF")
    
    if key == b'v':
        if not game_over and cheat_mode:

            gun_following = not(gun_following)
            if gun_following==True:
                print(f"Gun Following: ON")
            else:
                print(f"Gun Following: OFF")

        elif not game_over and not cheat_mode:
                print(f"Gun Following Mode only available in Cheat Mode!")

    if game_over==True:
        return
    
    dell_x=math.cos(math.radians(player_movement_angle))
    dell_y=math.sin(math.radians(player_movement_angle))

    if key == b'w':  
        new_player_x=player_x+(player_speed*dell_x) 
        new_player_y=player_y+(player_speed*dell_y) 

        if -max_border<new_player_x<max_border and -max_border<new_player_y<max_border:
            player_x=new_player_x 
            player_y=new_player_y 

    if key == b's':
        new_player_x=player_x-(player_speed*dell_x) 
        new_player_y=player_y-(player_speed*dell_y) 

        if -max_border<new_player_x<max_border and -max_border<new_player_y<max_border:
            player_x=new_player_x 
            player_y=new_player_y 

    if key == b'a' and not cheat_mode:
        player_movement_angle+=5

    if key == b'd' and not cheat_mode:
        player_movement_angle-=5

def specialKeyListener(key, x, y):
    global camera_angle, camera_height, game_over
    
    if game_over==True:
        return
    
    if key == GLUT_KEY_UP:
        camera_height+=5

    if key == GLUT_KEY_DOWN:
        camera_height-=5

    if key == GLUT_KEY_LEFT:
        camera_angle-=2  

    if key == GLUT_KEY_RIGHT:
        camera_angle+=2 

def mouseListener(button, state, x, y):
    global bullets_list, player_x, player_y, player_movement_angle, score, bullets_missed, game_over, toggle, cheat_mode
    
    if game_over==True:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not cheat_mode:
        bullets_list.append({"x": player_x, "y": player_y, "angle": player_movement_angle})
        print(f"Player Bullet Fired!")  


    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        toggle=not(toggle)

        if toggle==False:
            print("Switched Mode to Third Person.")
        else:
            print("Switched Mode to First Person.")

def setupCamera():
    global toggle, player_x, player_y, player_movement_angle, cheat_mode, gun_following, player_speed

    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    x, y, z = camera_position()

    if toggle==False:
        gluLookAt(x, y, z,  
                0, 0, 0,  
                0, 0, 1)  
    else:
        cam_x=player_x+(player_speed*math.cos(math.radians(player_movement_angle)))
        cam_y=player_y+(player_speed*math.sin(math.radians(player_movement_angle)))
        cam_z=120

        if cheat_mode==True and not gun_following:
            look_x=cam_x+1
            look_y=cam_y+0
        else:
            look_x=cam_x+math.cos(math.radians(player_movement_angle))
            look_y=cam_y+math.sin(math.radians(player_movement_angle))
        
        look_z=cam_z

        gluLookAt(
            cam_x, cam_y, cam_z,
            look_x, look_y, look_z,
            0, 0, 1
        )

def idle():
    global enemy_list, player_x, player_y, player_life, enemy_speed, bullets_list, bullet_speed, bullets_missed, score, start_time, max_enemy, max_border, game_over, player_fall_angle, cheat_mode, cheat_rotation_speed, player_movement_angle, gun_following
    
    ###############################################################
    # Game Over Check

    if not game_over:
        if player_life<=0 or bullets_missed>=10:
            game_over=True
            print("Game Over!")
            print(f"Final Score: {score}")
            player_fall_angle=0
            enemy_list=[]
            bullets_list=[]
            cheat_mode=False
            gun_following=False
    
    if game_over==True:
        player_fall_angle=90
        glutPostRedisplay()
        return
    
    #############################################################

    # Animate Cheat Mode
    
    if cheat_mode==True and not game_over:
        player_movement_angle+=cheat_rotation_speed

        for k in enemy_list:

            flag=line_of_sight_check(k, player_movement_angle)

            if flag==True:
                distance_x=k["x"]-player_x
                distance_y=k["y"]-player_y
                
                angle_in_rad=math.atan2(distance_y, distance_x)
                angle_in_degree=math.degrees(angle_in_rad)
                
                bullets_list.append({"x": player_x, "y": player_y, "angle": angle_in_degree})
                break

#################################################

    # Animate Enemy
    for i in enemy_list:
        distance_x=(player_x-i['x'])
        distance_y=(player_y-i['y'])
        angle=math.atan2(distance_y, distance_x)

        i['x']+=enemy_speed*math.cos(angle)
        i['y']+=enemy_speed*math.sin(angle)

        distance=math.sqrt(distance_x**2+distance_y**2)

        if distance<60:
            player_life-=1
            print("Remaining Player life:", player_life)

            new_x=random.randint(-max_border, max_border)
            new_y=random.randint(-max_border, max_border)

            i["x"]=new_x
            i["y"]=new_y

    ##################################################################

    # Animate Bullets
    
    for b in bullets_list:

        b['x']+=(bullet_speed*math.cos(math.radians(b['angle'])))
        b['y']+=(bullet_speed*math.sin(math.radians(b['angle'])))

        bullet_hit=False
        remove_enemy=None

        for e in enemy_list:
            distance=math.sqrt((b['x']-e['x'])**2+(b['y']-e['y'])**2)
            
            if distance<35:
                score+=1
                remove_enemy=e
                bullet_hit=True
                bullets_list.remove(b)
                break

        if bullet_hit==True and remove_enemy!=None and remove_enemy in enemy_list:
            enemy_list.remove(remove_enemy)
            spawn_enemy()

        if not bullet_hit:
            if (abs(b['x'])>GRID_LENGTH) or (abs(b['y'])>GRID_LENGTH):
                bullets_missed+=1
                print(f"Bullet missed: {bullets_missed}")
                bullets_list.remove(b)

    glutPostRedisplay()

def showScreen():
    global start_time, bullets_list, enemy_list, game_over, cheat_mode, gun_following

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    #************************************
    setupCamera()
    draw_arena()
    draw_border()
    draw_player()
    
    # Draw all enemies
    for e in enemy_list:
        t_enemy=(time.time()-start_time)
        draw_enemy(e["x"], e["y"], t_enemy)

    # Draw bullets
    for i in bullets_list:
        draw_bullets(i)

    if game_over==True:
        draw_text(10, 760, f"Game is Over. Your Score is : {score}")
        draw_text(10, 730, f"Press ''R''  to Restart the Game.")
        
    else:
        draw_text(10, 760, f"Player Life Remaining: {player_life}")
        draw_text(10, 730, f"Game Score: {score}")
        draw_text(10, 700, f"Player Bullet Missed: {bullets_missed}")
        
    glutSwapBuffers()

#################### Main Function ##############################
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Bullet Frenzy")

    initialize_enemies()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()