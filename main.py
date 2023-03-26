import pygame
import sys
import math
import random
from pygame.locals import *

BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)

# 이미지 로딩
img_galaxy = pygame.image.load("image/galaxy.png")
img_ship = [
    pygame.image.load("image/starship.png"),
    pygame.image.load("image/starship_l.png"),
    pygame.image.load("image/starship_r.png"),
    pygame.image.load("image/starship_burner.png")
]
img_weapon = pygame.image.load("image/bullet.png")
img_shield = pygame.image.load("image/shield.png")
img_enemy = [
    pygame.image.load("image/enemy0.png"),
    pygame.image.load("image/enemy1.png")
]
img_explode = [
    None,
    pygame.image.load("image/explosion1.png"),
    pygame.image.load("image/explosion2.png"),
    pygame.image.load("image/explosion3.png"),
    pygame.image.load("image/explosion4.png"),
    pygame.image.load("image/explosion5.png"),
]
img_title = [
    pygame.image.load("image/nebula.png"),
    pygame.image.load("image/logo.png")
]

idx = 0             # 인덱스 변수
tmr = 0             # 타이머 변수
score = 0           # 점수 변수
bg_y = 0            # 배경 스크롤용 변수

s_x = 0           # 플레이어 기체의 X 좌표
s_y = 0           # 플레이어 기체의 Y 좌표
s_d = 0             # 플레이어 기체의 기울기 변수
s_shield = 0      # 플레이어 기체의 실드량 변수
s_unvincible = 0    # 플레이어 기체의 무적 상태 변수
key_spc = 0         # 스페이스 키를 눌렀을 때 사용하는 변수
key_z = 0           # z 키를 눌렀을 때 사용할 변수

MISSILE_MAX = 200
msl_no = 0
msl_f = [False] * MISSILE_MAX
msl_x = [0] * MISSILE_MAX           # 탄환의 X 좌표
msl_y = [0] * MISSILE_MAX           # 탄환의 Y 좌표
msl_a = [0] * MISSILE_MAX           # 탄환의 날아가는 각도 리스트

ENEMY_MAX = 100
emy_no = 0                          # 적 등장 시 사용할 리스트 인덱스 변수
emy_f = [False] * ENEMY_MAX         # 적 등장 여부 관리 플래그 리스트
emy_x = [0] * ENEMY_MAX             # 적의 X 좌표 리스트
emy_y = [0] * ENEMY_MAX             # 적의 Y 좌표 리스트
emy_a = [0] * ENEMY_MAX             # 적의 비행 각도리스트
emy_type = [0] * ENEMY_MAX          # 적의 종류 리스트
emy_speed = [0] * ENEMY_MAX         # 적 속도 리스트

EMY_BULLET = 0
LINE_T = -80                        # 적이 나타나는(사라지는) 위쪽 좌표
LINE_B = 800                        # 적이 나타나는(사라지는) 아래쪽 좌표
LINE_L = -80                        # 적이 나타나는(사라지는) 왼쪽 좌표
LINE_R = 1040                       # 적이 나타나는(사라지는) 오른쪽 좌표

EFFECT_MAX = 100                    # 폭팔 연출 최대 수 정의
eff_no = 0                          # 폭팔 연출 시 사용할 리스트 인덱스 변수
eff_p = [0] * EFFECT_MAX            # 폭팔 연출 시 이미지 번호 리스트
eff_x = [0] * EFFECT_MAX            # 폭팔 연출 시 X 좌표 리스트
eff_y = [0] * EFFECT_MAX            # 폭팔 연출 시 Y 좌표 리스트

def get_dis(x1, y1, x2, y2):                                # 두 점 사이 거리 계산
    return ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))  # 제곱한 값을 반환(루트 미 사용)

# 문자 표시 함수
def draw_text(scrn, txt, x, y, siz, col):       # 문자 표시
    fnt = pygame.font.Font(None, siz)           # 폰트 객체 생성
    sur = fnt.render(txt, True, col)            # 문자열을 그릴 surface 생성
    x = x - sur.get_width() / 2                 # 중심선을 표시할 x 좌표 계산
    y = y - sur.get_height() / 2                # 중심선을 표시할 Y 좌표 계산
    scrn.blit(sur, [x, y])                      # 문자열을 그린 Surface를 화면에 전송

