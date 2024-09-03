import pygame
import sys

pygame.init()
pygame.font.init()

BLACK=(255,255,255)
WHITE=(0,0,0)
YELLOW = (255, 255, 0)


# will display the screen 
screen_length = 600
screen_height = 400
window = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("ECHOES OF THE MULTIVERSE")
font = pygame.font.SysFont('Comic Sans', 48)
char_1 = pygame.image.load("iron warrior.png").convert_alpha()
char_2 = pygame.image.load("captainwillie.png").convert_alpha()
char_3 = pygame.image.load("stormbreak.png").convert_alpha()
char_1 = pygame.transform.scale(char_1, (100, 100))
char_2 = pygame.transform.scale(char_2, (100, 100))
char_3 = pygame.transform.scale(char_3, (100, 100))

laser_img = pygame.image.load("laser.jpg").convert_alpha()
laser_img=pygame.transform.scale(laser_img,(20,10))
laptopshot_img = pygame.image.load("willie sheild.jpg").convert_alpha()
laptopshot_img=pygame.transform.scale(laptopshot_img,(20,10))
thunder_img = pygame.image.load("thunder.jpg").convert_alpha()
thunder_img=pygame.transform.scale(thunder_img,(20,10))
#the blueskull
enemy_photo=pygame.image.load("blueskull.jpeg").convert_alpha()
enemy_photo=pygame.transform.scale(enemy_photo,(100,100))
char_images = {
        "IRON WARRIOR": char_1,
        "CAPTAIN WILLIE": char_2,
        "STORMBREAK": char_3
    }



char_1_posi=(50,screen_height-150)
char_2_posi=(50,screen_height-150)
char_3_posi=(50,screen_height-150)
enemy_pos=(450,250)

players_healthy=150
blueskull_healthy=150
class Heroes:
    def __init__(self,image,bullet_img,bullet_speed,typesof_bullet):
        self.image=image
        self.bullet_img=bullet_img
        self.typesof_bullet= typesof_bullet
        self.bullet_speed=bullet_speed

    def firing_bullettypes(self, x, y):
        return[Bullet(self.bullet_img, x - 80 , y - 10, self.bullet_speed)]
        
    
    def draw(self, window, x, y):
        window.blit(self.image, (x, y))

class  Bullet:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        
    def move(self):
        self.x += self.speed
    def draw(self,window):
         window.blit(self.image, (self.x, self.y))          
class Blueskull:
    def __init__(self, image,x,y):
        self.image=image
        self.x=x
        self.y=y
        self.direction=1
        self.speed= 0.25

    def move(self):
        self.y += self.direction * self.speed
        if self.y <=50 :
            self.direction=1 
        elif self.y >= screen_height -150:
            self.direction = -1

    def draw(self,window):
        window.blit(self.image,(self.x,self.y))

 
ironwarrior=Heroes(char_1,laser_img,3,"laser")
captainwillie=Heroes(char_2,laptopshot_img,3,"laptopshot")
stormbreak=Heroes(char_3,thunder_img,3,"thunder")
def get_hero_by_name(name):
    if name == "IRON WARRIOR":
        return ironwarrior
    elif name == "CAPTAIN WILLIE":
        return captainwillie
    elif name == "STORMBREAK":
        return stormbreak
def start_level_4(selected_chara):
    global charaselect
    charaselect = get_hero_by_name(selected_chara)
    if charaselect is None:
         print("Invalid character selected!")
         return

       

bullets=[]
maximum_bullet=12
bullet_cooldowntime =300
last_shot_timimg=pygame.time.get_ticks()
players_x,players_y= 0, screen_height-120

blueenemy=Blueskull(enemy_photo,enemy_pos[0],enemy_pos[1])

running = True
while running:
   current_timimg=pygame.time.get_ticks()
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_timimg -last_shot_timimg > bullet_cooldowntime:
                        if len(bullets) < maximum_bullet:
                            new_bullety=charaselect.firing_bullettypes(players_x,players_y)
                            bullets.extend(new_bullety)
                            last_shot_timimg =current_timimg
   for bullet in bullets[:]:
        bullet.move()
        if bullet.x > screen_length:
            bullets.remove(bullet)
        elif blueenemy.x <  bullet.x < blueenemy.x +150 and blueenemy.y <bullet.y <blueenemy.y +150:
            bullets.remove(bullet)
            blueskull_healthy -=10

   window.fill(BLACK)  

   pygame.draw.rect(window, YELLOW,(10,10, players_healthy,20))
   pygame.draw.rect(window,YELLOW,(screen_length-blueskull_healthy-10,10,blueskull_healthy,20))

     
   
   charaselect.draw(window, players_x, players_y)



   blueenemy.move() 
   blueenemy.draw(window )
   for bullet in bullets:
        bullet.draw(window)
   
   pygame.display.update()

   if blueskull_healthy <=0:
       print("blueskull is defeated")
       running=False
   if players_healthy<=0:
       print("you are dead")
       running=False


pygame.quit()
sys.exit()  
      
            