import pygame
import random
import sys

pygame.init() #initialize the game
screen = pygame.display.set_mode((1280,720))  # setting the width, height 
clock = pygame.time.Clock() # intialising the clock
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("/Users/diya/Downloads/Dinosaur-Game-main/assets/PressStart2P-Regular.ttf")


class Cloud(pygame.sprite.Sprite):  # inheriting functionalities from already present pygame Sprite class.
    def __init__(self, image, x_pos, y_pos):
        super().__init__()   # taking the init method/attributes of the pygame sprite class and using it on our own sprite.
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) # making a rectangle using the coordinates and 
        # placing the cloud in the center of the rectangle. 

    def update(self):
        self.rect.x -= 1    # to place all the rectangles/sprite/cloud.

class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):   # we didnt pass velocity, gravity here because they are constant. 
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("/Users/diya/Downloads/Dinosaur-Game-main/assets/Dino1.png"),(80, 100)
        ))   # transforming the height and width of the dino image using transform.scale.
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("/Users/diya/Downloads/Dinosaur-Game-main/assets/Dino2.png"),(80, 100)
        ))   # transforming the height and width of the dino image using transform.scale.

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/DinoDucking1.png"), (110, 60)
        ))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/DinoDucking2.png"), (110, 60)
        ))

        self.x_pos = x_pos  # setting the x position
        self.y_pos = y_pos  # setting the y position
        self.current_image = 0  # index of the sprites list. starts from 0 so that we start from the first sprite
        self.image = self.running_sprites[self.current_image]  # took the first dino running image. 
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # again i made the rectangle with
        # the positons and filled the dino inside it. 
        self.velocity = 50  # constant velocity. 
        self.gravity = 4.5
        self.ducking = False  # running dino image. 

    # VAGUE
    def jump(self):
        jump_sfx.play()  # they are just playing the jump sound. 
        if self.rect.centery >= 360:
            while self.rect.centery - self.velocity > 40:  # it keeps on jumping until the person is pressing the button. 
                self.rect.centery -= 1 # jumping

    def duck(self):
        self.ducking == True # now the dino is the ducking dino 
        self.rect.centery = 380 #bending dino

    def unduck(self):
        self.ducking  == False  # running dino again. 
        self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360: # dino is jumping (in the air)
            self.rect.centery += self.gravity # adding the gravity to the centery position 
            #so that dino comes back to the ground
    
    def update(self):
        self.animate() # changing the dino pictures 
        self.apply_gravity()  # making dino come back to the ground again... after jump. 

    def animate(self):
        self.current_image += 0.05   # mystery 
        if self.current_image >= 2:  # out of the list of dinos, then go to the zero index dino again. 
            self.current_image = 0

        if self.ducking:   # if dino is a ducking dino i.e. self.ducking == True
            self.image = self.ducking_sprites[int(self.current_image)]
        else:  # if running dino
            self.image = self.running_sprites[int(self.current_image)]

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = [] # a lot of cactuses

        for i in range(1, 7): # because the pic names stats with "cactus1" 
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"/Users/diya/Downloads/Dinosaur-Game-main/assets/cacti/cactus{i}.png"), (100, 100)
            )
            self.sprites.append(current_sprite) # list of ordered cactus images

        self.image = random.choice(self.sprites) #choosing a random sprites from all 6 sprites
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed    # (speed is distance per sec) bc dino moves from left to right and cactus moves in opp direction
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 295, 350]) # low, mid, high postion for the bird
        self.sprites = []

        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero1.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero2.png"), (84, 62)))
        
        self.current_image = 0 # starts with 0 so that it picks the first bird
        self.image = self.sprites[self.current_image] # taking the image of the current sprite
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # boundary of bird

    def update(self):
        self.animate()
        self.x_pos -= game_speed   # bird is moving from right to left direction with the speed of the game.
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:  # if we are out of the list, then go back to the first image index(0) in the list. 
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]   # changing the images, so that it looks like its animating. 


# Global Variables
game_speed = 5
jump_count = 10
player_score = 0
game_over = False  # because the user is playing, game is still not over.
obstacle_timer = 0 # mystery.... 
obstacle_spawn = False  # right now no obstacle shows, as its start of the game, there is no obstacle on the screen. 
obstacle_cooldown = 1000  # how much time obstacle takes to come back again on the screen.

# Surfaces
ground = pygame.image.load("/Users/diya/Downloads/Dinosaur-Game-main/assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center = (640, 400)) #boundary

cloud = pygame.image.load("/Users/diya/Downloads/Dinosaur-Game-main/assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group() 
dino_group = pygame.sprite.GroupSingle() # all the dino will be present in the same group
ptero_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(50, 360)  # starting x_pos is 50, y_pos is 360. 
dino_group.add(dinosaur)  # added one dino with the starting pos in the group.

# Sounds
death_sfx = pygame.mixer.Sound("/Users/diya/Downloads/Dinosaur-Game-main/assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("/Users/diya/Downloads/Dinosaur-Game-main/assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("/Users/diya/Downloads/Dinosaur-Game-main/assets/sfx/jump.mp3")

# Events: you can control how your game responds to user
#  inputs therby increasing the intereactivity of your game

CLOUD_EVENT = pygame.USEREVENT # Custom event for cloud spawning
pygame.time.set_timer(CLOUD_EVENT, 3000) # 3 seconds (1000 ms = 1 s)
# Set a timer to trigger the cloud event every 3 seconds

# Functions

def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over", True, "black")
    game_over_rect = game_over_text.get_rect(center = (640,300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)

    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()

# infinite loop
while True:
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking == True:
            dinosaur.unduck()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()

                if game_over:  #reset variables
                    game_over = False
                    game_speed = 5
                    player_score = 0
    
    screen.fill("white")

    # Collisions
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0025
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1280, 340)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        cloud_group.update() # to change the x pos of the cloud
        cloud_group.draw(screen)  # to show cloud is moving to a new xpos
    
        ptero_group.update()
        ptero_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed

        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))  # show it on the screen

        if ground_x <= -1280:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()