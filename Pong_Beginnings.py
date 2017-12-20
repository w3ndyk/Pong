import pygame
import sys

wn_w = 920
wn_h = 570
speed = 10

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

pygame.init()


# !!!!! REMEMBER: (0,0) is top left; (wn_w,wn_h) is bottom right !!!!!
def main():
    pygame.display.set_caption('PONG')
    screen = pygame.display.set_mode((wn_w, wn_h), pygame.SRCALPHA)

    # paddle
    paddle_w = 20
    paddle_h = 70

    # left paddle
    l_paddle = pygame.Surface((paddle_w, paddle_h))
    x1 = 15
    y1 = (wn_h/2) - (paddle_h/2)
    l_paddle_rect = pygame.Rect(x1, y1, paddle_w, paddle_h)
    l_up = False
    l_down = False
    l_paddle.fill(RED)

    # right paddle
    r_paddle = pygame.Surface((paddle_w, paddle_h))
    x2 = (wn_w - paddle_w) - 15
    y2 = (wn_h/2) - (paddle_h/2)
    r_paddle_rect = pygame.Rect(x2, y2, paddle_w, paddle_h)
    r_up = False
    r_down = False
    r_paddle.fill(CYAN)

    # ball
    ball_w = ball_h = 20
    ball_speed = [5, 5]
    ball = pygame.Surface((ball_w, ball_h))
    x_ball = (wn_w/2) - (ball_w/2)
    y_ball = (wn_h/2) - (ball_h/2)
    ball_rect = pygame.Rect(x_ball, y_ball, ball_w, ball_h)
    ball.fill(WHITE)

    clock = pygame.time.Clock()
    play = True

    # game play
    while play:
        for event in pygame.event.get():
            # window exit button
            if event.type == pygame.QUIT:
                sys.exit()
            # keyboard for paddles
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    r_up = True
                    r_down = False
                elif event.key == pygame.K_DOWN:
                    r_up = False
                    r_down = True
                elif event.key == pygame.K_w:
                    l_up = True
                    l_down = False
                elif event.key == pygame.K_s:
                    l_up = False
                    l_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    r_up = False
                elif event.key == pygame.K_DOWN:
                    r_down = False
                elif event.key == pygame.K_w:
                    l_up = False
                elif event.key == pygame.K_s:
                    l_down = False

        # moving up or down
        if r_up or r_down or l_up or l_down:
            if l_up:
                l_paddle_rect.top -= speed
            if l_down:
                l_paddle_rect.top += speed
            if r_up:
                r_paddle_rect.top -= speed
            if r_down:
                r_paddle_rect.top += speed

        # bounds for paddles
        if l_paddle_rect.top < 0:
            l_paddle_rect.top = 0
        if l_paddle_rect.bottom > wn_h:
            l_paddle_rect.bottom = wn_h
        if r_paddle_rect.top < 0:
            r_paddle_rect.top = 0
        if r_paddle_rect.bottom > wn_h:
            r_paddle_rect.bottom = wn_h

        # ball bouncing on walls
        if ball_rect.top >= wn_h - ball_rect.height or ball_rect.bottom <= ball_rect.height:
            ball_speed = (ball_speed[0], -ball_speed[1])

        ball_rect = ball_rect.move(ball_speed)

        # ball bouncing on paddles
        if (ball_rect.right >= r_paddle_rect.left - 5) and (ball_rect.right <= r_paddle_rect.left + 5) \
                and (ball_rect.bottom >= r_paddle_rect.top) and (ball_rect.bottom <= r_paddle_rect.top + paddle_h):
            ball_speed = (-ball_speed[0], ball_speed[1])
        elif (ball_rect.left >= l_paddle_rect.right - 5) and (ball_rect.left <= l_paddle_rect.right + 5) \
                and (ball_rect.bottom >= l_paddle_rect.top) and (ball_rect.bottom <= l_paddle_rect.top + paddle_h):
            ball_speed = (-ball_speed[0], ball_speed[1])

        # blit images
        screen.fill(BLACK)
        screen.blit(ball, ball_rect)
        screen.blit(l_paddle, l_paddle_rect)
        screen.blit(r_paddle, r_paddle_rect)

        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
