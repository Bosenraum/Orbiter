from engine import *
import random


class Ball:

    def __init__(self, x, y, radius, vel, color=WHITE):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = vel

    def check_collision(self, b2):
        # Check collision with other ball
        if self == b2:
            return False
        if Vec2(self.x, self.y).distance(Vec2(b2.x, b2.y)) < self.radius + b2.radius:
            return True
        return False

    def get_angle(self, vec):
        pos = Vec2(self.x, self.y)
        return pos.angle(vec)

    def move(self):
        self.x += self.vel.x
        self.y += self.vel.y

    def draw(self, scr):
        pygame.draw.circle(scr, self.color, (self.x, self.y), self.radius)


class DriverEngine(Engine):
    APP_NAME = "DriveEngine"

    def __init__(self, width, height, pf):
        self.num_balls = None
        self.balls = []
        super().__init__(width, height, pf)

    # called once before the loop begins
    def on_start(self):
        self.num_balls = 50
        for i in range(self.num_balls):
            radius = random.randint(8, 20)
            x = random.randint(0 + radius, self.width - radius)
            y = random.randint(0 + radius, self.height - radius)
            vel = Vec2(random.randint(-4, 4), random.randint(-4, 4))
            color = get_random_color((50, 200), (50, 200), (50, 200))
            ball = Ball(x, y, radius, vel, color)

            # Don't place balls on top of each other
            valid_pos = False
            while not valid_pos:
                if self.check_collisions(ball):
                    x = random.randint(0 + radius, self.width - radius)
                    y = random.randint(0 + radius, self.height - radius)
                    ball.x = x
                    ball.y = y
                else:
                    valid_pos = True

            self.balls.append(ball)

    # called once per loop iteration
    def on_update(self, elapsed_time):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(BLACK)
        # Draw stuff
        for ball in self.balls:
            self.check_collisions(ball)
            ball.move()
            ball.draw(self.screen)

        # self.draw_pixels()

        # pygame.draw.rect(self.screen, alabaster, pygame.Rect(0, 0, 400, 400), border_radius=10)
        pygame.display.update()

    def check_collisions(self, ball):
        # Check for wall collisions
        collision_detected = False
        if ball.x < ball.radius or ball.x > (self.width - ball.radius):
            ball.vel.x *= -1
            collision_detected = True
        if ball.y < ball.radius or ball.y > (self.height - ball.radius):
            ball.vel.y *= -1
            collision_detected = True

        # for b2 in self.balls:
        #     if ball.check_collision(b2):
        #         angle = Vec2(ball.vel.x, ball.vel.y).angle(Vec2(b2.vel.x, b2.vel.y))
        #         dx = -1 if math.cos(angle) < 0 else 1
        #         dy = -1 if math.sin(angle) < 0 else 1
        #
        #         ball.vel.x *= dx
        #         ball.vel.y *= dy
        #         # b2.vel.x *= dx
        #         # b2.vel.y *= dy
        #         collision_detected = True

        return collision_detected

    def draw_pixels(self):
        for col in self.pixels:
            for pixel in col:
                pixel.draw(self.screen)


if __name__ == "__main__":
    driver = DriverEngine(720, 480, 2)
    driver.start()
