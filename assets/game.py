import pygame, sys, random 

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('/home/david/Desktop/flappy/FlappyBird_Python-master/assets/background-day.png').convert()


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		

	screen.blit(bg_surface,(0,0))
	pygame.display.update()
	clock.tick(120)
