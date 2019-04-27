"""
Name: Lee Wai Lam
Student ID: 20262666
Email address: wlleeag@connect.ust.hk
"""

import turtle
import pygame
import random
pygame.init()
pygame.mixer.init(buffer=16)
lasersound = pygame.mixer.Sound('shoot.wav')
explodesound = pygame.mixer.Sound('explosion.wav')
victorysound = pygame.mixer.Sound('Victory_Fanfare.wav')
losesound = pygame.mixer.Sound("lose.wav")

window_height = 600
window_width = 600
window_margin = 50
update_interval = 25

player_size = 50
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10

enemy_number = 2
enemy_size = 50
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin
enemy_min_x = enemy_init_x
enemy_max_x = window_width / 2 - enemy_size *6
enemy_hit_player_distance = 30
enemy_speed = 2
enemy_speed_increment = 1
enemy_direction = 1
enemies = []
enemy_bullet = []

laser_width = 2
laser_height = 15
laser_speed = 20
laser_hit_enemy_distance = 20

player_mouse = turtle.Turtle()
player_mouse.up()
player_mouse.hideturtle()
player_mouse.goto(600,600)


interval = 1000

cheat = 1

def playermoveleft():

    x, y = player.position()
    if x - player_speed > -window_width / 2 + window_margin:
        player.goto(x - player_speed, y)

def playermoveright():
    x, y = player.position()
    if x + player_speed < window_width / 2 - window_margin:
        player.goto(x + player_speed, y)

