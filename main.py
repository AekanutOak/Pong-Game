import pygame, math, random, sys, os
from pygame import mixer
from Paddle import Paddle
from Ball import Ball
from gtts import gTTS

WIDTH = 1280
HEIGHT = 720

PADDLE_SPEED = 600

WINNING_SCORE = 2

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

dirname = os.path.dirname(__file__)

class GameMain:
    def __init__(self):
        pygame.init()

        self.previous_time = pygame.time.get_ticks()
        self.mode = "multiplayer"
        self.color_choice = [
            (255,0,0),
            (255,127,0),
            (255,255,0),
            (0,255,0),
            (0,0,255),
            (75,0,130),
            (148,0,211)
        ]

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.mouse_click = False

        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)

        self.sounds_list = {
            'paddle_hit': mixer.Sound('sounds/paddle_hit.wav'),
            'score': mixer.Sound('sounds/score.wav'),
            'wall_hit': mixer.Sound('sounds/wall_hit.wav'),
            'easy':mixer.Sound('sounds/easy.mp3'),
            "lose":mixer.Sound('sounds/lose.mp3'),
            "ha":mixer.Sound('sounds/ha.mp3')
        }

        mixer.music.load("theme.mp3")
        mixer.music.set_volume(0)  # Set volume level (0.0 to 1.0)
        mixer.music.play(-1)

        self.player1 = Paddle(self.screen, 30, 90, 15, 100, WIDTH, HEIGHT)
        self.player2 = Paddle(self.screen, WIDTH - 30, HEIGHT - 90, 15, 100, WIDTH, HEIGHT)

        self.ball_size = 12
        self.ball = Ball(self.screen, WIDTH / 2 - self.ball_size/2, HEIGHT / 2 - self.ball_size/2, self.ball_size, self.ball_size, WIDTH, HEIGHT)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = 1
        self.winning_player = 0

        #1. 'start' (the beginning of the game, before first serve)
        #2. 'serve' (waiting on a key press to serve the ball)
        #3. 'play' (the ball is in play, bouncing between paddles)
        #4. 'done' (the game is over, with a victor, ready for restart)

        self.game_state = 'start'

        self.small_font = pygame.font.Font('./font.ttf', 24)
        self.large_font = pygame.font.Font('./font.ttf', 48)
        self.score_font = pygame.font.Font('./font.ttf', 96)

        #text
        self.t_welcome = self.small_font.render("Welcome to Pong!", False, (0,0,0))
        self.t_press_enter_begin = self.small_font.render('Press Enter to begin!', False, (0,0,0))
        self.t_player_turn = self.small_font.render("player" + str(self.serving_player) + "'s serve!", False, (0,0,0))
        self.t_press_enter_serve = self.small_font.render('Press Enter to serve!', False, (0,0,0))
        self.t_player_win = self.large_font.render("player" + str(self.serving_player) + "'s wins!", False, (0,0,0))
        self.t_press_restart = self.small_font.render("Press Enter to restart", False, (0,0,0))
        self.t_p1_score = self.score_font.render(str(self.player1_score), False, (0,0,0))
        self.t_p2_score = self.score_font.render(str(self.player2_score), False, (0,0,0))

        self.t_ball_size_display = self.small_font.render(f"Ball Size: {self.ball_size}",False,(0,0,0))
        self.t_add_ball_size = self.small_font.render("+",False,(0,0,0))
        self.t_remove_ball_size = self.small_font.render("-",False,(0,0,0))

        self.t_easy = self.small_font.render(f"Easy",False,(0,0,0))
        self.t_hard = self.small_font.render(f"Hard",False,(0,0,0))
        self.t_extreme = self.small_font.render(f"Extreme",False,(0,0,0))
        self.t_multiplayer = self.small_font.render(f"Multiplayer",False,(255,0,0))

        self.max_frame_rate = 60

    def update(self, dt):
        if self.game_state == "serve":
            self.ball.dy = random.uniform(-150, 150)
            if self.serving_player == 1:
                self.ball.dx = random.uniform(420, 600)
            else:
                self.ball.dx = -random.uniform(420, 600)
                
        elif self.game_state == 'play':

            if(self.mode == "easy"):
                if(pygame.time.get_ticks() - self.previous_time >= 1000):
                    if(self.player1.rect.y < HEIGHT/2):
                        random_dy = random.uniform(400,800) if random.choices([True,False],[0.8,0.2],k=1)[0] else random.uniform(-800,-400)
                        self.player1.dy = random_dy
                    else:
                        random_dy = random.uniform(400,800) if random.choices([True,False],[0.2,0.8],k=1)[0] else random.uniform(-800,-400)
                        self.player1.dy = random_dy

                    self.previous_time = pygame.time.get_ticks()

            elif(self.mode == "hard"):
                if(pygame.time.get_ticks() - self.previous_time >= 250):
                    if(self.ball.rect.y-50 < self.player1.rect.y):
                        self.player1.dy = -PADDLE_SPEED

                    elif(self.ball.rect.y-50 > self.player1.rect.y):
                        self.player1.dy = PADDLE_SPEED

                    else:
                        self.player1.dy = 0

                    self.previous_time = pygame.time.get_ticks()

            elif(self.mode == "extreme"):
                if(pygame.time.get_ticks() - self.previous_time >= 100):
                    if(self.ball.rect.y-50 < self.player1.rect.y):
                            self.player1.dy = -PADDLE_SPEED

                    elif(self.ball.rect.y-50 > self.player1.rect.y):
                        self.player1.dy = PADDLE_SPEED

                    else:
                        self.player1.dy = 0

                    self.previous_time = pygame.time.get_ticks()

            if self.ball.Collides(self.player1):

                if(self.mode != "extreme"):

                    # If ball is collided with paddle, change its direction (negative)
                    # and increase some horizontal speed by multiplication
                    if(pygame.key.get_pressed()[pygame.K_d]):

                        self.ball.dx = -self.ball.dx * 2
                        self.music_channel.play(self.sounds_list['score']) #reflect speed multiplier
                        
                    else:
                        self.ball.dx = -self.ball.dx * 1.03
                        self.music_channel.play(self.sounds_list['paddle_hit'])

                else:
                    power_up = random.choices([True,False],[0.3,0.7],k=1)[0]
                    if(power_up):
                        self.ball.dx = -self.ball.dx * 2
                        self.music_channel.play(self.sounds_list['score'])
                        sound_choice = ["easy","lose","ha"]
                        self.music_channel.play(self.sounds_list[random.choice(sound_choice)])
                        
                    else:
                        self.ball.dx = -self.ball.dx * 1.03
                        self.music_channel.play(self.sounds_list['paddle_hit'])

                self.ball.rect.x = self.player1.rect.x + self.ball_size+3

                # The vertical speed is random in each collision
                if self.ball.dy < 0:
                    self.ball.dy = -random.uniform(30, 450)
                else:
                    self.ball.dy = random.uniform(30, 450)


            if self.ball.Collides(self.player2):
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.ball.dx = -self.ball.dx * 2
                    self.music_channel.play(self.sounds_list['score'])

                else:
                    self.ball.dx = -self.ball.dx * 1.03
                    self.music_channel.play(self.sounds_list['paddle_hit'])

                self.ball.rect.x = self.player2.rect.x - self.ball_size
                if self.ball.dy < 0:
                    self.ball.dy = -random.uniform(30, 450)
                else:
                    self.ball.dy = random.uniform(30, 450)

                

            # ball hit top wall
            if self.ball.rect.y <= 0:
                self.ball.rect.y = 0
                self.ball.dy = -self.ball.dy
                self.music_channel.play(self.sounds_list['wall_hit'])

            # ball hit bottom wall
            if  self.ball.rect.y >= HEIGHT - self.ball_size:
                self.ball.rect.y = HEIGHT - self.ball_size
                self.ball.dy = -self.ball.dy
                self.music_channel.play(self.sounds_list['wall_hit'])

            # If x < 0 mean out of screen
            if self.ball.rect.x < 0:
                self._SwitchPlayer(1)
                self.player2_score +=1
                self.music_channel.play(self.sounds_list['score'])

                if(self.mode == "extreme"):

                    text = random.choice([
                        "You are cheating",
                        "Impossible",
                        "That is unfair",
                        "I just give it to you",
                        "Don't be ridiculous",
                        "Hacking detected"
                    ])

                    tts_path = os.path.join(dirname,"sounds/output.mp3")
                    tts = gTTS(text)
                    tts.save(tts_path)

                    sound = mixer.Sound(tts_path)      
                    self.music_channel.play(sound)

                if self.player2_score == WINNING_SCORE:
                    self._WinningPlayer(2)
                    self.game_state = 'done'
                else:
                    self.game_state = 'serve'
                    if(self.mode == "easy"):
                        if(self.player2_score >= 0):
                            self.mode = "hard"

                    elif(self.mode == "hard"):
                        if(self.player2_score >= 0):
                            self.mode = "extreme"
                            mixer.music.set_volume(0.1)

                    self.ball.Reset()

            # If x > width mean out of screen
            if self.ball.rect.x > WIDTH:
                self._SwitchPlayer(2)
                self.player1_score += 1
                self.music_channel.play(self.sounds_list['score'])

                if(self.mode == "extreme"):
                    text = random.choice([
                        "Too easy",
                        "You are so easy.",
                        "You are chicken.",
                        "You are no matched for me",
                        "Give me harder"
                    ])

                    tts_path = os.path.join(dirname,"sounds/output.mp3")
                    tts = gTTS(text)
                    tts.save(tts_path)

                    sound = mixer.Sound(tts_path)      
                    self.music_channel.play(sound)

                if self.player1_score == WINNING_SCORE:
                    self._WinningPlayer(1)
                    self.game_state = 'done'
                    
                else:
                    self.game_state = 'serve'
                    self.ball.Reset()

        if self.game_state == 'play':
            self.ball.update(dt)

        self.player1.update(dt)
        self.player2.update(dt)

    def process_input(self):
        #one time input
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == 'start':
                        self.game_state = 'serve'
                    elif self.game_state == 'serve':
                        self.game_state = 'play'
                    elif self.game_state == 'done':

                        self.game_state = 'start'
                        self.ball.Reset()

                        #reset score
                        self.player1_score = 0
                        self.player2_score = 0

                        if self.winning_player == 1:
                            self._SwitchPlayer(2)
                        else:
                            self._SwitchPlayer(1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                self.mouse_click = True

        #continuous input
        key = pygame.key.get_pressed()

        if(self.mode == "multiplayer"):
            if key[pygame.K_w]:
                if(key[pygame.K_a]):
                    self.player1.rect.y-=10
                    self.music_channel.play(self.sounds_list['score'])
                else:
                    self.player1.dy = -PADDLE_SPEED
            elif key[pygame.K_s]:
                if(key[pygame.K_a]):
                    self.player1.rect.y+=10
                    self.music_channel.play(self.sounds_list['score'])
                else:
                    self.player1.dy = PADDLE_SPEED
            else:
                self.player1.dy = 0

        if key[pygame.K_UP]:
            if(key[pygame.K_RIGHT]):
                self.player2.rect.y-=10
                self.music_channel.play(self.sounds_list['score'])
            else:
                self.player2.dy = -PADDLE_SPEED
        elif key[pygame.K_DOWN]:
            if(key[pygame.K_RIGHT]):
                self.player2.rect.y+=10
                self.music_channel.play(self.sounds_list['score'])
            else:
                self.player2.dy = PADDLE_SPEED

        else:
            self.player2.dy = 0

    def _SwitchPlayer(self, player_number):
        self.serving_player = player_number
        self.t_player_turn = self.small_font.render("player" + str(player_number) + "'s serve!", False, (0,0,0))

    def _WinningPlayer(self, player_number):
        self.winning_player = player_number
        self.t_player_win = self.large_font.render("player" + str(player_number) + "'s wins!", False, (0,0,0))


    def draw(self):
        self.screen.blit(background_image, (0, 0))

        if self.game_state == "start":
            text_rect = self.t_welcome.get_rect(center=(WIDTH/2, 20))
            self.screen.blit(self.t_welcome, text_rect)
            text_rect = self.t_press_enter_begin.get_rect(center=(WIDTH / 2, 40))
            self.screen.blit(self.t_press_enter_begin, text_rect)

            text_rect = self.t_ball_size_display.get_rect(center=((WIDTH / 2), HEIGHT-40))
            self.screen.blit(self.t_ball_size_display,text_rect)

            text_rect = self.t_add_ball_size.get_rect(center=((WIDTH / 2)+100, HEIGHT-40))
            self.screen.blit(self.t_add_ball_size,text_rect)
            
            text_rect = self.t_remove_ball_size.get_rect(center=((WIDTH / 2)-100, HEIGHT-40))
            self.screen.blit(self.t_remove_ball_size,text_rect)

            text_rect = self.t_easy.get_rect(center=((WIDTH / 2)-577, HEIGHT-40))
            self.screen.blit(self.t_easy,text_rect)

            text_rect = self.t_hard.get_rect(center=((WIDTH / 2)-477, HEIGHT-40))
            self.screen.blit(self.t_hard,text_rect)

            text_rect = self.t_extreme.get_rect(center=((WIDTH / 2)-350, HEIGHT-40))
            self.screen.blit(self.t_extreme,text_rect)

            text_rect = self.t_multiplayer.get_rect(center=((WIDTH / 2)-200, HEIGHT-40))
            self.screen.blit(self.t_multiplayer,text_rect)

            if self.mouse_click:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                text_rect_add = self.t_add_ball_size.get_rect(center=((WIDTH / 2)+100, HEIGHT-40))
                text_rect_remove = self.t_remove_ball_size.get_rect(center=((WIDTH / 2)-100, HEIGHT-40))
                text_rect = self.t_ball_size_display.get_rect(center=((WIDTH / 2), HEIGHT-40))

                text_rect_easy = self.t_easy.get_rect(center=((WIDTH / 2)-577, HEIGHT-40))
                text_rect_hard = self.t_hard.get_rect(center=((WIDTH / 2)-477, HEIGHT-40))
                text_rect_extreme = self.t_extreme.get_rect(center=((WIDTH / 2)-350, HEIGHT-40))
                text_rect_multiplayer = self.t_multiplayer.get_rect(center=((WIDTH / 2)-200, HEIGHT-40))
            

                if text_rect_add.collidepoint(mouse_x, mouse_y):
                    # Handle the click event for this specific text
                    if(self.ball_size != 100):
                        self.ball_size+=1
                    else:
                        self.ball_size = 100

                elif text_rect_remove.collidepoint(mouse_x,mouse_y):
                    if(self.ball_size != 10):
                        self.ball_size-=1
                    else:
                        self.ball_size = 10

                elif text_rect_easy.collidepoint(mouse_x,mouse_y):
                    self.t_easy = self.small_font.render(f"Easy",False,(255,0,0))
                    self.t_hard = self.small_font.render(f"Hard",False,(0,0,0))
                    self.t_extreme = self.small_font.render(f"Extreme",False,(0,0,0))
                    self.t_multiplayer = self.small_font.render(f"Multiplayer",False,(0,0,0))
                    self.mode = "easy"
                    mixer.music.set_volume(0)

                elif text_rect_hard.collidepoint(mouse_x,mouse_y):
                    self.t_easy = self.small_font.render(f"Easy",False,(0,0,0))
                    self.t_hard = self.small_font.render(f"Hard",False,(255,0,0))
                    self.t_extreme = self.small_font.render(f"Extreme",False,(0,0,0))
                    self.t_multiplayer = self.small_font.render(f"Multiplayer",False,(0,0,0))
                    self.mode = "hard"
                    mixer.music.set_volume(0)

                elif text_rect_extreme.collidepoint(mouse_x,mouse_y):
                    self.t_easy = self.small_font.render(f"Easy",False,(0,0,0))
                    self.t_hard = self.small_font.render(f"Hard",False,(0,0,0))
                    self.t_extreme = self.small_font.render(f"Extreme",False,(255,0,0))
                    self.t_multiplayer = self.small_font.render(f"Multiplayer",False,(0,0,0))
                    self.mode = "extreme"
                    mixer.music.set_volume(0.1)
                    
                elif text_rect_multiplayer.collidepoint(mouse_x,mouse_y):
                    self.t_easy = self.small_font.render(f"Easy",False,(0,0,0))
                    self.t_hard = self.small_font.render(f"Hard",False,(0,0,0))
                    self.t_extreme = self.small_font.render(f"Extreme",False,(0,0,0))
                    self.t_multiplayer = self.small_font.render(f"Multiplayer",False,(255,0,0))
                    self.mode = "multiplayer"
                    mixer.music.set_volume(0)

                self.screen.blit(self.t_easy,text_rect_easy)
                self.screen.blit(self.t_hard,text_rect_hard)
                self.screen.blit(self.t_extreme,text_rect_extreme)
                self.screen.blit(self.t_multiplayer,text_rect_multiplayer)

                self.screen.blit(self.t_ball_size_display,text_rect)
                self.t_ball_size_display = self.small_font.render(f"Ball Size: {self.ball_size}",False,(0,0,0))

                del self.ball
                self.ball = Ball(self.screen, WIDTH / 2 - self.ball_size/2, HEIGHT / 2 - self.ball_size/2, self.ball_size, self.ball_size, WIDTH, HEIGHT)

                self.ball.render()
                self.mouse_click = False

        elif self.game_state == "serve":
            text_rect = self.t_player_turn.get_rect(center=(WIDTH / 2, 20))
            self.screen.blit(self.t_player_turn, text_rect)
            text_rect = self.t_press_enter_serve.get_rect(center=(WIDTH / 2, 40))
            self.screen.blit(self.t_press_enter_serve, text_rect)
        
        elif self.game_state == "play":
            pass

        elif self.game_state == "done":
            text_rect = self.t_player_win.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(self.t_player_win, text_rect)
            text_rect = self.t_press_restart.get_rect(center=(WIDTH / 2, 70))
            self.screen.blit(self.t_press_restart, text_rect)
            self.t_easy = self.small_font.render(f"Easy",False,(255,0,0))
            self.t_hard = self.small_font.render(f"Hard",False,(0,0,0))
            self.t_extreme = self.small_font.render(f"Extreme",False,(0,0,0))
            self.t_multiplayer = self.small_font.render(f"Multiplayer",False,(0,0,0))
            self.mode = "easy"
            self.player1.render((0,255,0))
            mixer.music.set_volume(0)

        self.DisplayScore()

        self.ball.render()
        if(self.mode == "extreme"):
            self.player1.render(random.choice(self.color_choice))

        elif(self.mode == "easy"):
            self.player1.render((0,255,0))

        elif(self.mode == "hard"):
            self.player1.render((255,0,0))

        else:
            self.player1.render((255,255,255))

        self.player2.render((255,255,255))
        

    def DisplayScore(self):
        self.t_p1_score = self.score_font.render(str(self.player1_score), False, (0,0,0))
        self.t_p2_score = self.score_font.render(str(self.player2_score), False, (0,0,0))
        self.screen.blit(self.t_p1_score, (WIDTH/2 - 90, HEIGHT/2-40))
        self.screen.blit(self.t_p2_score, (WIDTH / 2 + 35, HEIGHT/2-40))



if __name__ == '__main__':
    main = GameMain()

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption("Pong game running with {:d} FPS".format(int(clock.get_fps())))

        # elapsed time from the last call
        dt = clock.tick(main.max_frame_rate)/1000.0

        main.process_input()
        main.update(dt)
        main.draw()

        pygame.display.update()

