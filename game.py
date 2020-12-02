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
        score_surface = game_font.render (str(int(score)),False,(0,0,0))
        score_rect = score_surface.get_rect (midright = (600,100))
        screen.blit(score_surface,score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score {int(score)}',False,(0,0,0))
        score_rect = score_surface.get_rect (midright = (600,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score {int(high_score)}',False,(0,0,0))
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
game_font = pygame.font.Font('/home/david/Desktop/Carritos/assets/ARCADECLASSIC.TTF',40)

#Game Variables
car_player_x_mov = 0
game_active = False
score = 0
high_score = 0
can_score = True
speed = 5
random_enemy = 0 

#Cover
game_over_sur = pygame.image.load('/home/david/Desktop/Carritos/assets/mucho lo rapido.png').convert_alpha()
game_over_rect = game_over_sur.get_rect(center = (350, 350))

#Background
bg_surface = pygame.image.load('/home/david/Desktop/Carritos/assets/grass.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_y_pos = 0

road_surface = pygame.image.load('/home/david/Desktop/Carritos/assets/road.png').convert()
road_y_pos = 0

#Car player
player_sur = pygame.image.load ('/home/david/Desktop/Carritos/assets/red_car.png').convert_alpha()
player_rect = player_sur.get_rect(center = (350, 500))

#Car enemies
black_car_sur = pygame.image.load ('/home/david/Desktop/Carritos/assets/black_car.png').convert_alpha()
grey_car_sur = pygame.image.load ('/home/david/Desktop/Carritos/assets/grey_car.png').convert_alpha()
white_car_sur = pygame.image.load ('/home/david/Desktop/Carritos/assets/white_car.png').convert_alpha()
enemy_sur = None
#Enemies movement
enemy_cars_list = []
SPAWNCAR = pygame.USEREVENT
pygame.time.set_timer(SPAWNCAR, 500)

#Explosion
#explosion_sur = pygame.image.load('/home/david/Desktop/Carritos/assets/explosion.png').convert_alpha()

#Sound
intro_music = pygame.mixer.Sound("/home/david/Desktop/Carritos/sound/intro.wav")
explosion_sound = pygame.mixer.Sound("/home/david/Desktop/Carritos/sound/explosion.wav")

while True:
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
                if game_active == False:
                    game_active = True
                    enemy_cars_list.clear()
                    player_rect.center = (350, 500)
                    car_player_x_mov = 0
                    score = 0
                    speed = 5
                    intro_music.play()
                else:
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
    
    if game_active == True: 
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
        intro_music.stop()
    else:
        screen.blit(game_over_sur,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")
        intro_music.play()

    pygame.display.update()
    clock.tick(120)