def updatescreen():
    global enemy_direction, enemy_speed, cheat, count

    if cheat == 1:
        

        dx = enemy_speed * enemy_direction
        dy = 0

        x0 = enemies[0].xcor()
        if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:
            enemy_direction = -enemy_direction
            dy = -enemy_size / 2
            if enemy_direction > 0:
                enemy_speed = enemy_speed + enemy_speed_increment

        for enemy in enemies:
            x, y = enemy.position()
            enemy.goto(x + dx, y + dy)
            if (x//20)%2 == 0:
                enemy.shape("enemy.gif")
            else:
                enemy.shape("enemy2.gif")

    if laser.isvisible():
        laser.forward(laser_speed)
        if laser.ycor() > window_height/2:
            laser.hideturtle()
    
        for enemy in enemies:
            if enemy.isvisible():
                if laser.distance(enemy) < laser_hit_enemy_distance:
                    enemy.hideturtle()
                    explodesound.play()
                    laser.hideturtle()
                    break

    if cheat == 1:
        
        for bullet in enemy_bullet:      
            if bullet.isvisible():
                bullet.forward(laser_speed)
                if bullet.ycor() < -window_height/2:
                    bullet.hideturtle()
                    enemy_bullet.remove(bullet)

        for enemy in enemies:
            if enemy.ycor() - player.ycor() < enemy_hit_player_distance:
                gameover("You lose!")
                losesound.play()
                return

        for bullet in enemy_bullet:    
            if bullet.isvisible():
                if bullet.distance(player) < laser_hit_enemy_distance:
                    player.hideturtle()
                    gameover("You lose!")
                    losesound.play()
                    return
            
    if cheat == -1:
        turtle.onscreenclick(die)

        

    count = 0
    for enemy in enemies:
        if enemy.isvisible():
            count = count + 1

    if count == 0:
        gameover("You win!")
        victorysound.play()
        return
    turtle.update()
    turtle.ontimer(updatescreen, update_interval)

def die(x,y):
    if cheat == -1:
        
        player_mouse.goto(x,y)
        for enemy in enemies:
            if player_mouse.distance(enemy) < laser_hit_enemy_distance:
                    enemy.hideturtle()
                    explodesound.play()


def shoot():
    if laser.isvisible() == False:
        if player.isvisible():
            
            laser.showturtle()
            x, y = player.position()
            laser.goto(x,y)
            lasersound.play()

def shoot_bullet():
    global enemy_bullet, count
    turtle.addshape("bomb.gif")
    if cheat == 1:
        attack = random.randint(0,(enemy_number-1))
        bx,by = enemies[attack].position()
        if enemies[attack].isvisible():
            bullet = turtle.Turtle()
            bullet.shape("bomb.gif")
            bullet.right(90)
            bullet.up()
            bullet.hideturtle()
            enemy_bullet.append(bullet)
            bullet.goto(bx,by)
            bullet.showturtle()
            if player.isvisible():
                turtle.ontimer(shoot_bullet, interval)
                
        if enemies[attack].isvisible() == False:
            if count > 0:
                shoot_bullet()
            
    if cheat == -1:
        turtle.ontimer(shoot_bullet, interval)
            
            


def gamestart(x,y):
    start_button.clear()
    start_button.hideturtle()
    Labels.clear()
    enemy_number_text.clear()
    Left_arrow.hideturtle()
    Right_arrow.hideturtle()
    text.clear()

    showtime.write("Shoot Interval:", font = ("System",10,"bold"))
    time.write(interval, font = ("System",10,"bold"))

    global player, laser

    turtle.addshape("spaceship.gif")
    player = turtle.Turtle()
    player.shape("spaceship.gif")
    player.up()
    player.goto(player_init_x, player_init_y)

    turtle.onkeypress(playermoveleft, "Left")
    turtle.onkeypress(playermoveright, "Right")

    turtle.listen()

    turtle.addshape("enemy.gif")
    turtle.addshape("enemy2.gif")

    for i in range(enemy_number):
        enemy = turtle.Turtle()
        enemy.shape("enemy.gif")
        enemy.up()

        enemy.goto(enemy_init_x + enemy_size * (i%6), enemy_init_y - enemy_size * (i//6))
        enemies.append(enemy)
        
    laser = turtle.Turtle()
    turtle.addshape("laser.gif")
    laser.shape("laser.gif")
    laser.left(90)
    laser.up()
    laser.hideturtle()

    turtle.onkeypress(shoot, "space")
    turtle.listen()
    turtle.update()

    turtle.ontimer(updatescreen, update_interval)
    turtle.ontimer(shoot_bullet, interval)

    turtle.onkeypress(decreasetime, ",")
    turtle.onkeypress(increasetime, ".")
    turtle.listen()

    turtle.onkeypress(cheat_mode,"s")
    turtle.listen()


def decreasetime():
    global interval,time
    if interval > 200:
        interval = interval - 100
        time.clear()
        time.write(interval, font = ("System",10,"bold"))

def increasetime():
    global interval,time
    if interval < 1000:
        interval = interval + 100
        time.clear()
        time.write(interval, font = ("System",10,"bold"))

    
def gameover(message):
    new = turtle.Turtle()
    new.hideturtle()
    new.color("yellow")
    new.write(message,align="center",font=("System", 30,"bold"))
    turtle.update()

def cheat_mode():
    global cheat
    cheat = cheat * (-1)
    
    

turtle.setup(window_width, window_height)
turtle.bgpic("Background.gif")
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

text = turtle.Turtle()
text.hideturtle()
text.color("white")
text.up()
text.goto(-130,120)
text.write("Python", font = ("System",80,"bold"))
text.goto(-150,50)
text.write("Angry Birds", font = ("System",50,"bold"))
text.goto(-100,0)
text.write("Control the Slingshot", font = ("System",20,"bold"))
text.goto(-100,-20)
text.write("using the arrow keys", font = ("System",20,"bold"))
text.goto(-100,-40)
text.write("and spacebar to shoot", font = ("System",20,"bold"))
text.goto(-100,-60)
text.write("and kill the enemies!", font = ("System",20,"bold"))

Labels = turtle.Turtle()
Labels.hideturtle()
Labels.color("white")
Labels.up()
Labels.goto(-120, -150)
Labels.write("Number of Enemies:", font=("Arial", 12, "bold"))

enemy_number_text = turtle.Turtle()
enemy_number_text.hideturtle()
enemy_number_text.color("white")
enemy_number_text.up()
enemy_number_text.goto(80,-150)
enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")

Left_arrow = turtle.Turtle()
Left_arrow.shape("arrow")
Left_arrow.color("white")
Left_arrow.shapesize(0.5,1)
Left_arrow.left(180)
Left_arrow.up()
Left_arrow.goto(60,-142)

Right_arrow = turtle.Turtle()
Right_arrow.shape("arrow")
Right_arrow.color("white")
Right_arrow.shapesize(0.5,1)
Right_arrow.up()
Right_arrow.goto(100,-142)

showtime = turtle.Turtle()
showtime.hideturtle()
showtime.up()
showtime.goto(130,280)
time = turtle.Turtle()
time.hideturtle()
time.up()
time.goto(250,280)

def decrease_enemy_number(x,y):
    global enemy_number
    if enemy_number > 1:
        enemy_number -= 1
        enemy_number_text.clear()
        enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")
def increase_enemy_number(x, y):   
    global enemy_number
    if enemy_number < 48 :
        enemy_number += 1 
        enemy_number_text.clear()
        enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")        

Left_arrow.onclick(decrease_enemy_number)
Right_arrow.onclick(increase_enemy_number)

start_button = turtle.Turtle()
start_button.up()
start_button.goto(-40, -230)
start_button.color("White", "DarkGray")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()
start_button.color("White")
start_button.goto(0, -225)
start_button.write("Start", font=("System", 12, "bold"), align="center")
start_button.goto(0, -228)
start_button.shape("square")
start_button.shapesize(1.25,4)
start_button.color("")
start_button.onclick(gamestart)
turtle.update()
turtle.done()