def move_starship(scrn, key): # 플레이어 기체 이동
    global idx, tmr, s_x, s_y, s_d, key_spc, key_z , s_shield, s_unvincible       # 전역변수 선언
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
        set_missile(0)                                              # 미사일 발사
    key_z = (key_z + 1) * key[K_z]                                  # Z키를 누르는 동안 변수 값 증가
    if key_z == 1 and s_shield > 10:                                # 한 번 눌렀을 때 실드량이 10보다 크다면
        set_missile(10)                                             # 탄막치기
        s_shield = s_shield - 10                                    # 실드량 10 감소

    if s_unvincible % 2 == 0:                                       # 무적 상태에서 깜빡이기 위한 if 구문
        scrn.blit(img_ship[3], [s_x - 8, s_y + 40 + (tmr % 3)*2])   # 엔진 불꽃 그리기
        scrn.blit(img_ship[s_d], [s_x - 37 , s_y - 48])             # 플레이어 기체 그리기

    if s_unvincible > 0:                                            # 무적 상태라면
        s_unvincible = s_unvincible - 1                             # ss_unvencible 값 감소
        return                                                      # 함수를 벗어남(적과 히트 체크 미수행)
    elif idx == 1:
        for i in range(ENEMY_MAX):                                      # 적 기체와 히트 체크
            if emy_f[i] == True:                                        # 적 기체가 존재한다면
                w = img_enemy[emy_type[i]].get_width()                  # 적 기체 이미지 폭
                h = img_enemy[emy_type[i]].get_height()                 # 적 기체 이미지 높이
                r = int((w + h) / 4 + (74 + 96) / 4)                    # 히트 체크 거리 계산
                if get_dis(emy_x[i], emy_y[i], s_x, s_y) < r * r:       # 적 기체와 플레이어 기체 사이의 거리가 히트 체크 거리보다 작으면
                    set_effect(s_x, s_y)                                # 폭팔 연출 설정
                    s_shield = s_shield - 10                            # 실드량 감소
                    if s_shield <= 0:                                   # 실드값이 0 이하일 경우
                        s_shield = 0                                    # 실드값 0으로
                        idx = 2                                         # 게임오버
                        tmr = 0
                    if s_unvincible == 0:                               # 무적 상태가 아니라면
                        s_unvincible = 60                               # 무적 상태로 설정
                    emy_f[i] = False                                    # 적 기체 삭제

def set_missile(typ):  # 플레이어 기체 발사 탄환 설정
    global msl_no
    if typ == 0:                                                    # 단발발사
        msl_f[msl_no] = True                                        # 탄환 발사 플래그 True 설정
        msl_x[msl_no] = s_x                                         # 탄환 X 좌표
        msl_y[msl_no] = s_y - 50                                    # 탄환 Y 좌표
        msl_a[msl_no] = 270                                         # 탄환 발사 각도
        msl_no = (msl_no + 1) % MISSILE_MAX                         # 다음 설정을 위한 번호 계산
    if typ == 10:                                                   # 탄막발사
        for a in range(160, 390, 10):
            msl_f[msl_no] = True
            msl_x[msl_no] = s_x
            msl_y[msl_no] = s_y - 50
            msl_a[msl_no] = a
            msl_no = (msl_no + 1) % MISSILE_MAX             

def move_missile(scrn): # 탄환이동
    for i in range(MISSILE_MAX):        # 반복해서
        if msl_f[i] == True:            # 탄환이 발사된 상태라면
            msl_x[i] = msl_x[i] + 36 * math.cos(math.radians(msl_a[i]))             # x 좌표 계산
            msl_y[i] = msl_y[i] + 36 * math.sin(math.radians(msl_a[i]))             # y 좌표 계산
            img_rz = pygame.transform.rotozoom(img_weapon, -90 - msl_a[i], 1.0)     # 탄환이 날아가는 각도의 회전 이미지 생성
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2])  # 탄환 이미지
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False


def bring_enemy():      # 적 기체 등장
    if tmr % 30 == 0:
        set_enemy(random.randint(20, 940), LINE_T, 90, 1, 6)            # 일반 기체 1기 등장

def set_enemy(x, y, a, ty, sp):     # 적 기체 설정
    global emy_no                   # 전역 변수 선언
    while True:                     # 무한 반복
        if emy_f[emy_no] == False:  # 비어 있는 리스트의 경우
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            break
        emy_no = (emy_no + 1) % ENEMY_MAX   # 다음 설정을 위한 번호 계산

