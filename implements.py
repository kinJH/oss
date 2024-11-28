import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self, ball: 'Ball'):
        if self.alive and self.rect.colliderect(ball.rect):  # 충돌 감지
            self.alive = False  # 블록 상태 변경
            ball.dir = 360 - ball.dir  # 공의 방향 변경
            self.color =(0,0,0)  #블록 색 변경
        
        


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)  # 공의 초기 방향을 랜덤으로 설정

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        for block in blocks:
            if block.alive and self.rect.colliderect(block.rect):  # 블록과 충돌 여부 확인
                block.collide(self)  # Block의 collide 메서드 호출
                # 공의 방향을 블록의 가로/세로 면 충돌에 따라 반사 처리
                if abs(self.rect.right - block.rect.left) <= self.speed or abs(self.rect.left - block.rect.right) <= self.speed:
                    self.dir = 180 - self.dir  # 좌우 면 충돌
                elif abs(self.rect.bottom - block.rect.top) <= self.speed or abs(self.rect.top - block.rect.bottom) <= self.speed:
                    self.dir = 360 - self.dir  # 상하 면 충돌
                break  # 한 번 충돌하면 루프 종료

    def collide_paddle(self, paddle: Paddle):
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)  # 공의 반사 각도를 약간 변형
            self.rect.top = paddle.rect.top - self.rect.height  # 공이 패들에 묻히는 현상 방지

    def hit_wall(self):
        # 좌우 벽 충돌 처리
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:
            self.dir = 180 - self.dir
        # 상단 벽 충돌 처리
        if self.rect.top <= 0:
            self.dir = 360 - self.dir

    def alive(self):
        # 공이 화면 하단으로 떨어졌는지 확인
        if self.rect.top >= config.display_dimension[1]:
            return False  # 공이 죽었음
        return True  # 공이 살아 있음


