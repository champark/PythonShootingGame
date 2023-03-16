import pygame
import sys
from pygame.locals import *

# 이미지 로딩
img_galaxy = pygame.image.load("image/galaxy.png")
img_ship = [
    pygame.image.load("image/starship.png"),
    pygame.image.load("image/starship_l.png"),
    pygame.image.load("image/starship_r.png"),
    pygame.image.load("image/starship_burner.png")
]
img_weapon = pygame.image.load("image/bullet.png")

tmr = 0
bg_y = 0

s_x = 480       # 플레이어 기체의 X 좌표
s_y = 360       # 플레이어 기체의 Y 좌표
s_d = 0         # 플레이어 기체의 기울기 변수
key_spc = 0     # 스페이스 키를 눌렀을 때 사용하는 변수

MISSILE_MAX = 200
msl_no = 0
msl_f = [False] * MISSILE_MAX
msl_x = [0] * MISSILE_MAX
msl_y = [0] * MISSILE_MAX

def move_starship(scrn, key): # 플레이어 기체 이동
    global s_x, s_y, s_d, key_spc
    s_d = 0
    if key[pygame.K_UP] == 1:
        s_y = s_y - 20
        if s_y < 80:
            s_y = 80
    if key[pygame.K_DOWN] == 1:
        s_y = s_y + 20
        if s_y > 640:
            s_y = 640
    if key[pygame.K_LEFT] == 1:
        s_d = 1
        s_x = s_x - 20
        if s_x < 40:
            s_x = 40
    if key[pygame.K_RIGHT] == 1:
        s_d = 2
        s_x = s_x + 20
        if s_x > 920:
            s_x = 920
            
    key_spc = (key_spc + 1) * key[K_SPACE]                          # 스페이스 키를 누르는 동안 변수 값 증가
    if key_spc % 4 == 1:                                            # 스페이스 키를 처음 누른 후,4 프레임마다 탄환 발사
        set_missile()                                               # 미사일 발사

    scrn.blit(img_ship[3], [s_x - 8, s_y + 40 + (tmr % 3)*2])       # 엔진 불꽃 그리기
    scrn.blit(img_ship[s_d], [s_x - 37 , s_y - 48])                 # 플레이어 기체 그리기

def set_missile():  # 플레이어 기체 발사 탄환 설정
    global msl_no
    msl_f[msl_no] = True
    msl_x[msl_no] = s_x
    msl_y[msl_no] = s_y - 50
    msl_no = (msl_no + 1) % MISSILE_MAX

def move_missile(scrn): # 탄환이동
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            msl_y[i] = msl_y[i] - 36
            scrn.blit(img_weapon, [msl_x[i] - 10, msl_y[i] - 32])
            if msl_y[i] < 0:
                msl_f[i] = False

def main(): # 메인 루프
    global tmr, bg_y
    pygame.init()
    pygame.display.set_caption("파이썬 슈팅게임")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((960, 720), pygame.FULLSCREEN)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

        # 배경 스크롤
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed()
        move_starship(screen, key)
        move_missile(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()