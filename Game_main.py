# 初めてのゲーム開発
import pygame
from pygame import mixer
import random
import math

pygame.init()

# 画面とゲームタイトル
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Invaders Game')

# プレイヤー
playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

# プレイヤー関数
def player(x, y):
    screen.blit(playerImg, (x, y))

# スコア
score_value = 0

# エネミー
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# 攻撃レーザー
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
bullet_state = 'ready'

# 攻撃レーザー音
laser_sound = pygame.mixer.Sound('laser.wav')
laser_sound.set_volume(0.2)  # 音量の設定

# 背景音楽
pygame.mixer.music.load('background.wav')
pygame.mixer.music.set_volume(0.5)  # 音量の設定
pygame.mixer.music.play(-1)  # -1はループ再生を意味する

# ゲームの制限時間（ミリ秒）
time_limit = 30000  # 30秒

# ゲームの開始時間
start_time = 0

# ゲームステータス
game_started = False
game_over = False

# エネミー関数
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# 攻撃レーザー関数
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))
    laser_sound.play()

# 衝突判定関数
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
      return True
    else:
      return False

# ゲーム開始
while not game_started:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
                start_time = pygame.time.get_ticks()

    screen.fill((0, 0, 0))

    font = pygame.font.SysFont(None, 64)
    title_text = font.render("Invaders Game", True, (255, 255, 255))
    screen.blit(title_text, (200, 250))
    
    press_enter_text = font.render("Press Enter key", True, (255, 255, 255))
    screen.blit(press_enter_text, (200, 350))

    pygame.display.update()

while not game_over:
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    if elapsed_time >= time_limit:
        game_over = True  # 制限時間に達したら、ゲーム終了

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # 得点表示
    font = pygame.font.SysFont(None, 32)
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (20, 50))

    player(playerX, playerY)
     
    # 残り時間
    time_remaining = max(0, (time_limit - elapsed_time) // 1000) 
    time_text = font.render(f"Time Remaining: {time_remaining} seconds", True, (255, 255, 255))
    screen.blit(time_text, (20, 20))

    pygame.display.update()

    if game_over:
        screen.fill((0, 0, 0))
        game_over_font = pygame.font.SysFont(None, 64)
        game_over_text = game_over_font.render("Thank you for playing!!", True, (255, 0, 0))
        screen.blit(game_over_text, (200, 250))

        font = pygame.font.SysFont(None, 32)
        final_score_text = font.render(f"Final Score: {str(score_value)}", True, (255, 255, 255))
        screen.blit(final_score_text, (250, 350))

        pygame.display.update()

        pygame.time.wait(5000)
        pygame.quit()
        quit()
