import pygame
import sys
import random
import math
from pygame import Vector2, Surface, Rect
from abc import ABC
from abc import abstractmethod

WIDTH = 800
HEIGHT = 600
FPS = 60

class GameObject(ABC):
    @abstractmethod
    def draw(self, screen: Surface):
        pass

class DragonFire:
    def __init__(self) -> None:
        self.pos: Vector2 = Vector2(WIDTH // 2, HEIGHT - 50)
        self.image: Surface = pygame.image.load("resources/images/DragonFire.bmp")
        self.imagerect: Rect = self.image.get_rect()
        self.angle: int = 0
        self.is_firing: bool = False

    def tilt_clockwise(self):
        if self.angle < 90:
            self.angle += 1

    def tilt_counterclockwise(self):
        if self.angle > -90:
            self.angle -= 1

    def set_firing(self, is_firing: bool):
        self.is_firing = is_firing

    def draw(self, screen: Surface):
        image = pygame.transform.rotate(self.image, -self.angle)
        if self.is_firing:
            pygame.transform.threshold(image, image, (0, 0, 0), (0, 0, 0), (255, 0, 0), 1, 255, 0)
        imagerect = image.get_rect()
        screen.blit(
            image,
            (
                self.pos[0] - (imagerect[2] // 2),
                self.pos[1] - (imagerect[3] // 2),
            ),
            imagerect,
        )
        if self.is_firing:
            angle = self.angle - 90
            second_point = (
                1000 * math.cos(math.radians(angle)),
                1000 * math.sin(math.radians(angle))
            )
            pygame.draw.line(
                screen,
                (255, 0, 0),
                self.pos,
                (
                    self.pos + second_point
                ),
                5,
            )

class Drone(GameObject):
    def __init__(self) -> None:
        self.pos = Vector2(random.randint(0, WIDTH - 1), 0)
        self.speed: Vector2 = Vector2(
            random.uniform(-1, 1),
            random.random(),
        )
        self.image = pygame.image.load("resources/images/Drone.bmp")
        self.imagerect = self.image.get_rect()
        self.health = 1.0

    def draw(self, screen: Surface):
        self.pos += self.speed
        screen.blit(
            self.image,
            (
                self.imagerect[0] + self.pos[0],
                self.imagerect[1] + self.pos[1]
            )
        )

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("DragonFire Game")
        self.clock = pygame.time.Clock()
        self.drone_list = [Drone()]
        self.dragon_fire = DragonFire()

    def run_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Add a new drone
        if random.random() < 0.01:
            self.drone_list.append(Drone())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dragon_fire.tilt_counterclockwise()
        if keys[pygame.K_RIGHT]:
            self.dragon_fire.tilt_clockwise()
        
        if keys[pygame.K_SPACE]:
            self.dragon_fire.set_firing(True)
        else:
            self.dragon_fire.set_firing(False)


        self.screen.fill((0, 0, 0))


        for drone in self.drone_list:
            if (
                drone.pos[1] > HEIGHT
                or drone.pos[1] < 0
                or drone.pos[0] < 0
                or drone.pos[0] > WIDTH
                or drone.health <= 0
            ):
                self.drone_list.remove(drone)
                continue
            
            drone.draw(self.screen)
        
        self.dragon_fire.draw(self.screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        self.clock.tick(FPS)


if __name__ == "__main__":
    game = GameController()
    while True:
        game.run_loop()