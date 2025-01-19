import pygame
import random

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("audio/space.ogg")
pygame.mixer.music.play()
fire_sound = pygame.mixer.Sound("audio/fire.ogg")

pygame.font.init()

font = pygame.font.Font("font/PressStart2P.ttf", 40)
end_game_font = pygame.font.Font("font/PressStart2P.ttf", 64)

you_win_text = end_game_font.render("You win!", True, "white")
you_lose_text = end_game_font.render("You lose!", True, "white")

goal = 10
score = 0
lost = 0

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, w=64, h=64, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), (w, h))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < WIDTH - self.width:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(
            "img/bullet.png", self.rect.centerx, self.rect.top, 16, 32, 5
        )
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed

        if self.rect.y > 600:
            self.rect.x = random.randint(64, HEIGHT - 64)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


WIDTH = 800
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")

background = pygame.transform.scale(
    pygame.image.load("img/background.jpg"), (WIDTH, HEIGHT)
)

ship = Player("img/ship.png", 400, 500, 64, 64, 5)

monsters = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(1, 5):
    monster = Enemy(
        "img/ufo.png", random.randint(1, WIDTH), -64, 64, 64, random.randint(1, 5)
    )
    monsters.add(monster)

game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                ship.fire()

    if not game_over:
        window.blit(background, (0, 0))

        score_text = font.render("Score: " + str(score), True, "white")
        lost_text = font.render("Lost: " + str(lost), True, "white")

        window.blit(score_text, (10, 10))
        window.blit(lost_text, (10, 50))

        ship.move()
        monsters.update()

        ship.draw()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        collides = pygame.sprite.groupcollide(monsters, bullets, True, True) 
        for c in collides:
            score += 1 
            monster = Enemy(
                "img/ufo.png", 
                random.randint(1, WIDTH), -64, 64, 64, random.randint(1, 5)
            )
            monsters.add(monster)

        if pygame.sprite.spritecollide(ship, monsters, False) or lost >= 3:
            game_over = True
            window.blit(you_lose_text, (200, 200))

        if score >= goal:
            game_over = True
            window.blit(you_win_text, (200, 200))

        pygame.display.update()
        pygame.time.Clock().tick(60)

pygame.quit()