import pygame
import sys
import os
import time

# force static position of screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

wn_w = 920
wn_h = 570
speed = 10
fps = 60
# colors
WHITE = (255, 255, 255)

pygame.init()

# to get rid of sound lag
pygame.mixer.pre_init(44100, -16, 2, 2048)


class Game:
    def __init__(self, caption, screen_w, screen_h):
        self.caption = pygame.display.set_caption(str(caption))
        self.screen = pygame.display.set_mode((screen_w, screen_h), pygame.SRCALPHA)
        self.l_up = self.l_down = self.r_up = self.r_down = True
        self.clock = pygame.time.Clock()
        self.intro = self.play = True
        self.outro = False
        self.countdown = True

        self.title = Text(150, "Pong", WHITE, 460, 235)
        self.click = Text(50, "-- Click here to start --", WHITE, 460, 335)
        self.l_score = Text(90, "0", WHITE, 230, 100)
        self.r_score = Text(90, "0", WHITE, 690, 100)
        self.winner = Text(150, "Winner", WHITE, 460, 200)
        self.again = Text(50, "-- Click here to play again --", WHITE, 460, 335)

        self.opening = pygame.mixer.Sound("my_sounds/opening.ogg")
        self.game_music = pygame.mixer.Sound("my_sounds/game_music.ogg")
        self.point = pygame.mixer.Sound("my_sounds/scores.ogg")
        self.ending = pygame.mixer.Sound("my_sounds/ending.ogg")
        self.count_music = pygame.mixer.Sound("my_sounds/countdown.ogg")
        self.count_music_end = pygame.mixer.Sound("my_sounds/countdown_end.ogg")

        self.intro_bg = pygame.image.load("images/opening_bg.jpg").convert()
        self.intro_bg = pygame.transform.scale(self.intro_bg, (wn_w, wn_h))
        self.intro_bg_rect = self.intro_bg.get_rect()
        self.game_bg = pygame.image.load("images/game_bg.png").convert()
        self.game_bg = pygame.transform.scale(self.game_bg, (wn_w, wn_h))
        self.game_bg_rect = self.game_bg.get_rect()
        self.outro_bg = pygame.image.load("images/end_bg.png").convert()
        self.outro_bg = pygame.transform.scale(self.outro_bg, (wn_w, wn_h))
        self.outro_bg_rect = self.outro_bg.get_rect()

    def update(self, b, lp, rp, l_s, r_s):
        # increments score and repositions ball
        if b.rect.right < 0:
            self.game_music.stop()
            self.point.play(0)
            rp.score += 1
            r_s.image = r_s.font.render(str(rp.score), 1, WHITE)
            time.sleep(1.5)
            b.rect.center = (wn_w / 2, wn_h / 2)
            lp.rect.topleft = (15, (wn_h / 2) - (90 / 2))
            rp.rect.topleft = ((wn_w - 30) - 15, (wn_h / 2) - (90 / 2))
            time.sleep(1.5)
            self.countdown = True

        if b.rect.left > wn_w:
            self.game_music.stop()
            self.point.play(0)
            lp.score += 1
            l_s.image = l_s.font.render(str(lp.score), 1, WHITE)
            time.sleep(1.5)
            b.rect.center = (wn_w / 2, wn_h / 2)
            lp.rect.topleft = (15, (wn_h / 2) - (90 / 2))
            rp.rect.topleft = ((wn_w - 30) - 15, (wn_h / 2) - (90 / 2))
            time.sleep(1.5)
            self.countdown = True

        if lp.score == 3 or rp.score == 3:
            self.play = False
            self.game_music.stop()
            if lp.score > rp.score:
                self.winner = Text(150, "Player 1 wins!", WHITE, 460, 200)
            if rp.score > lp.score:
                self.winner = Text(150, "Player 2 wins!", WHITE, 460, 200)
            self.outro = True
            self.ending.play(0)

    def blink(self, image, rect):
        # blinking text
        if (pygame.time.get_ticks() % 1000) < 500:
            self.screen.blit(image, rect)

    def cd(self, ball, lp, rp):
        countdown = [3, 2, 1]
        for x in countdown:
            num = Text(350, str(x), WHITE, 460, 285)

            self.screen.blit(self.game_bg, self.game_bg_rect)
            self.screen.blit(ball.image, ball.rect)
            self.screen.blit(lp.image, lp.rect)
            self.screen.blit(rp.image, rp.rect)

            self.screen.blit(num.image, num.rect)
            pygame.display.flip()
            self.count_music.play(0)
            self.clock.tick(fps)
            time.sleep(.75)

        self.count_music_end.play(0)
        time.sleep(1)
        self.countdown = False
        self.game_music.play(-1)


