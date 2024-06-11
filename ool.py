import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ool")

# Sets all the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ERIERIERIC_COLOR = (100, 215, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)

# Middle border in between
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('final_project/Assets/ow.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('final_project/Assets/bap.mp3')
SONG = pygame.mixer.Sound('final_project/Assets/burrito_sabanero.mp3')

HEALTH_FONT = pygame.font.SysFont('georgia', 40)
WINNER_FONT = pygame.font.SysFont('georgia', 100)

FPS = 60
VEL = 12
BULLET_VEL = 7
BIG_BULLET_VEL = BULLET_VEL * 2
MAX_BULLETS = 5
CHARACTER_WIDTH = 60
CHARACTER_HEIGHT = 45
BIG_BULLET_SIZE = (20, 10)
BULLET_DAMAGE = 1
BIG_BULLET_DAMAGE = BULLET_DAMAGE * 2

ERIERIERIC_HIT = pygame.USEREVENT + 1
CAIDNE_HIT = pygame.USEREVENT + 2
POWER_UP_SPAWN = pygame.USEREVENT + 3

POWER_UP_DURATION = 5000  # 5 seconds
POWER_UP_SIZE = 20

# Loads images
ERIERIERIC_IMAGE = pygame.image.load(
    os.path.join('final_project/Assets', 'erierieric.png'))
ERIERIERIC = pygame.transform.rotate(pygame.transform.scale(
    ERIERIERIC_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 0)

CAIDNE_IMAGE = pygame.image.load(
    os.path.join('final_project/Assets', 'caidne.png'))
CAIDNE = pygame.transform.rotate(pygame.transform.scale(
    CAIDNE_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 0)

FLOOR = pygame.transform.scale(pygame.image.load(
    os.path.join('final_project/Assets', 'flor.png')), (WIDTH, HEIGHT))


class Bullet:
    def __init__(self, x, y, width, height, color, vel, damage):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.vel = vel
        self.damage = damage

    def move(self):
        self.rect.x += self.vel

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


class PowerUp:
    def __init__(self, x, y, effect):
        self.rect = pygame.Rect(x, y, POWER_UP_SIZE, POWER_UP_SIZE)
        self.effect = effect
        self.color = self.get_color(effect)

    def get_color(self, effect):
        if effect == 'speed':
            return BLUE
        elif effect == 'size':
            return GREEN
        elif effect == 'bullet_speed':
            return PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


# Creates window of all the things pygame keeps track of, blitting stuff around
def draw_window(caidne, erierieric, caidne_bullets, erierieric_bullets, caidne_health, erierieric_health, power_ups):
    WIN.blit(FLOOR, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    caidne_health_text = HEALTH_FONT.render(
        "Health: " + str(caidne_health), 1, WHITE)
    erierieric_health_text = HEALTH_FONT.render(
        "Health: " + str(erierieric_health), 1, WHITE)
    WIN.blit(caidne_health_text, (WIDTH - caidne_health_text.get_width() - 10, 10))
    WIN.blit(erierieric_health_text, (10, 10))

    WIN.blit(ERIERIERIC, (erierieric.x, erierieric.y))
    WIN.blit(CAIDNE, (caidne.x, caidne.y))

    for bullet in caidne_bullets:
        bullet.draw(WIN)

    for bullet in erierieric_bullets:   
        bullet.draw(WIN)

    for power_up in power_ups:
        power_up.draw(WIN)

    pygame.display.update()


# Handles Eric's movement
def erierieric_handle_movement(keys_pressed, erierieric, vel):
    if keys_pressed[pygame.K_a] and erierieric.x - vel > 0:  # LEFT
        erierieric.x -= vel
    if keys_pressed[pygame.K_d] and erierieric.x + vel + erierieric.width < BORDER.x:  # RIGHT
        erierieric.x += vel
    if keys_pressed[pygame.K_w] and erierieric.y - vel > 0:  # UP
        erierieric.y -= vel
    if keys_pressed[pygame.K_s] and erierieric.y + vel + erierieric.height < HEIGHT - 15:  # DOWN
        erierieric.y += vel


# Handles Caiden's movement
def caidne_handle_movement(keys_pressed, caidne, vel):
    if keys_pressed[pygame.K_LEFT] and caidne.x - vel > BORDER.x + BORDER.width:  # LEFT
        caidne.x -= vel
    if keys_pressed[pygame.K_RIGHT] and caidne.x + vel + caidne.width < WIDTH:  # RIGHT
        caidne.x += vel
    if keys_pressed[pygame.K_UP] and caidne.y - vel > 0:  # UP
        caidne.y -= vel
    if keys_pressed[pygame.K_DOWN] and caidne.y + vel + caidne.height < HEIGHT - 15:  # DOWN
        caidne.y += vel


# Handles shooting bullets and magazine
def handle_bullets(erierieric_bullets, caidne_bullets, erierieric, caidne):
    for bullet in erierieric_bullets:
        bullet.move()
        if caidne.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(CAIDNE_HIT, {'damage': bullet.damage}))
            erierieric_bullets.remove(bullet)
        elif bullet.rect.x > WIDTH:
            erierieric_bullets.remove(bullet)

    for bullet in caidne_bullets:
        bullet.move()
        if erierieric.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(ERIERIERIC_HIT, {'damage': bullet.damage}))
            caidne_bullets.remove(bullet)
        elif bullet.rect.x < 0:
            caidne_bullets.remove(bullet)


# Draws winner text
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def apply_power_up(effect, character_rect, character_vel, original_vel, bullet_vel):
    if effect == 'speed':
        return character_vel * 2, bullet_vel  # Double the speed
    elif effect == 'size':
        character_rect.inflate_ip(20, 20)  # Increase size
        return character_vel, bullet_vel
    elif effect == 'bullet_speed':
        return character_vel, bullet_vel * 2  # Double the bullet speed
    return character_vel, bullet_vel


def main():
    caidne = pygame.Rect(700, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    erierieric = pygame.Rect(100, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    caidne_bullets = []
    erierieric_bullets = []

    caidne_health = 10
    erierieric_health = 10

    clock = pygame.time.Clock()

    pygame.mixer.Channel(1).play(SONG)

    power_ups = []

    pygame.time.set_timer(POWER_UP_SPAWN, 10000)  # Spawn a power-up every 10 seconds

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == POWER_UP_SPAWN:
                x = random.randint(0, WIDTH - POWER_UP_SIZE)
                y = random.randint(0, HEIGHT - POWER_UP_SIZE)
                effect = random.choice(['speed', 'size', 'bullet_speed'])
                power_up = PowerUp(x, y, effect)
                power_ups.append(power_up)

            if event.type == pygame.KEYDOWN:
                # Normal shot Eric
                if event.key == pygame.K_SPACE and len(erierieric_bullets) < MAX_BULLETS:
                    bullet = Bullet(erierieric.x + erierieric.width, erierieric.y + erierieric.height//2 - 2, 10, 5, ERIERIERIC_COLOR, BULLET_VEL, BULLET_DAMAGE)
                    erierieric_bullets.append(bullet)
                    pygame.mixer.Channel(0).play(BULLET_FIRE_SOUND)
                # Big shot Eric
                if event.key == pygame.K_e and len(erierieric_bullets) == 0:
                    big_bullet = Bullet(erierieric.x + erierieric.width, erierieric.y + erierieric.height//2 - BIG_BULLET_SIZE[1]//2, *BIG_BULLET_SIZE, ERIERIERIC_COLOR, BIG_BULLET_VEL, BIG_BULLET_DAMAGE)
                    erierieric_bullets.append(big_bullet)
                    pygame.mixer.Channel(0).play(BULLET_FIRE_SOUND)
                # Normal shot Caiden
                if event.key == pygame.K_p and len(caidne_bullets) < MAX_BULLETS:
                    bullet = Bullet(caidne.x, caidne.y + caidne.height//2 - 2, 10, 5, RED, -BULLET_VEL, BULLET_DAMAGE)
                    caidne_bullets.append(bullet)
                    pygame.mixer.Channel(0).play(BULLET_FIRE_SOUND)
                # Big shot Caiden
                if event.key == pygame.K_o and len(caidne_bullets) == 0:
                    big_bullet = Bullet(caidne.x, caidne.y + caidne.height//2 - BIG_BULLET_SIZE[1]//2, *BIG_BULLET_SIZE, RED, -BIG_BULLET_VEL, BIG_BULLET_DAMAGE)
                    caidne_bullets.append(big_bullet)
                    pygame.mixer.Channel(0).play(BULLET_FIRE_SOUND)

            if event.type == CAIDNE_HIT:
                caidne_health -= event.dict['damage']
                pygame.mixer.Channel(0).play(BULLET_HIT_SOUND)

            if event.type == ERIERIERIC_HIT:
                erierieric_health -= event.dict['damage']
                pygame.mixer.Channel(0).play(BULLET_HIT_SOUND)

        winner_text = ""
        if caidne_health <= 0:
            winner_text = "ERIERIERIC Wins!"

        if erierieric_health <= 0:
            winner_text = "CAIDNE Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        # Default velocities
        erierieric_vel = VEL
        caidne_vel = VEL
        bullet_vel = BULLET_VEL

        # Handle power-up effects
        for power_up in power_ups:
            if erierieric.colliderect(power_up.rect):
                erierieric_vel, bullet_vel = apply_power_up(power_up.effect, erierieric, erierieric_vel, VEL, bullet_vel)
                power_ups.remove(power_up)
                pygame.time.set_timer(pygame.USEREVENT + 4, POWER_UP_DURATION)

            if caidne.colliderect(power_up.rect):
                caidne_vel, bullet_vel = apply_power_up(power_up.effect, caidne, caidne_vel, VEL, bullet_vel)
                power_ups.remove(power_up)
                pygame.time.set_timer(pygame.USEREVENT + 5, POWER_UP_DURATION)

        erierieric_handle_movement(keys_pressed, erierieric, erierieric_vel)
        caidne_handle_movement(keys_pressed, caidne, caidne_vel)

        handle_bullets(erierieric_bullets, caidne_bullets, erierieric, caidne)

        draw_window(caidne, erierieric, caidne_bullets, erierieric_bullets,
                    caidne_health, erierieric_health, power_ups)

        # Reset power-up effects after duration
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 4:  # Eric's power-up effect ends
                erierieric_vel = VEL
                bullet_vel = BULLET_VEL
                erierieric = pygame.Rect(erierieric.x, erierieric.y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

            if event.type == pygame.USEREVENT + 5:  # Caidne's power-up effect ends
                caidne_vel = VEL
                bullet_vel = BULLET_VEL
                caidne = pygame.Rect(caidne.x, caidne.y, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    main()


if __name__ == "__main__":
    main()