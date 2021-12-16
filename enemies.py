import pygame as pg


class Enemy:
    """общий класс для всех врагов"""
    def __init__(self, img, speed, hp, attack):
        self.icon = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
