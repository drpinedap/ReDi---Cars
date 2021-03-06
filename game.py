import pygame, sys, random, time

def draw_bg():
    screen.blit(bg_surface,(0,bg_y_pos))
    screen.blit(bg_surface,(0,road_y_pos-700))

def draw_road():
    screen.blit(road_surface,(175,road_y_pos))
    screen.blit(road_surface,(175,road_y_pos-700))

def create_enemy():
    global enemy_sur, random_enemy
    
    if  random_enemy == 0:
        enemy_sur = black_car_sur
    elif random_enemy == 1: 
        enemy_sur = black_car_sur
    elif random_enemy == 2: 
        enemy_sur = black_car_sur
    else: 
        enemy_sur = black_car_sur
    
    random_enemy_pos = random.randrange(200,500)
    new_enemy = enemy_sur.get_rect(midtop = ((random_enemy_pos),-1000))
    return  new_enemy

def move_enemy(enemies):
    for enemy in enemies:
        if speed == 1:
            enemy.centery += 1
        else: 
            enemy.centery += speed - 1        
    visible_enemies = [enemy for enemy in enemies if enemy.centery < 700]
    return visible_enemies  

def draw_enemy(enemies):
    for enemy in enemies:
        screen.blit(enemy_sur,enemy)

def check_collision(enemies):
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            explosion_sound.play()
            return False
    if player_rect.left <= 175 or player_rect.right >= 525:
        explosion_sound.play()
        return False
    return True

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render (str(score),False,(0,0,0))
        score_rect = score_surface.get_rect (midright = (600,100))
        screen.blit(score_surface,score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score {(score)}',False,(0,0,0))
        score_rect = score_surface.get_rect (midright = (600,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score {(high_score)}',False,(0,0,0))
        high_score_rect = high_score_surface.get_rect (midright = (600,200))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

def score_check():
    global score, can_score
    
    if enemy_cars_list:
        for enemy in enemy_cars_list:
            if 500 >= enemy.centery >= 496  and can_score is True:
                score += 1
                can_score = False
            if enemy.centery > 550:
                can_score = True

def speed_display(speed):
    speed_surface = game_font.render ((str(speed - 1)),False,(0,0,0))
    speed_rect = speed_surface.get_rect (midright = (600,200))
    screen.blit(speed_surface,speed_rect)


pygame.init()
screen = pygame.display.set_mode((700,600))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/ARCADECLASSIC.TTF',30)

#Game Variables
car_player_x_mov = 0
game_active = False
score = 0
high_score = 0
can_score = True
speed = 5
random_enemy = 0 
selection_car = 0

#Cover
game_over_sur = pygame.image.load('assets/mucho lo rapido.png').convert_alpha()
instruction_sur = pygame.image.load("assets/keys.png").convert_alpha()
game_over_rect = game_over_sur.get_rect(center = (350, 300))
instruction_rect = instruction_sur.get_rect(center = (250,500))
instru_text_1_sur = game_font.render(f'to  start',False,(0,0,0))
instru_text_1_rect = instru_text_1_sur.get_rect (center = (450,450))
instru_text_2_sur = game_font.render(f'to  move or',False,(0,0,0))
instru_text_2_rect = instru_text_2_sur.get_rect (center = (460,515))
instru_text_3_sur = game_font.render(f'change car',False,(0,0,0))
instru_text_3_rect = instru_text_3_sur.get_rect (center = (460,540))

#Background
bg_surface = pygame.image.load('assets/grass_1.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_y_pos = 0

road_surface = pygame.image.load('assets/road.png').convert()
road_y_pos = 0

#Car player
player_sur = pygame.image.load ('assets/red_car.png').convert_alpha()
player_rect = player_sur.get_rect(center = (350, 500))

#Car enemies
black_car_sur = pygame.image.load ('assets/black_car.png').convert_alpha()
grey_car_sur = pygame.image.load ('assets/grey_car.png').convert_alpha()
white_car_sur = pygame.image.load ('assets/white_car.png').convert_alpha()
enemy_sur = None
#Enemies movement
enemy_cars_list = []
SPAWNCAR = pygame.USEREVENT
pygame.time.set_timer(SPAWNCAR, 500)

#Explosion
explosion_sur = pygame.image.load('/home/david/Desktop/Carritos/assets/explosion.png').convert_alpha()

#Sound
intro_music = pygame.mixer.Sound("sound/intro.wav")
explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
motor = pygame.mixer.Sound("sound/motor.wav")

    
#Game loop
while True:
    
    # Screen movement
    bg_y_pos += speed 
    draw_bg()
    if bg_y_pos >= 700:
        bg_y_pos = 0    
    
    #Road movement
    road_y_pos += speed 
    draw_road()
    if road_y_pos >= 700:
        road_y_pos = 0

    #in Menu
    if game_active == False:
        enemy_cars_list.clear()
        player_rect.center = (350, 500)
        car_player_x_mov = 0
        score = 0
        speed = 5
        
        
        intro_music.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selection_car +=1
                    if selection_car > 2:
                        selection_car = 0
                if event.key == pygame.K_LEFT:
                    selection_car -=1
                    if selection_car < 0:
                        selection_car = 2
                if event.key == pygame.K_UP:
                    #Restore game to 0
                    game_active = True

            if selection_car == 0:
                player_sur = pygame.image.load ('assets/red_car.png').convert_alpha()
                player_rect = player_sur.get_rect(center = (350, 500))            
            if selection_car == 1:
                player_sur = pygame.image.load ('assets/blue_car.png').convert_alpha()
                player_rect = player_sur.get_rect(center = (350, 500)) 
            if selection_car == 2:
                player_sur = pygame.image.load ('assets/green_car.png').convert_alpha()
                player_rect = player_sur.get_rect(center = (350, 500))  
 


                
        screen.blit(game_over_sur,game_over_rect)
        screen.blit(player_sur,(player_rect))
        screen.blit(instruction_sur,instruction_rect)
        screen.blit(instru_text_1_sur,instru_text_1_rect)
        screen.blit(instru_text_2_sur,instru_text_2_rect)  
        screen.blit(instru_text_3_sur,instru_text_3_rect)       
        high_score = update_score(score,high_score)
        score_display("game_over")
        intro_music.play()
        motor.stop()

    #Events
    
    #in game
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    car_player_x_mov += 2 
            
                if event.key == pygame.K_LEFT:
                    car_player_x_mov -= 2
            
                if event.key == pygame.K_UP:
                    car_player_x_mov = 0
                    speed += 1
                    if speed > 5:
                        speed = 5
                if event.key == pygame.K_DOWN:
                    speed -=  1
                    if speed < 5:
                        speed = 5
       
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    car_player_x_mov=0
  

            if event.type == SPAWNCAR:
                random_enemy = random.randrange(0,4)
                enemy_cars_list.append(create_enemy())
            
    #Player movement
        player_rect.centerx += car_player_x_mov
        screen.blit(player_sur,(player_rect))
        
        #Enemies
        enemy_list = move_enemy(enemy_cars_list)
        draw_enemy(enemy_list)

        #Collision
        game_active = check_collision(enemy_list)

        #Score
        score_check()
        score_display("main_game")
        #speed_display(speed)
        motor.play()
        intro_music.stop()

    pygame.display.update()
    clock.tick(120)