class Text:
    def __init__(self, size, text, color, x, y):
        self.font = pygame.font.Font(None, int(size))
        self.image = self.font.render(str(text), 1, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Paddle:
    def __init__(self, x, y, paddle_speed, width, height, image):
        # initialize paddle's variables
        self.x = x
        self.y = y
        self.speed = paddle_speed
        self.width = width
        self.height = height

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.score = 0

    def update(self, up, down):
        # moving up or down
        if up or down:
            if up:
                self.rect.y -= self.speed
            if down:
                self.rect.y += self.speed

        # bounds for paddles
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > wn_h:
            self.rect.bottom = wn_h


class Ball:
    def __init__(self, x, y, ball_speed, dim):
        # initialize ball's variables
        self.x = x
        self.y = y
        self.speed = ball_speed
        self.dim = dim
        self.image = pygame.image.load("images/ball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.dim, self.dim))
        self.rect = pygame.Rect(self.x, self.y, self.dim, self.dim)

        self.hit_wall = pygame.mixer.Sound("my_sounds/hit_wall.ogg")
        self.hit_wall.set_volume(0.25)
        self.hit_paddle = pygame.mixer.Sound("my_sounds/hit_paddle.ogg")
        self.hit_paddle.set_volume(0.25)

    def update(self, lp, rp):
        # ball bouncing on walls
        if self.rect.top < 0 or self.rect.top > wn_h - self.rect.height:
            self.hit_wall.play(0)
            self.speed[1] = -self.speed[1]

        # ball bouncing on paddles
        if (self.rect.left > lp.rect.right - 5) and (self.rect.left < lp.rect.right + 5) \
                and (self.rect.bottom > lp.rect.top) and (self.rect.top < lp.rect.bottom):
            self.hit_paddle.play(0)
            self.speed[0] = -self.speed[0]
        if (self.rect.right < rp.rect.left + 5) and (self.rect.right > rp.rect.left - 5) \
                and (self.rect.bottom > rp.rect.top) and (self.rect.top < rp.rect.bottom):
            self.hit_paddle.play(0)
            self.speed[0] = -self.speed[0]

        self.rect = self.rect.move(self.speed)


def main():
    global wn_w, wn_h, speed, fps, WHITE

    while True:
        # objects
        game = Game('PONG', wn_w, wn_h)
        l_paddle = Paddle(15, (wn_h / 2) - (90 / 2), speed, 30, 100, "images/red_paddle.png")
        r_paddle = Paddle((wn_w - 30) - 15, (wn_h / 2) - (90 / 2), speed, 30, 100, "images/cyan_paddle.png")
        ball = Ball((wn_w / 2) - (30 / 2), (wn_h / 2) - (30 / 2), [5, 5], 30)

        # music
        game.opening.play(-1)

        # intro
        while game.intro:
            # checks if window exit button is pressed or if screen is clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    game.screen.blit(game.click.image, game.click.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    game.intro = False
                    game.opening.stop()
                    time.sleep(1)

            # blit images
            game.screen.blit(game.intro_bg, game.intro_bg_rect)
            game.screen.blit(game.title.image, game.title.rect)
            # blinking -- click here to start
            game.blink(game.click.image, game.click.rect)

            # limits frames per iteration of while loop
            game.clock.tick(fps)
            # writes to main surface
            pygame.display.flip()

        # game play
        while game.play:
            for event in pygame.event.get():
                # window exit button
                if event.type == pygame.QUIT:
                    sys.exit()
                # keyboard for paddles
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.r_up = True
                        game.r_down = False
                    elif event.key == pygame.K_DOWN:
                        game.r_up = False
                        game.r_down = True
                    elif event.key == pygame.K_w:
                        game.l_up = True
                        game.l_down = False
                    elif event.key == pygame.K_s:
                        game.l_up = False
                        game.l_down = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        game.r_up = False
                    elif event.key == pygame.K_DOWN:
                        game.r_down = False
                    elif event.key == pygame.K_w:
                        game.l_up = False
                    elif event.key == pygame.K_s:
                        game.l_down = False

            while game.countdown:
                game.cd(ball, l_paddle, r_paddle)

            l_paddle.update(game.l_up, game.l_down)
            r_paddle.update(game.r_up, game.r_down)
            ball.update(l_paddle, r_paddle)
            game.update(ball, l_paddle, r_paddle, game.l_score, game.r_score)

            # blit images
            game.screen.blit(game.game_bg, game.game_bg_rect)

            game.screen.blit(ball.image, ball.rect)
            game.screen.blit(l_paddle.image, l_paddle.rect)
            game.screen.blit(r_paddle.image, r_paddle.rect)

            game.screen.blit(game.l_score.image, game.l_score.rect)
            game.screen.blit(game.r_score.image, game.r_score.rect)

            game.clock.tick(fps)
            pygame.display.flip()

        while game.outro:
            # checks if window exit button is pressed or if screen is clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    game.screen.blit(game.again.image, game.again.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    game.outro = False
                    game.ending.stop()
                    time.sleep(1.5)

            # blit images
            game.screen.blit(game.outro_bg, game.outro_bg_rect)
            game.screen.blit(game.winner.image, game.winner.rect)
            # blinking -- click here to start
            game.blink(game.again.image, game.again.rect)

            # limits frames per iteration of while loop
            game.clock.tick(fps)
            # writes to main surface
            pygame.display.flip()


if __name__ == "__main__":
    main()
