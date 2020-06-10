import turtle
import random
import math
import playsound

#speed
player_maxspeed=2
enemy_speed=1

#game boarder settigs
boarder_len=600
boarder_wid=600
#after boundary collision
rotating_angle=60

Screen=turtle.Screen()
Screen.title("Space fighter")
Screen.setup(width=1020,height=768)
Screen.bgcolor("black")
Screen.tracer(0)

class Element(turtle.Turtle):
    def __init__(self,shapee,colour,xpos,ypos):
        turtle.Turtle.__init__(self)
        self.shape(shapee)
        self.speed(0)
        self.penup()
        self.color(colour)
        self.goto(xpos,ypos)
        # self.pendown()
        self.speed=1
    
    def move(self):
        self.forward(self.speed)

        #boundary collision check
        if self.xcor() > 290:
            self.setx = 290
            self.right(rotating_angle)
        
        if self.xcor() < -290:
            self.setx = -290
            self.right(rotating_angle)

        if self.ycor() > 290:
            self.setx = 290
            self.right(rotating_angle)

        if self.ycor() < -290:
            self.setx = -290
            self.right(rotating_angle)
               
    def collision(self, other):
        d=math.hypot(self.xcor()-other.xcor(),self.ycor()-other.ycor())
        if d<=20:
            return True
        else:
            return False
        


# class boundary(Element):
#     def __init__(self,shapee,colour,xpos,ypos):
#         Element.__init__(self,shapee,colour,xpos,ypos)

    # def draw_boarder(self):
    #     self.pensize(3)
    #     self.pendown()

    #     for i in range(2):
    #         self.forward(800)
    #         self.left(90)
    #         self.forward(600)
    #         self.left(90)
    #     self.penup()
    #     self.hideturtle()

class Player(Element):
    def __init__(self,shapee,colour,xpos,ypos):
        Element.__init__(self,shapee,colour,xpos,ypos)
        self.shapesize(stretch_wid=0.5,stretch_len=1)

    def turn_left(self):
        self.setheading(180)
    
    def turn_right(self):
        self.setheading(0)

    def turn_up(self):
        self.setheading(90)

    def turn_down(self):
        self.setheading(270)

    def acclerate(self):
        if self.speed <player_maxspeed:
            self.speed+=1
        else:
            pass

            

    def decelerate(self):
        if self.speed >1:
            self.speed-=1
        else:
            pass



class Enemy(Element):
    def __init__(self,shapee,colour,xpos,ypos):
        Element.__init__(self,shapee,colour,xpos,ypos) 
        self.speed=enemy_speed
        self.setheading(random.randint(0,360))
#-------------------------------------------------------------------------
class Friend(Element):
    def __init__(self,shapee,colour,xpos,ypos):
        Element.__init__(self,shapee,colour,xpos,ypos) 
        self.speed=enemy_speed
        self.setheading(random.randint(0,360))

    def move(self):
        self.forward(self.speed)

        #boundary collision check
        if self.xcor() > 290:
            self.setx = 290
            self.left(rotating_angle)
        
        if self.xcor() < -290:
            self.setx = -290
            self.left(rotating_angle)

        if self.ycor() > 290:
            self.setx = 290
            self.left(rotating_angle)

        if self.ycor() < -290:
            self.setx = -290
            self.left(rotating_angle)   


class Bullet(Element):
    def __init__(self,shapee,colour,xpos,ypos):
        Element.__init__(self,shapee,colour,xpos,ypos)
        self.shapesize(stretch_wid=0.2,stretch_len=0.5,outline=None)
        self.penup()
        self.goto(-5000,5000)
        self.status="waiting"
        self.speed=10
    
    def shot(self):
        if self.status=="waiting":
            self.goto(character.xcor(),character.ycor())
            self.status="firing"
            playsound.playsound("missile.mp3",False) 
    
    def fired(self):
        if self.status=="firing":
            self.setheading(character.heading())
            self.forward(self.speed)   
            


        #bullet crossing boundary
        if self.xcor()>290 or self.xcor() <-290 \
            or self.ycor() >290 or self.ycor()< -290:
            self.goto(-5000,5000)
            self.status="waiting"
        else:
            pass



class Game_progress():
    def __init__(self):
        self.score=0
        self.lives=3
        self.state="ready"
        self.pen=turtle.Turtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.pencolor("white")
        self.pen.goto(-boarder_len/2,-boarder_wid/2)

    
    def draw_boarder(self):
        self.pen.speed(0)
        self.pen.pensize(3)
        self.pen.pendown()
        

        for i in range(2):
            self.pen.forward(boarder_len)
            self.pen.left(90)
            self.pen.forward(boarder_wid)
            self.pen.left(90)
        self.pen.penup()
        self.pen.hideturtle()

    def update(self):
        self.pen.undo()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.speed(0)       
        self.pen.goto(-310,310)
        self.pen.write(f"STAR WARS          Score:{self.score} Live:{self.lives}")
        self.pen.penup()
        

#drawing player element
character=Player("triangle","green",0,0)
#drawing boundary element
game1=Game_progress()
game1.draw_boarder()
game2=Game_progress()


#draw enemy 
enemies=[]
for i in range(6):
    enemies.append(Enemy("circle","red",random.randint(-300,300),random.randint(-300,300)))

#friend
friends=[]
for i in range(6):
    friends.append(Friend("triangle","blue",0,0))


#making bullet
bullet=Bullet("triangle","yellow",0,0)

##keyboard inputs and controls guide-------------------------------------
turtle.listen()
turtle.onkey(character.turn_left,"a")
turtle.onkey(character.turn_right,"d")
turtle.onkey(character.turn_up,"w")
turtle.onkey(character.turn_down,"s")
turtle.onkeypress(character.acclerate,"Up")
turtle.onkeypress(character.decelerate,"Down")
turtle.onkey(bullet.shot,"space")
##------------------------------------------------------------------------

while True:

    turtle.update()
    character.move()
    game2.update()
    bullet.fired()

    for enemy in enemies:
        enemy.move()
        #collision with enemy check
        if character.collision(enemy):
            enemy.goto(random.randint(-200,200),random.randint(-200,200))
            game2.lives-=1
            playsound.playsound("explosion.mp3",False)
        else:
            pass

        #collision of bullet and enemy
        if bullet.collision(enemy):
            enemy.goto(random.randint(-200,200),random.randint(-200,200))
            bullet.goto(-5000,5000)
            bullet.status="waiting"
            game2.score+=100
        else:
            pass

    for friend in friends:
        friend.move()

        #collision of bullet and friend
        if bullet.collision(friend):
            friend.goto(random.randint(-200,200),random.randint(-200,200))
            bullet.goto(-5000,5000)
            bullet.status="waiting"
            game2.score-=50
            playsound.playsound("explosion.mp3",False)
        else:
            pass

    if game2.lives==0:
        exit()

turtle.done()