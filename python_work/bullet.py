import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	#class about bullet
	
	def __init__(self,ai_settings,screen,ship):
		#build bullet on ship loc
		super(Bullet,self).__init__()
		self.screen = screen 
		
		#on(0,0)build bullet ,set true loc
		self.rect = pygame.Rect(0,0,ai_settings.bullet_width,
			ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		#hold min number to bullet loc
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
	def update(self):
		#upward move bullet
		#update show bullet loc min number_class
		self.y -= self.speed_factor
		self.rect.y = self.y
		#draw bullet on phone
		pygame.draw.rect(self.screen,self.color,self.rect)
		
	def draw_bullet(self):
		pygame.draw.rect(self.screen,self.color,self.rect)
			

