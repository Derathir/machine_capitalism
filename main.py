import pygame
import random

#handler class for all game sprites:
class Sprite:
    def __init__(self, image:str, speed:float=1, x:int=0, y:int=0, angle:float=0):
        self.sprite = self.image_loader(image)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.speed = speed
        self.x = x
        self.y = y
        self.angle = angle
    #just covering some inconsistencies with file placement in the exercises:
    def image_loader(self, image):
        try:
            return pygame.image.load(image)
        except FileNotFoundError:
            return pygame.image.load("src/" + image)

#main game class:        
class MachineCapitalism:
    def __init__(self, width, height):
        pygame.init()
        self.sprites = []
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Machine Capitalism")
        self.background = (128, 128, 128)
        self.clock = pygame.time.Clock()
        self.round = 0
        self.loop()
    #reset and create sprites for the round:
    def populate(self):
        #new color each round, for fun:
        self.background = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.sprites = []
        #index 0 is coin:
        self.sprites.append(Sprite("coin.png", 0))
        #index 1 is player character:
        self.sprites.append(Sprite("monster.png", 0))
        #randomize starting position:
        self.sprites[1].x = random.randint(0, self.width - self.sprites[1].width)
        self.sprites[1].y = random.randint(0, self.height - self.sprites[1].height)
        self.stick()
        #add enemies equal to round number:
        for i in range(self.round):
            new_sprite = Sprite("robot.png", 1)
            while True:
                #random position:
                new_sprite.x = random.randint(0, self.width - new_sprite.width)
                new_sprite.y = random.randint(0, self.height - new_sprite.height)
                #check if away from starting position, try again if not:
                if self.apart(self.sprites[1], new_sprite):
                    break
            self.sprites.append(new_sprite)
    def loop(self):
        while True:
            if len(self.sprites) < 3:
                self.new_round()
            self.controls()
            self.move()
            self.draw()
            self.clock.tick(60)
    def controls(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.sprites[1].speed = 2
                    if event.button == 3 and self.sprites[0].speed == 0:
                        self.throw()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.sprites[1].speed = 0
    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        for sprite in self.sprites:
            pos = (sprite.x, sprite.y)
            delta = pygame.math.Vector2.from_polar((sprite.speed, sprite.angle))
            if self.sprites.index(sprite) == 1:
                #player aims at mouse location:
                sprite.angle += delta.angle_to(pygame.math.Vector2(mouse_pos[0] - sprite.x, mouse_pos[1] - sprite.y))
            if self.sprites.index(sprite) > 1:
                #robots aim at player:
                sprite.angle += delta.angle_to(pygame.math.Vector2(self.sprites[1].x - sprite.x, self.sprites[1].y - sprite.y))
                #coin kills robots:
                if not self.apart(self.sprites[0], sprite):
                    self.sprites.remove(sprite)
                #robots kill player:
                if not self.apart(self.sprites[1], sprite):
                    self.game_over()
            pos += delta
            sprite.x = pygame.math.clamp(pos[0], 0, self.width - sprite.width)
            sprite.y = pygame.math.clamp(pos[1], 0, self.height - sprite.height)
        #coin sticks to player if not thrown:
        if not self.apart(self.sprites[0], self.sprites[1]) and self.sprites[0].speed == 0:
            self.stick()
        #coin stops at screen edges:
        if self.sprites[0].speed != 0 and (not 0 < self.sprites[0].x < self.width - self.sprites[0].width or not 0 < self.sprites[0].y < self.height - self.sprites[0].height):
            self.sprites[0].speed = 0
    #check sprite collision:
    def apart(self, sprite_a, sprite_b):
        return sprite_a.x + sprite_a.width < sprite_b.x or sprite_a.x > sprite_b.x + sprite_b.width or sprite_a.y + sprite_a.height < sprite_b.y or sprite_a.y > sprite_b.y + sprite_b.height
    def throw(self):
        mouse_pos = pygame.mouse.get_pos()
        sprite = self.sprites[0]
        sprite.speed = 4
        sprite.angle += pygame.math.Vector2.from_polar((sprite.speed, sprite.angle)).angle_to(pygame.math.Vector2(mouse_pos[0] - sprite.x, mouse_pos[1] - sprite.y))
    #move coin to player:
    def stick(self):
        self.sprites[0].x = self.sprites[1].x
        self.sprites[0].y = self.sprites[1].y
    def draw(self):
        self.window.fill(self.background)
        self.window.blit(pygame.font.SysFont("Arial", 32).render("L-click to move", True, (255, 255, 255)), (8, 8))
        self.window.blit(pygame.font.SysFont("Arial", 32).render("R-click to pay", True, (255, 255, 255)), (8, 40))
        for sprite in self.sprites:
            self.window.blit(sprite.sprite, (sprite.x, sprite.y))
        pygame.display.flip()
    def new_round(self):
        self.round += 1
        self.populate()
        self.window.fill(self.background)
        self.window.blit(pygame.font.SysFont("Arial", 64).render(f"Round {self.round}", True, (255, 255, 255)), (8, 8))
        pygame.display.flip()
        pygame.time.wait(1200)
        self.draw()
        #small delay to give player time to react:
        pygame.time.wait(200)
    def game_over(self):
        self.window.fill((0, 0, 0))
        self.window.blit(pygame.font.SysFont("Arial", 32).render(f"Round {self.round}", True, (255, 255, 255)), (8, 8))
        self.window.blit(pygame.font.SysFont("Arial", 64).render(f"GAME OVER", True, (255, 0, 0)), (128, 128))
        pygame.display.flip()
        pygame.time.wait(1800)
        exit()

#go!
MachineCapitalism(640, 480)