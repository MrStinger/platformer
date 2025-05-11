from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Platform(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)   

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)   
        self.opora = False   



    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>10:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<700 -10- self.rect.width:
            self.rect.x+=self.speed 

    def gravity(self):
        self.opora = False
        sprite_list = sprite.spritecollide(player, platforms, False)
        if len(sprite_list)!=0:
            self.opora = True
        if not self.opora:
            self.rect.y += 1



window = display.set_mode((700,400))
display.set_caption('Платформер')
background = transform.scale(image.load('fon.png'), (700,400))
player = Player('player.png', 10, 0, 50, 70, 5)

platforms = sprite.Group()
pl_count = 5
for i in range(pl_count):
    x = randint(5, 700-105)
    y= randint(100, 400-55)
    plt = Platform('platform.png', x, y, 130, 60, 0)
    platforms.add(plt)
plt = Platform('platform.png', -100, 307, 900, 140, 0)
platforms.add(plt)


game = True
clock = time.Clock()
fps = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0,0))
    platforms.draw(window)
    player.reset()
    player.update()
    player.gravity()


    clock.tick(fps)
    display.update()