class GameStats():
#follow statistics information

	def __init__(self,ai_settings):
		#init stat information
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		self.high_score = 0
		
			
	def reset_stats(self):
		#init stat information - change
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
