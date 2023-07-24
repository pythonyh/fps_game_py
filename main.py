import pygame
import sys
import math

args = sys.argv
sprites_path = "C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\"


class General:
    def __init__(self):
        self.resolution = (1280, 720)
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta = self.clock.tick(60) / 1000
        self.shoot_inst = False
        pygame.display.set_caption("Fps Game")

    def first_load(self):
        mainloop.scenario.add_mainscene()
        self.main_build()
        mainloop.hero.add()

    @staticmethod
    def main_build():
        mainloop.interface.add_life()
        mainloop.interface.add_crosshair()


class Scenario:
    def __init__(self):
        self.mainscene = \
            pygame.image.load("C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\Maps\\Wide-Wasteland.jpg")

    def add_mainscene(self):
        print("added")
        general.screen.blit(self.mainscene, pygame.Vector2((40, 30)))
        self.mainscene = pygame.transform.scale(self.mainscene, (10, 10))


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.Vector2(general.screen.get_width()/2, general.screen.get_height()/2)
        self.speed = 1
        self.life = 100
        self.stamina = 100
        self.balas = 10
        self.sprites = []
        self.sprites_walk = []
        self.image = 0
        self.running = True
        self.image_walk = 0
        self.walking = False
        self.flipped = False

    def add(self):
        for num in range(21):
            self.sprites.append(pygame.image.load(f"{sprites_path}Player\\Idle\\Character_idle{num+1}.png"))
            self.sprites[num] = pygame.transform.scale(self.sprites[num], (40, 60))
        for num in range(8):
            self.sprites_walk.append(pygame.image.load(f"{sprites_path}Player\\Walk\\Character_run{num + 1}.png"))
            self.sprites_walk[num] = pygame.transform.scale(self.sprites_walk[num], (40, 60))

    def anim(self, animation):
        if animation == "idle":
            general.screen.blit(self.sprites[self.image], self.pos)
            self.image += 1
            if self.image >= 21:
                self.image = 0
        elif animation == "walk":
            general.screen.blit(self.sprites_walk[self.image_walk], self.pos)
            self.image_walk += 1
            if self.image_walk >= 8:
                self.image_walk = 0

    def buttons(self):
        keys = pygame.key.get_pressed()
        if self.walking:
            self.anim("walk")
        else:
            self.anim("idle")
        if keys[pygame.K_w]:
            self.walking = True
            self.pos.y -= self.speed * general.delta
        elif keys[pygame.K_s]:
            self.walking = True
            self.pos.y += self.speed * general.delta
        else:
            self.walking = False
        if keys[pygame.K_a]:
            self.walking = True
            self.pos.x -= self.speed * general.delta
        elif keys[pygame.K_d]:
            self.walking = True
            self.pos.x += self.speed * general.delta
        if keys[pygame.K_LSHIFT]:
            if self.stamina > 0:
                self.running = True
                self.speed = 100 * 40 * general.delta
                self.stamina -= 35 * general.delta
            else:
                self.running = False
                self.speed = 100
        else:
            self.speed = 100

    def flip(self):
        if tuple(self.pos) > pygame.mouse.get_pos():
            if not self.flipped:
                for num in range(21):
                    self.sprites[num] = pygame.transform.flip(self.sprites[num], True, False)
                for num in range(8):
                    self.sprites_walk[num] = pygame.transform.flip(self.sprites_walk[num], True, False)
                self.flipped = True
        else:
            if self.flipped:
                for num in range(21):
                    self.sprites[num] = pygame.transform.flip(self.sprites[num], True, False)
                for num in range(8):
                    self.sprites_walk[num] = pygame.transform.flip(self.sprites_walk[num], True, False)
                self.flipped = False

    def shoot(self):
        if pygame.mouse.get_pressed()[0]:
            general.shoot_inst = True


class Gun:
    def __init__(self):
        self.num = 0
        self.shoot_sprites = []        
        pygame.image.load("C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\Player\\Gun\\0.png")
        for num in range(3):
            self.shoot_sprites.append\
                (pygame.image.load(f"C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\Shoot\\Shoot{num+1}.png"))
        for sprite in self.shoot_sprites:
            pygame.transform.scale(sprite, (20, 20))
    
    def __call__(self, *args, **kwargs):
        self.bala_pos = mainloop.hero.pos

    def shoot_inst(self):
        ca = int(mainloop.hero.pos.x) - int(pygame.mouse.get_pos()[0])
        co = int(mainloop.hero.pos.y) - int(pygame.mouse.get_pos()[1])
        if co == 0 or ca == 0:
            co += 1
            ca += 1
        hip = math.hypot(ca, co)
        sin_angle = co / hip
        angle = sin_angle * 180/math.pi
        print(angle)
        gun_rotated = pygame.transform.rotate(self.shoot_sprites[self.num], angle)
        general.screen.blit(gun_rotated, pygame.Vector2(self.bala_pos))
        self.num += 1
        if self.num >= 2:
            self.num = 0
        self.bala_pos.x += 50 * general.delta


class Interface:
    def __init__(self):
        self.crosshair = pygame.image.load("C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\UI\\crosshair.png")
        self.life_bar = pygame.image.load("C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\UI\\GreenBar.png")
        self.heart = pygame.image.load("C:\\Users\\marce\\PycharmProjects\\fpsgame\\Sprites\\UI\\heart.png")

    def add_crosshair(self):
        general.screen.blit(self.crosshair, pygame.Vector2(pygame.mouse.get_pos()))
        self.crosshair = pygame.transform.scale(self.crosshair, (30, 25))

    def add_life(self):
        general.screen.blit(self.life_bar, pygame.Vector2((50, 80)))
        general.screen.blit(self.heart, pygame.Vector2((50, 100)))
        self.heart = pygame.transform.scale(self.heart, (30, 30))
        self.life_bar = pygame.transform.scale(self.life_bar, (25, 250))


class MainLoop:
    def __init__(self):
        pygame.display.init()
        #pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)
        self.scenario = Scenario()
        self.interface = Interface()
        self.hero = Hero()
        self.gun = Gun()
        self.time = 0

    def run(self):
        general.first_load()
        self.gun.__call__(None)
        while general.running:
            self.hero.shoot()
            general.main_build()
            self.time += 20 * general.delta
            if self.time >= 100:
                if not self.hero.running:
                    self.hero.stamina += 20 * general.delta
                if self.hero.stamina >= 100:
                    self.time = 0
            for cmd in pygame.event.get():
                if cmd == pygame.QUIT:
                    general.running = False
            if self.hero.stamina <= 0:
                self.hero.stamina = 0
            elif self.hero.stamina >= 100:
                self.hero.stamina = 100
            self.hero.buttons()
            if general.shoot_inst:
                self.gun.shoot_inst()
            general.delta = general.clock.tick(20) / 1000
            pygame.display.flip()
            general.screen.fill("purple")
            self.hero.flip()
        pygame.quit()


if __name__ == "__main__":
    general = General()
    mainloop = MainLoop()
    mainloop.run()