def move_enemy(scrn):   # 적 기체 이동
    global idx, tmr, score, s_shield
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90 - emy_a[i]
            png = emy_type[i]
            emy_x[i] = emy_x[i] + emy_speed[i] * math.cos(math.radians(emy_a[i]))
            emy_y[i] = emy_y[i] + emy_speed[i] * math.sin(math.radians(emy_a[i]))
            if emy_type[i] == 1 and emy_y[i] > 360:         # 적 기체의 Y 좌표가 360을 넘었다면
                set_enemy(emy_x[i], emy_y[i], 90, 0, 8)     # 탄환발사
                emy_a[i] = -45
                emy_speed[i] = 16
            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:        # 화면 상하좌우에서 벗어났다면
                emy_f[i] = False                                                                        # 적 기체 삭제

            if emy_type[i] != EMY_BULLET:                   # 플레이어 기체 발사 탄환과 히트 체크
                w = img_enemy[emy_type[i]].get_width()      # 적 기체 이미지 폭
                h = img_enemy[emy_type[i]].get_height()     # 적 기체 이미지 높이
                r = int((w+h) / 4) + 12                     # 히트체크에 사용할 거리 계산
                for n in range(MISSILE_MAX):
                    if msl_f[n] == True and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r * r:
                        msl_f[n] = False                    # 탄환 삭제
                        set_effect(emy_x[i], emy_y[i])      # 폭팔 이펙트
                        score = score + 100                 # 점수 증가
                        emy_f[i] = False                    # 적 기체 삭제
                        if s_shield < 100:                  # 실드량 증가
                            s_shield = s_shield + 1

            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)                                # 적 기체를 회전시킨 이미지 생성
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2])  # 적 기체 이미지 그리기

def set_effect(x, y):                       # 폭팔 설정
    global eff_no                           # 전역 변수 선언
    eff_p[eff_no] = 1                       # 폭팔 연출 이미지 번호 대입
    eff_x[eff_no] = x                       # 폭팔 연출 X 좌표 대입
    eff_y[eff_no] = y                       # 폭팔 연출 Y 좌표 대입
    eff_no = (eff_no + 1) % EFFECT_MAX      # 다음 설정을 위한 번호 계산

def draw_effect(scrn):                      # 폭팔 연출
    for i in range(EFFECT_MAX) :            # 반복
        if eff_p[i] > 0:                    # 폭팔 연출 중이면
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48])     # 폭팔 연출 표시
            eff_p[i] = eff_p[i] + 1         # eff_p 값 1 증가
            if eff_p[i] == 6:               # eff_p가 6이 되었다면
                eff_p[i] = 0                # eff_p에 0 대입 후 연출 종료

def main(): # 메인 루프
    global idx, tmr, score, bg_y, s_x, s_y, s_d, s_shield, s_unvincible
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

        key = pygame.key.get_pressed()                      # key에 모든 키 상태 대입

        # 타이틀
        if idx == 0:
            img_rz = pygame.transform.rotozoom(img_title[0], -tmr % 360, 1.0)                   # 로고 뒤 회전하는 소용돌이 이미지
            screen.blit(img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2])  # 이미지를 화면에 그리기
            screen.blit(img_title[1], [70, 160])                                                # 로고 그리기
            draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)
            if key[K_SPACE] == 1:                                                               # 스페이스 키를 눌렀다면
                idx = 1                                                                         # 초기화
                tmr = 0
                score = 0
                s_x = 480
                s_y = 600
                s_d = 0
                s_shield = 100
                s_unvincible = 0
                for i in range(ENEMY_MAX):                                                      # 적 기체가 등장하지 않는 상태
                    emy_f[i] = False
                for i in range(MISSILE_MAX):                                                    # 플레이어 탄환 미 발사 상태
                    msl_f[i] = False

        # 게임 플레이중
        if idx == 1:
            move_starship(screen, key)
            move_missile(screen)
            bring_enemy()
            move_enemy(screen)
            if tmr == 30 * 60:      # tmr 값이 30x60이 되면 게임 클리어
                idx = 3
                tmr = 0

        # 게임오버
        if idx == 2:
            move_missile(screen)
            move_enemy(screen)
            draw_text(screen, "GAME OVER", 480, 300, 80, RED)

            if tmr == 150:          # tmr 값이 150 이면 타이틀 화면으로
                idx = 0
                tmr = 0

        # 게임 클리어
        if idx == 3:
            move_starship(screen, key)
            move_missile(screen)
            draw_text(screen, "GAME CLEAR", 480, 300, 80, SILVER)
            if tmr == 150:
                idx = 0
                tmr = 0

        # 폭팔 연출
        draw_effect(screen)
        draw_text(screen, "SCORE " + str(score), 200, 30, 50, SILVER)
        if idx != 0:    # 실드 표시
            screen.blit(img_shield, [40, 680])
            pygame.draw.rect(screen, (64, 32, 32), [40 + s_shield * 4 , 680, (100 - s_shield) * 4, 12])

        pygame.display.update()             # 화면 업데이트
        clock.tick(30)                      # 프레임 레이트 지정

if __name__ == '__main__':
    main()