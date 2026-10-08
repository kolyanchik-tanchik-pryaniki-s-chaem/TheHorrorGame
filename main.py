import pygame as pg
import pytmx
import random
TILE_SCALE = 2
FPS = 60
class Notes(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
    def update(self, velocity_x, velocity_y):
        self.rect.y -= velocity_y
        self.rect.x -= velocity_x
class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (width * TILE_SCALE, height* TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
    def update(self,  velocity_x, velocity_y):

        self.rect.y -= velocity_y
        self.rect.x -= velocity_x
class Wall(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
    def update(self,  velocity_x, velocity_y):

        self.rect.y -= velocity_y
        self.rect.x -= velocity_x
class Enemy(pg.sprite.Sprite):
    def __init__(self, player, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load("64x64_faces/64x64_faces_011.png"), (100,50))
        self.rect = self.image.get_rect()
        self.is_following = True
        self.rect.center = (550, 300)
        self.velocity_x = 0
        self.velocity_y = 0
        self.left = -4
        self.right = 4
        self.bottom = 4
        self.top = -4
        self.player = player
        self.game = game
    def update(self):
        platform1 = None
        platform2 = None
        platform3 = None
        platform4 = None
        for wall in self.game.walls:

            if wall.rect.collidepoint(self.rect.midleft):
                platform1 = wall
                self.rect.left = wall.rect.right - 1
                self.left = 0
            if platform1 == None:
                self.left = -4
            if wall.rect.collidepoint(self.rect.midright):
                platform2 = wall
                self.rect.right = wall.rect.left
                self.right = 0
            if platform2 == None:
                self.right = 4
            if wall.rect.collidepoint(self.rect.midtop):
                platform3 = wall
                self.rect.top = wall.rect.bottom - 1
                self.top = 0
            if platform3 == None:
                self.top = -4
            if wall.rect.collidepoint(self.rect.midbottom):
                platform4 = wall
                self.rect.bottom = wall.rect.top
                self.bottom = 0
            if platform4 == None:
                self.bottom = 4
        if self.is_following:
         if self.player.rect.x > self.rect.x:
            self.velocity_x = self.right

         elif self.player.rect.x < self.rect.x:
            self.velocity_x = self.left

         else:
            self.velocity_x = 0
         if self.player.rect.y > self.rect.y:
            self.velocity_y = self.bottom

         elif self.player.rect.y < self.rect.y:
            self.velocity_y = self.top

         else:
            self.velocity_y = 0
        self.rect.x += self.velocity_x
        self.rect.x -= self.player.velocity_x
        self.rect.y += self.velocity_y
        self.rect.y -= self.player.velocity_y
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load("64x64_faces/64x64_faces_002.png"), (100,50))
        self.rect = self.image.get_rect()
        self.rect.center = (450, 300)
        self.game = game

        self.velocity_x = 0
        self.velocity_y = 0
        self.left = -6
        self.right = 6
        self.top = -6
        self.bottom = 6
    def update(self, keys):
        platform1 = None
        platform2 = None
        platform3 = None
        platform4 = None
        for wall in self.game.walls:

            if wall.rect.collidepoint(self.rect.midleft):
                platform1 = wall
                self.rect.left = wall.rect.right - 1
                self.left = 0
            if platform1 == None:
                self.left = -6
            if wall.rect.collidepoint(self.rect.midright):
                platform2 = wall
                self.rect.right = wall.rect.left
                self.right = 0
            if platform2 == None:
                self.right = 6
            if wall.rect.collidepoint(self.rect.midtop):
                platform3 = wall
                self.rect.top = wall.rect.bottom - 1
                self.top = 0
            if platform3 == None:
                self.top = -6
            if wall.rect.collidepoint(self.rect.midbottom):
                platform4 = wall
                self.rect.bottom = wall.rect.top
                self.bottom = 0
            if platform4 == None:
                self.bottom = 6
        if keys[pg.K_a]:
            self.velocity_x = self.left
        elif keys[pg.K_d]:
            self.velocity_x = self.right
        else:
            self.velocity_x = 0
        if keys[pg.K_s]:
            self.velocity_y = self.bottom
        elif keys[pg.K_w]:
            self.velocity_y = self.top
        else:
            self.velocity_y = 0
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        pg.display.set_caption("The horror game")
        self.is_running = False
        self.tmx_map = pytmx.load_pygame("horror1.tmx")
        self.walls = pg.sprite.Group()
        self.player = Player(self)

        self.enemy_event = pg.USEREVENT + 1
        self.enemy_event1 = pg.event.Event(self.enemy_event)
        self.enemy = Enemy(self.player, self)
        self.background_platform = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        for layer in self.tmx_map:
            for x, y, gid in layer:
               tile = self.tmx_map.get_tile_image_by_gid(gid)
               if tile and layer.name == 'main':
                   platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight, self.tmx_map.tilewidth, self.tmx_map.tileheight)
                   self.background_platform.add(platform)
                   self.all_sprites.add(platform)

               if tile and layer.name == 'walls':
                   wall = Wall(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight, self.tmx_map.tilewidth, self.tmx_map.tileheight)
                   self.walls.add(wall)
                   self.all_sprites.add(wall)
               if tile and layer.name == 'notes':
        pg.time.set_timer(self.enemy_event1, 2000)
        self.temp_x = self.enemy.rect.x
        self.temp_y = self.enemy.rect.y
        self.run()
    def run(self):
       self.is_running = True
       while self.is_running:
            self.draw()
            self.event()
            self.update()

            self.clock.tick(FPS)
    def update(self):
        self.background_platform.update(self.player.velocity_x, self.player.velocity_y)
        self.walls.update(self.player.velocity_x, self.player.velocity_y)
        self.player.update(pg.key.get_pressed())
        self.enemy.update()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == self.enemy_event:
                if self.temp_x - self.enemy.rect.x < 6 or self.enemy.rect.x + self.temp_x < 6 and self.enemy.top == 0 or self.enemy.bottom == 0 and self.enemy.is_following:

                    self.enemy.is_following = False
                    # if self.enemy.velocity_x == self.enemy.right:
                    #     self.enemy.velocity_x = self.enemy.left
                    # if self.enemy.velocity_x == self.enemy.left:
                    #     self.enemy.velocity_x = self.enemy.right
                    self.enemy.velocity_x = random.choice((self.enemy.left, self.enemy.right))
                if self.enemy.right == 0 or self.enemy.left == 0 and self.enemy.top == 0 or self.enemy.bottom == 0:
                    self.enemy.is_following = True
                if self.temp_y - self.enemy.rect.y < 6 or self.enemy.rect.y + self.temp_y < 6 and self.enemy.left == 0 or self.enemy.right == 0 and self.enemy.is_following:
                    self.enemy.is_following = False

                    # if self.enemy.velocity_y == self.enemy.top:
                    #     self.enemy.velocity_y = self.enemy.bottom
                    # if self.enemy.velocity_y == self.enemy.bottom:
                    #     self.enemy.velocity_y = self.enemy.top
                    self.enemy.velocity_y = random.choice((self.enemy.top, self.enemy.bottom))
                if self.enemy.top == 0 and self.enemy.bottom == 0:
                    self.enemy.is_following = True
                if self.temp_x - self.enemy.rect.x < 6 or self.enemy.rect.x + self.temp_x < 6 and self.temp_y - self.enemy.rect.y < 6 or self.enemy.rect.y + self.temp_y < 6:
                    self.enemy.is_following = True
                self.temp_y = self.enemy.rect.y
                self.temp_x = self.enemy.rect.x
    def draw(self):
        self.screen.blit(pg.transform.scale(pg.image.load("Снимок экрана 2026-10-04 105440.png"), (800, 600)), (0, 0))
        for wall in self.walls:
            self.screen.blit(wall.image, wall.rect)
        for platform in self.background_platform:
            self.screen.blit(platform.image, platform.rect)
        self.player.draw(self.screen)
        self.screen.blit(self.enemy.image, self.enemy.rect)
        pg.display.flip()
if __name__ == '__main__':
    game = Game()

