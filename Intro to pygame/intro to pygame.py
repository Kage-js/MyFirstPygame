import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: 
            self.gravity = -20 
            print(self.gravity)
  
            
    def apply_gravity(self):
        self.gravity += 1 
        print(self.gravity)
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: 
            self.rect.bottom = 300   
                 
    def update(self):
        self.player_input()
        self.apply_gravity()
        
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'{current_time}',False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):

    if obstacle_list:
        for obstacle_rect in obstacle_list: 
            obstacle_rect.x -=5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

            obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return[]

def collisions(player,obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom<300:
        player_surface = player_jump 
    else: 
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0 

        player_surface = player_walk[int(player_index)]


pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)
game_active = False
start_time = 0 
score = 0 

player = pygame.sprite.GroupSingle()
player.add(Player())


#background
sky_surface = pygame.image.load("Sky.png").convert()
ground_surface = pygame.image.load("ground.png").convert()

#score_surface = test_font.render("my game", False, 'black').convert()
#score_rectangle = score_surface.get_rect(midbottom = (400,50))

#obstacles 
snail_frame1 = pygame.image.load('snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('snail2.png').convert_alpha()
snail_frame = [snail_frame1, snail_frame2]
snail_index = 0 
snail_surf = snail_frame[snail_index]

fly_frame1 = pygame.image.load('fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('fly2.png').convert_alpha()
fly_frame = [fly_frame1, fly_frame2]
fly_index = 0
fly_surf = fly_frame[fly_index]




obstacle_rect_list= []

player_walk_1 = pygame.image.load('player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0 
player_jump = pygame.image.load('jump.png')

player_surface = player_walk[player_index]

player_rectangle = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0



# intro screen
player_stand = pygame.image.load('player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
stand_rectangle = player_stand.get_rect(center = (400,200))

title_text = test_font.render("running game thing", False, 'black').convert()
title_rectangle = title_text.get_rect(center = (400,50))
instruction_text = test_font.render("Press 'Space' to begin!",False,"black")
instruction_rectangle = instruction_text.get_rect(center=(400,300))

#timer 

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
 
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

#game loop
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom>=300:
                    player_gravity = -20

            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                  player_gravity = -20
        else:
            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_SPACE and game_active == False:
                    print("restart")
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000) 


        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1100), 210)))
            #snail timer 
            if event.type == snail_animation_timer:
                if snail_index == 0: 
                    snail_index = 1
                else: 
                    snail_index = 0 
                snail_surf = snail_frame[snail_index]
            #fly timer         
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frame[fly_index]
    



    if game_active: 
        

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        #pygame.draw.line(screen,'Pink',(800,0),(0,400))
        #screen.blit(score_surface,(score_rectangle))
        score = display_score()

        #player 
        player_gravity += 1 
        player_rectangle.y += player_gravity

        if player_rectangle.bottom > 300:
            player_rectangle.bottom = 300

        player_animation()
        screen.blit(player_surface,(player_rectangle))
        player.draw(screen)
        player.update()
        
        #Obstacle movement 
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision 
        game_active = collisions(player_rectangle,obstacle_rect_list)
        
    else: 
        screen.fill((94,129,162))
        screen.blit(player_stand,stand_rectangle)
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0 

        score_message = test_font.render(f'your score {score}',False,('black'))
        score_message_rectangle = score_message.get_rect(center=(400, 300))
        screen.blit(title_text,title_rectangle)
        
       
        if score == 0: 
            screen.blit(instruction_text,instruction_rectangle)
        else:
            screen.blit(score_message,score_message_rectangle)

        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and game_active == False:
                print("restart")
                game_active = True

    pygame.display.update()
    clock.tick(60)