import pygame, sys
import random

#initialisation
pygame.init()
pygame.mixer.init()
running = True
font = pygame.font.SysFont(None,30)
pause = False
game_over = False
start_game = False
enemies = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60

#display window
background_color = (12, 3, 32)
resolution = (480,820)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("UFO Blitz")

#asset
player_image = pygame.image.load(r"Assets\sprites\spaceship.png").convert_alpha()
enemy_image = pygame.image.load(r"Assets\sprites\ufo.png").convert_alpha()
shoot_sound =pygame.mixer.Sound(r"Assets\sound\shot.mp3")
score_sound =pygame.mixer.Sound(r"Assets\sound\score.mp3")
music =pygame.mixer.Sound(r"Assets\sound\music.mp3")
background = pygame.image.load(r"Assets\sprites\background.jpg")
#highscore
high_score_file = open("highscore.txt", "r")
high_score = int(high_score_file.read())
high_score_file.close()
music.set_volume(0.5)
music.play(loops=-1)
spceship_scale = 6
enemy_scale = 7
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        super().__init__()
        self.image = player_image  # Sprite image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() *spceship_scale,self.image.get_height()*spceship_scale ))
        self.rect = self.image.get_rect()  # Get rect from image
        self.rect.topleft = (x, y)  # Starting position
        self.speed = speed
        self.projectiles = pygame.sprite.Group() 
    def update(self,keys):
        #movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        #keeping in bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 480:
            self.rect.right = 480
        self.projectiles.update()
    
    def shoot(self):
        global pause
        global start_game
        if not pause and start_game and not game_over:
            bullet = Projectile(self.rect.centerx, self.rect.top)
            self.projectiles.add(bullet)
            shoot_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = enemy_image  # Sprite image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * enemy_scale,self.image.get_height() * enemy_scale))
        self.rect = self.image.get_rect()  # Get rect from image
        self.rect.topleft = (x, y)  # Starting position
        self.speed = random.randint(2,7)
    def update(self):
        global game_over
        self.rect.y += self.speed
        if self.rect.top > 820 :  # if it goes off the bottom of the screen
            self.kill()  # removes itself from the group
            game_over = True
        elif game_over:
            self.kill()

        

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill("yellow")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  # Remove from group when off-screen

#gameobjects
player_speed = 8
player = Player(100, 700,player_speed)
enemy = Enemy(100,0)
score = 0


def pause_menu():
    pause_text = font.render("PAUSED", True, (255,255,255))
    screen.blit(pause_text, (190,410))
def draw_ufo():
    if random.randint(0, 100) < 1: #spawn rate
        x = random.randint(0, resolution[0] - 60)  # random x position
        new_enemy = Enemy(x, 0)
        enemies.add(new_enemy)
    enemies.update()
    enemies.draw(screen)
def hit_detection():
    for bullet in player.projectiles:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True) #Kills enemy
        if hit_enemies:
            bullet.kill()  # Destroy the bullet
            global score
            score +=1
            score_sound.play()
def scoreboard():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, "white")
    # Blit to screen at top-left corner
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (200, 10))    
def draw_spaceship():
    keys = pygame.key.get_pressed()
    player.update(keys)
    screen.blit(player.image, player.rect)
    player.projectiles.update
    player.projectiles.draw(screen)
def game_over_screen():
    game_over_text = font.render("GAME OVER! press R to restart",True,(255,255,255))
    screen.blit(game_over_text, (100,410))
    global pause
    global score
    global high_score
    pause = True
    if score > high_score:
        high_score = score

#game loop
while running:
    #fps
    clock.tick(fps)
    #Event handeling
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                if not pause:
                    pause = True
                else:
                    pause = False
            if event.key == pygame.K_RETURN:
                start_game = True
            if event.key ==pygame.K_r:
                game_over= False
                pause = False
                score = 0
    #game logic
    if start_game:        
        if not pause:
            #background
            screen.fill(background_color)
            screen.blit(background, (0,0))
            #drawing spaceship
            draw_spaceship()
            #drawing ufo
            draw_ufo()
        
            #enemy hit detection
            hit_detection()
        
            #render score
            scoreboard()
        elif pause and not game_over :
            pause_menu()
        if game_over :
            game_over_screen()
            
    else:
        start_game_text = font.render("Press ENTER to start", True,"white")
        screen.blit(start_game_text, (140,410))

    #update display
    pygame.display.flip()

#Save the high score
high_score_file = open("highscore.txt","w")
high_score_file.write(str(high_score))
high_score_file.close()

#quit the game
pygame.quit()
sys.exit()