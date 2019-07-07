import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
					bullets):
	#response button & mouse
	for event in pygame.event.get():
		if event == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,
								ship,aliens,bullets,mouse_x,mouse_y)
			
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,
						aliens,bullets,mouse_x,mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		aliens.empty()
		bullets.empty()
		
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
			
def check_keydown_events(event,ai_settings,screen,ship,bullets):	
	#reponse button	
	if event.key == pygame.K_RIGHT:
		#ship move to right
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		#ship move to left
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		
def fire_bullet(ai_settings,screen,ship,bullets):
	#build a bullet & join group(bullets)
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)	
		
def check_keyup_events(event,ship):	
	#reponse open
	if event.key == pygame.K_RIGHT:
		#ship move to right
		ship.moving_right = False			
	elif event.key == pygame.K_LEFT:
		#ship move to left
		ship.moving_left = False

def update_screen(ai_settings,screen,stats,sb,ship,aliens,
					bullets,play_button):
	#update picture on phone & switch phone 5
	
	#when every circle draw phone
	screen.fill(ai_settings.bg_color) 
	
	#behind ship & alien draw bullet
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	#draw "play" button
	if not stats.game_active:
		play_button.draw_button()
	
	#can see draw on recently
	pygame.display.flip()
	

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	bullets.update()
		
	#delete discover bullet
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	#check bullet if attack alien
	#if result is "true" delete alien & bullet
	check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,
									aliens,bullets)

def check_bullet_alien_collision(ai_settings,screen,stats,sb,
									ship,aliens,bullets):
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
		
	if len(aliens) == 0:
		#delete now_bullets & build new_aliens
		bullets.empty()
		ai_settings.initialize_dynamic_settings()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)
	
def create_fleet(ai_settings,screen,ship,aliens):
	#build aliens
	#build a alien & number how many a line
	#spacing alien
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_numner_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,
		alien.rect.height)
	
	#build a line alien
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			##build a alien & join in
			#alien = Alien(ai_settings,screen)
			#alien.x = alien_width + 2 * alien_width * alien_number
			#alien.rect.x = alien.x
			#aliens.add(alien)
			create_alien(ai_settings,screen,aliens,alien_number,
				row_number)
	
def get_numner_aliens_x(ai_settings,alien_width):
	#number hold how many alien in a lien
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	
	return number_aliens_x
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	#build aliens
	#build a alien & number how many a line
	#spacing alien
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)	
	
def get_number_rows(ai_settings,ship_height,alien_height):
	#number can hold how aliens
	available_space_y = (ai_settings.screen_height - 
								(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def check_fleet_edges(ai_settings,aliens):
	#when alien touch edge
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	#g_down aliens & change direction
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
					
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#update aliens loc 
	#if check alien loc screen edge & update alien loc
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship,aliens):
		#print("ship hit!!!")
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	if stats.ships_left > 0:
		#answer alien attack ship
		#ship_left -1
		stats.ships_left -= 1
		
		sb.prep_ships()
		
		#clear aliens list & bullets list
		aliens.empty()
		bullets.empty()
		
		#create new aliens & put ship in center-bottom
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
		#sleep
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#check if alien go to bottom
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#as like ship attack
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			break 

def check_high_score(stats,sb):
	#check high-score
	if stats.score >stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
	
	
