import pygame
import math
import random
#
# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game clock
clock = pygame.time.Clock()

# Load assets (optional: replace with actual images)
tower_image = pygame.Surface((40, 40))
tower_image.fill(GREEN)

enemy_image = pygame.Surface((30, 30))
enemy_image.fill(RED)

bullet_image = pygame.Surface((10, 10))
bullet_image.fill(BLUE)

# Define Enemy class
class Enemy:
    def __init__(self, path):
        """Initialize enemy with path, speed, and health."""
        self.path = path
        self.speed = 2
        self.health = 100
        self.index = 0  # Current position in path
        self.x, self.y = self.path[self.index]  # Start position
        self.alive = True

    def move(self):
        """Move enemy along the predefined path."""
        if self.index < len(self.path) - 1:
            target_x, target_y = self.path[self.index + 1]
            dir_x, dir_y = target_x - self.x, target_y - self.y
            dist = math.sqrt(dir_x ** 2 + dir_y ** 2)

            if dist != 0:
                dir_x, dir_y = dir_x / dist, dir_y / dist  # Normalize

            self.x += dir_x * self.speed
            self.y += dir_y * self.speed

            if dist < self.speed:  # Move to next point
                self.index += 1
        else:
            self.alive = False  # Enemy reached the end

    def draw(self, screen):
        """Draw enemy on screen."""
        screen.blit(enemy_image, (self.x - 15, self.y - 15))

# Define Tower class
class Tower:
    def __init__(self, x, y):
        """Initialize tower at (x, y)."""
        self.x, self.y = x, y
        self.range = 100
        self.fire_rate = 30  # Delay between shots
        self.timer = 0

    def shoot(self, enemies, bullets):
        """Fire bullets at enemies in range."""
        self.timer += 1
        if self.timer >= self.fire_rate:
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
                if dist <= self.range:
                    bullets.append(Bullet(self.x, self.y, enemy))
                    self.timer = 0  # Reset timer
                    break  # Only shoot one enemy per cycle

    def draw(self, screen):
        """Draw tower on screen."""
        screen.blit(tower_image, (self.x - 20, self.y - 20))

# Define Bullet class
class Bullet:
    def __init__(self, x, y, target):
        """Initialize bullet targeting an enemy."""
        self.x, self.y = x, y
        self.speed = 5
        self.target = target
        self.alive = True

    def move(self):
        """Move bullet towards the target."""
        if not self.target.alive:
            self.alive = False
            return

        dir_x, dir_y = self.target.x - self.x, self.target.y - self.y
        dist = math.sqrt(dir_x ** 2 + dir_y ** 2)

        if dist != 0:
            dir_x, dir_y = dir_x / dist, dir_y / dist

        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

        if dist < self.speed:  # Bullet hit the enemy
            self.target.health -= 50  # Reduce enemy health
            if self.target.health <= 0:
                self.target.alive = False
            self.alive = False

    def draw(self, screen):
        """Draw bullet on screen."""
        screen.blit(bullet_image, (self.x - 5, self.y - 5))

# Main game loop
def main():
    """Main game function."""
    running = True

    # Define enemy path
    path = [(50, 300), (200, 300), (400, 200), (600, 200), (750, 300)]

    # Game entities
    enemies = []
    towers = []
    bullets = []

    spawn_timer = 0  # Timer for spawning enemies

    while running:
        screen.fill(WHITE)  # Clear screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                towers.append(Tower(mx, my))  # Place a new tower

        # Spawn enemies
        spawn_timer += 1
        if spawn_timer >= 100:
            enemies.append(Enemy(path))
            spawn_timer = 0

        # Update enemies
        for enemy in enemies[:]:
            enemy.move()
            if not enemy.alive:
                enemies.remove(enemy)

        # Update towers (shoot bullets)
        for tower in towers:
            tower.shoot(enemies, bullets)

        # Update bullets
        for bullet in bullets[:]:
            bullet.move()
            if not bullet.alive:
                bullets.remove(bullet)

        # Draw path
        for i in range(len(path) - 1):
            pygame.draw.line(screen, BLACK, path[i], path[i + 1], 5)

        # Draw entities
        for enemy in enemies:
            enemy.draw(screen)
        for tower in towers:
            tower.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()  # Refresh screen
        clock.tick(30)  # 30 FPS

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
