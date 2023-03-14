import pygame
from sys import exit
from random import randint, choice, uniform

game_status = True
winner = None
red_score, green_score = 0, 0

class Paddle(pygame.sprite.Sprite):
    def __init__(self, center_pos, player, **kwargs):
        super().__init__(**kwargs)

        random = randint(1, 5)
        paddle_surf = pygame.image.load(f'items/paddle_{random}.png')
        paddle_surf = pygame.transform.rotozoom(paddle_surf, 90, 0.5)
        
        self.player = player
        self.center_pos = center_pos
        self.image = paddle_surf
        self.rect = self.image.get_rect(center= (self.center_pos , 300))
    
    def player_input(self):
        keys = pygame.key.get_pressed()

        if self.player == 'red':
            if keys[pygame.K_UP] and self.rect.midtop[1] > 0: self.rect.y -= 4
            elif keys[pygame.K_DOWN] and self.rect.midbottom[1] < 612: self.rect.y += 4
        else:
            if keys[pygame.K_w] and self.rect.midtop[1] > 0: self.rect.y -= 4
            elif keys[pygame.K_s] and self.rect.midbottom[1] < 612: self.rect.y += 4

    def update(self):
            self.player_input()

class Ball(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        random = randint(1, 2)
        ball_surf = pygame.image.load(f'items/ball_{random}.png')
        ball_surf = pygame.transform.rotozoom(ball_surf, 0, 0.12)
        
        self.range_choice = choice([(-2, -1), (1, 2)])
        
        self.x_multiplier = choice([6, -6]) 
        self.y_multiplier = round(uniform(self.range_choice[0], self.range_choice[1]), 2)
        self.image = ball_surf
        self.rect = self.image.get_rect(center= (306 , 306))
    
    def update(self):
        self.rect.x += self.x_multiplier
        self.rect.y += self.y_multiplier

        self.get_win()

    def get_win(self):
        global game_status, winner, green_score, red_score
        
        if (pygame.sprite.spritecollide(red_paddle.sprite, ball, False) or (pygame.sprite.spritecollide(green_paddle.sprite, ball, False))):
            self.x_multiplier *= -1
            self.y_multiplier = round(uniform(self.range_choice[0], self.range_choice[1]), 2) * randint(-1, 1)
            pong.play()
        
        if (self.rect.center[1] <5 or self.rect.center[1] >608):
            self.y_multiplier *= -1
            pong.play()

        if self.rect.center[0] <10 or self.rect.center[0] >600:
            if self.rect.center[0] <10: green_score +=1
            if self.rect.center[0] >600: red_score +=1
            bop.play()
            
            self.kill()
            green_paddle.sprite.rect.center = (20, 300)
            red_paddle.sprite.rect.center = (590, 300)
            ball.add(Ball())


def get_timer():
    current_time = (pygame.time.get_ticks() - start_time) // 1000 # convert to seconds
    minutes, seconds = divmod(current_time, 60)
    time_str = f"{minutes:02d}:{seconds:02d}" # format as "mm:ss"
    time_sur = font.render(time_str, False, (255, 255, 255))
    time_rec = time_sur.get_rect(center=(300, 30))
    screen.blit(time_sur, time_rec)


pygame.init()

####
start_time = 0

screen = pygame.display.set_mode((612,612))
pygame.display.set_caption('Ping Pong')
icon = pygame.image.load('background/icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

background_surf = pygame.image.load('background/background.jpg').convert()
background_surf = pygame.transform.rotozoom(background_surf, 90, 1)

#creating objects
green_paddle = pygame.sprite.GroupSingle()
green_paddle.add(Paddle(center_pos=20, player='green'))
red_paddle = pygame.sprite.GroupSingle()
red_paddle.add(Paddle(center_pos=590, player='red'))
ball = pygame.sprite.Group()
ball.add(Ball())

#sounds
bg_music = pygame.mixer.Sound(f"audio/bg_{choice([1,2,3])}.mp3")
bg_music.set_volume(0.3)
bg_music.play(loops = -1)
end = pygame.mixer.Sound("audio/end.ogg")
end.set_volume(0.2)
bop = pygame.mixer.Sound("audio/bop.wav")
bop.set_volume(0.2)
pong = pygame.mixer.Sound(f"audio/pong_{choice([1,2,3])}.wav")
pong.set_volume(0.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    if game_status:
        
        screen.blit(background_surf, (0, 0))
        get_timer()


        green_paddle.draw(screen)
        green_paddle.update()
        red_paddle.draw(screen)
        red_paddle.update()
        ball.draw(screen)
        ball.update()

        red_score_surf = font.render(f'{red_score}', False, (255, 0, 0))
        red_score_rect = red_score_surf.get_rect(center = (50, 30))  
        green_score_surf = font.render(f'{green_score}', False, (0, 255, 0))
        green_score_rect = green_score_surf.get_rect(center = (550, 30)) 
        
        screen.blit(red_score_surf, red_score_rect)
        screen.blit(green_score_surf, green_score_rect)
        

        if red_score ==10 or green_score==10:
            winner = 'RED' if red_score ==10 else 'GREEN'
            bg_music.set_volume(0)
            end.play()
        
            game_status = False
    else:
        # Initialize the surface (gameover)
        gameover_sur = pygame.image.load('background/background.jpg').convert()
        font_over = pygame.font.Font('fonts/Pixeltype.ttf', 100)
        font_choices = pygame.font.Font('fonts/Pixeltype.ttf', 60)

        # game over texts
        textover_sur = font_over.render(f'WINNER: {winner}', False, (255, 255, 255))
        textover_rec = textover_sur.get_rect(center = (310, 220))

        restart_sur = font_choices.render('RESTART', False, (64, 45, 75))
        restart_rec = restart_sur.get_rect(center = (310, 270))

        yes_sur = font_choices.render('YES', False, (0, 255, 0))
        yes_rec = yes_sur.get_rect(center = (250, 320))
        
        no_sur = font_choices.render('NO', False, (255, 0, 0))
        no_rec = no_sur.get_rect(center = (360, 320))
        
        # Display
        screen.blit(gameover_sur, (0, 0))
        screen.blit(textover_sur, textover_rec)
        screen.blit(restart_sur, restart_rec)
        screen.blit(yes_sur, yes_rec)
        screen.blit(no_sur, no_rec)

        if event.type == pygame.MOUSEBUTTONDOWN and yes_rec.collidepoint(event.pos):
            game_status = True
            green_paddle.sprite.rect.center = (20, 300)
            red_paddle.sprite.rect.center = (590, 300)
            red_score, green_score =0, 0
            bg_music.set_volume(0.2)



        start_time = pygame.time.get_ticks()
        
        if event.type == pygame.MOUSEBUTTONDOWN and no_rec.collidepoint(event.pos):
            pygame.quit()
            exit()


    pygame.display.update()
    clock.tick(60)

