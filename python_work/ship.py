import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self,ai_settings,screen):
		super(Ship,self).__init__()
		#picture location
		self.screen = screen
		self.ai_settings = ai_settings
		
		#loding picture
		image = pygame.image.load('image/eat_head.png')
		self.image = pygame.transform.scale(image,(50,50))
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#low bottom
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#attribute 'center' hold min math
		self.center = float(self.rect.centerx)
		
		#flag move
		self.moving_right = False
		self.moving_left = False
		
	def update(self):	
		#adjust position according to flag
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		elif self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
			
		#why 'self.center' update 'rect'		
		self.rect.centerx = self.center
		
		
	
	def blitme(self):
		#location draw
		self.screen.blit(self.image,self.rect)
		
	def center_ship(self):
		#put ship center on screen
		self.center = self.screen_rect.centerx
		
