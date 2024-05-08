import pygame 

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		direction = player.status.split('_')[0]

		# graphic
		full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
		self.image = pygame.image.load(full_path).convert_alpha()
		
		# placement
		if direction == 'right':
			self.rect = self.image.get_rect(midleft=player.hitbox.midright + pygame.math.Vector2(0, 16))
		elif direction == 'left':
			self.rect = self.image.get_rect(midright=player.hitbox.midleft + pygame.math.Vector2(0, 16))
		elif direction == 'down':
			# Adjust the y-coordinate to bring the weapon closer to the character for the down direction
			self.rect = self.image.get_rect(midtop=player.hitbox.midbottom + pygame.math.Vector2(-10, -20))
		else:
			# Adjust the y-coordinate to bring the weapon closer to the character for the up direction
			self.rect = self.image.get_rect(midbottom=player.hitbox.midtop + pygame.math.Vector2(-10, -20))

	def update(self):
		pass

	def draw_debug_rect(self, surface):
		pygame.draw.rect(surface, self.debug_rect_color, self.rect, 1)