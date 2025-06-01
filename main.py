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
        if keys[K_SPACE] and self.opora:
            self.rect.y += -150

    def gravity(self):
        self.opora = False
        sprite_list = sprite.spritecollide(player, platforms, False)
        if len(sprite_list)!=0:
            self.opora = True
        if not self.opora:
            self.rect.y += 1

class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h, speed, fly=0):
        super().__init__(img, x, y, w, h, speed)
        self.fly = fly
    def start(self, z1, z2):
        self.z1 = z1
        self.z2 = z2
    def update(self):
        if self.fly == 1:
            if self.rect.y <= min(self.z1, self.z2):
                self.direct = 1
            elif self.rect.y >= max(self.z1, self.z2):
                self.direct = -1
            self.rect.y += self.speed*self.direct
        else:
            if self.rect.x <= min(self.z1, self.z2):
                self.direct = 1
            elif self.rect.x >= max(self.z1, self.z2):
                self.direct = -1
            self.rect.x += self.speed*self.direct



window = display.set_mode((700,400))
display.set_caption('Платформер')
background = transform.scale(image.load('fon.png'), (700,400))
player = Player('player.png', 10, 0, 50, 70, 5)

enemyes = sprite.Group()
enemy1 = Enemy('enemy.png', 200, 200, 50, 50, 1)
enemy1.start(200,300)
enemyes.add(enemy1)
enemy2 = Enemy('enemy.png', 400, 200, 50, 50, 1, 1)
enemy2.start(200,300)
enemyes.add(enemy2)

font.init()
font1 = font.SysFont('Arial', 36)


coins = sprite.Group()
for i in range(2000):
    x = randint(5, 695)
    y= randint(200, 300)
    coin = GameSprite('coin.png', x, y, 30, 35, 0)
    coins.add(coin)



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
c_count = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0,0))
    platforms.draw(window)
    player.reset()
    player.update()
    player.gravity()

    enemyes.update()
    enemyes.draw(window)

    coins.update()
    coins.draw(window)

    coin_count = font1.render('Coins:'+str(c_count), 1, (0,0,0))
    window.blit(coin_count, (10,10))

    spriteList = sprite.spritecollide(player, coins, True)
    for i in spriteList:
        c_count += 1


    clock.tick(fps)
    display.update()