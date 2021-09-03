import pygame
from time import sleep
from random import randint

score = 0
High_Score=score
hearts_left = 3

green=(0,255,0)
red=(255,0,0)
black=(5,5,5)
white=(255,255,255)
yellow=(255,255,0)
brick_green=(0, 128, 78)
brick_yellow=(255,215,0)
brick_red=(128, 30, 30)
dark_green = (0, 50, 32)
dark_yellow=(60, 40, 0)
dark_red=(55,0,0)


pygame.init()
dis=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, length = pygame.display.get_surface().get_size()
pygame.display.update()
pygame.display.set_caption('bricks')

def Your_score(score, hearts_left):
    score_font = pygame.font.SysFont("comicsansms", 35)
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [20, 0])
    hearts_font = pygame.font.SysFont("comicsansms", 35)
    value = hearts_font.render("Hearts: " + str(hearts_left), True, yellow)
    dis.blit(value, [width-200, 0])
    #score_font = pygame.font.SysFont("comicsansms", 35)
    #value = score_font.render("Your High Score: " + str(HighScore), True, yellow)
    #dis.blit(value, [width-350, 0])

def message(msg, color, size1=100, hight=length/4):
    pygame.font.init()
    behind=len(msg)
    font_style = pygame.font.SysFont(None, size1)
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [int(width/2-size1*behind/6),hight])
    pygame.display.update()

def draw_platform(platform_list):
    rect = pygame.Rect(platform_list[0], platform_list[1], 200, 30)
    pygame.draw.rect(dis, white, rect)

def draw_ball(Ball):
    pygame.draw.circle(dis, white, [Ball[0], Ball[1]], 7)

def draw_brick(brick):
    size = brick[1]-brick[0]
    pygame.draw.rect(dis, brick[4], [brick[0], brick[2], size, 32])
    pygame.draw.rect(dis, brick[5], [brick[0]+size/10, brick[2]+5, (size*4)/5, 22])
    pygame.draw.line(dis, brick[5], (brick[0], brick[2]), (brick[0]+size/10, brick[2]+5))
    pygame.draw.line(dis, brick[5], (brick[1], brick[2]), (brick[1]-size/10, brick[2]+5))
    pygame.draw.line(dis, brick[5], (brick[0], brick[3]), (brick[0]+size/10, brick[3]-5))
    pygame.draw.line(dis, brick[5], (brick[1], brick[3]), (brick[1]-size/10, brick[3]-5))

def Generate_Bricks(level):
    bricks = []
    x=0
    y=-32
    line=0
    num_of_lines = 7
    while line < num_of_lines:
        x=0
        num_of_brick=0
        line+=1
        y+=33
        num_of_bricks=9

        while num_of_brick < num_of_bricks:
            x1 = x-1
            x2 = x1+width/num_of_bricks-3
            y1 = length/9+y
            y2 = y1+32
            if line+7<level:
                resistance = brick_red
                dark = dark_red
            elif line<level:
                resistance = brick_yellow
                dark = dark_yellow
            else:
                resistance = brick_green
                dark = dark_green
            brick_xy = [int(x1), int(x2), int(y1), int(y2), resistance, dark]
            x+=width/num_of_bricks
            num_of_brick+=1
            bricks.append(brick_xy)

    return bricks

def Level_Finished(num_of_bricks, level):
    if num_of_bricks <= 0:
        message("You finished level " + str(level), green)
        sleep(1.5)
        dis.fill(black)
        message("Now entering level " + str(level+1), yellow, size1=50)
        sleep(0.35)
        dis.fill(black)
        message("Now entering level " + str(level+1)+'.', yellow, size1=50)
        sleep(0.35)
        dis.fill(black)
        message("Now entering level " + str(level+1)+'..', yellow, size1=50)
        sleep(0.35)
        dis.fill(black)
        return True
    return False

