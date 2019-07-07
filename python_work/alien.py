import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
		def __init__(self,ai_settings,screen):
			#init alien & set first loc
			super(Alien,self).__init__()
			self.screen = screen
			self.ai_settings = ai_settings
			
			#loding alien picture & set rect
			image = pygame.image.load('image/alien.png')
			self.image = pygame.transform.scale(image,(50,50))
			self.rect = self.image.get_rect()
			
			#every alien first loc on left_up
			self.rect.x = self.rect.width
			self.rect.y = self.rect.height
			
			#hold alien exact loc
			self.x = float(self.rect.x)	
        
		def blitme(self):
			#draw alien in loc
			self.screen.blit(self.image,self.rect)

		def update(self):
			#right || left move alien
			self.x += (self.ai_settings.alien_speed_factor *
						self.ai_settings.fleet_direction)
			self.rect.x = self.x
			
		def check_edges(self):
			#if alien with screen edge 'true'
			screen_rect = self.screen.get_rect()
			if self.rect.right >= screen_rect.right:
				return True
			elif self.rect.left <= 0:
				return True
				