def actual_game(highest, hearts, lvl, current_score=0, bricks=False):
    if not bricks:
        bricks = Generate_Bricks(lvl)
    game_over=False
    game_close=False


    pad_x1=width/2-100
    pad_x2=pad_x1+100
    pad_y1=length-50
    pad_y2=pad_y1+30

    Ball = [width/2, length-150]
    Ball_x_change = 0.0
    Ball_y_change = 1

    x1_change = 0
    clock = pygame.time.Clock()
    game_speed=300
    lose=0
    while not game_close:
        once = 0
        while game_over:
            if once == 0:
                if lose==1:
                    dis.fill(black)
                    message("You Lose!", red, 115)
                    message("Press Esc-Quit or Enter-Play Again", red, 35, length-50)
                    message("your score was: " + str(current_score), yellow, 50, length/2)
                if lose==0:
                    message("Press Esc-Quit or Enter-Play Again or Space-continue", red, 35, length-50)
                    message("your score is: " + str(current_score), yellow, 60, length/2)
                once = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = True
                    game_over=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_close = True
                        game_over=False
                    if event.key == pygame.K_SPACE:
                        game_over= False
                    if event.key == pygame.K_RETURN:
                        actual_game(highest, hearts_left, 1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over=True
                if event.key == pygame.K_LEFT:
                    x1_change = -0.9
                if event.key == pygame.K_RIGHT:
                    x1_change = 0.9


        for brick in bricks:
            if brick:
                draw_brick(brick)
        
        Ball[0] += Ball_x_change
        Ball[1] += Ball_y_change

        if pad_x2+100 >= width:
            x1_change=0
            pad_x2-=5
            pad_x1-=5
        if pad_x1 <=0:
            x1_change=0
            pad_x2+=5
            pad_x1+=5

        if Ball[0] >= width-5 or Ball[0] < 5:
            Ball_x_change *= -1

        if Ball[1] >= length:
            dis.fill(black)
            hearts -= 1
            message("-1 heart", red)
            message("you have " + str(hearts) + " hearts left!", red, hight=length/4+100, size1=60)
            sleep(2)
            actual_game(highest, hearts, 1, current_score, bricks)
        if hearts == 0:
            game_over = True
            lose = 1

        if Ball[1] > length - 100:
            if (Ball[0] >= pad_x1-10 and Ball[0] <= pad_x2+100) and Ball[1] == pad_y1:
                Ball_y_change = Ball_y_change * -1
                Ball[1] -= 10
                hit = (Ball[0]-(pad_x1+100))/100
                if hit > 0.3:
                    hit -= 0.2 if hit<0.6 else 0.25
                elif hit < -0.3:
                    hit += 0.2 if hit>-0.6 else 0.25
                if 0.3 > hit > -0.3:
                    hit = Ball_x_change/2
                if hit == 0:
                    hit = -0.1 if randint(0,1) == 0 else 0.1
                New_Ball_x_change= hit
                if Ball_x_change < 0:
                    New_Ball_x_change += 0.2
                    if New_Ball_x_change > 0:
                        New_Ball_x_change -= Ball_x_change/3 
                if Ball_x_change > 0:
                    New_Ball_x_change -= 0.2
                    if New_Ball_x_change < 0:
                        New_Ball_x_change += Ball_x_change/3
                New_Ball_x_change -=  New_Ball_x_change%0.1
                Ball_x_change = int((New_Ball_x_change*10))/10
                print(Ball_x_change)

            
            if ((Ball[0] >= pad_x1-5 and Ball[0] <= pad_x1+5) or (Ball[0] >= pad_x2+95 and Ball[0] <= pad_x2+105)) and (Ball[1] >= pad_y1 and Ball[1] <= pad_y1+10):
                Ball_x_change = (Ball[0]-(pad_x1+100))/100
                Ball_y_change *= -1

            if ((Ball[0] >= pad_x1-5 and Ball[0] <= pad_x1+5) or (Ball[0] >= pad_x2+95 and Ball[0] <= pad_x2+105)) and (Ball[1] > pad_y1+10):
                Ball_x_change *= -1

        if Ball[1] < 0:
            Ball_y_change = 1
            if Ball_x_change < 0 and Ball_x_change > -1.3:
                if randint(0, 2) == 1:
                    Ball_x_change += 0.3
                Ball_x_change -= 0.2
            elif Ball_x_change > 0 and Ball_x_change < 1.3:
                if randint(0, 2) == 1:
                    Ball_x_change -= 0.3
                Ball_x_change += 0.2
                
        if Ball[1] <= length/9+(33*7):
            index = 0
            for brick in bricks:
                if (Ball[0] >= brick[0] and Ball[0] <= brick[1]+1): 
                    if (Ball[1] > brick[2] and Ball[1] < brick[3]):
                        if brick[4] == brick_green:
                            del bricks[index]
                        if brick[4] == brick_yellow:
                            brick[4] = brick_green
                            brick[5] = dark_green
                        if brick[4] == brick_red:
                            brick[4] = brick_yellow
                            brick[5] = dark_yellow
                        Ball_x_change *= -1
                        current_score += 100
                    if Ball[1] == brick[2] or Ball[1] == brick[3]:
                        Ball_y_change *= -1
                        current_score += 100
                        if brick[4] == brick_green:
                            del bricks[index]
                        elif brick[4] == brick_yellow:
                            brick[4] = brick_green
                            brick[5] = dark_green
                        else:
                            brick[4] = brick_yellow
                            brick[5] = dark_yellow
                index +=1

        pad_x1 += x1_change
        pad_x2 += x1_change
        Platform = [pad_x1, pad_y1]

        clock.tick(game_speed)

        draw_platform(Platform)
        draw_ball(Ball)
        pygame.display.update()
        dis.fill(black)
        if Level_Finished(len(bricks), lvl):
            lvl += 1
            actual_game(highest, hearts, lvl, current_score)
        Your_score(current_score, hearts)
    pygame.quit()
    quit()

def main():
    actual_game(High_Score, hearts_left, 1)

if __name__ == "__main__":
    main()           
