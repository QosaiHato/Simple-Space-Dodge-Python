import pygame
import time
import random


pygame.font.init()


WIDTH, HEIGHT = 1000, 800


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Dodge')

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))


PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5


STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars, hit_count, hit_positions):
    """Render the game elements on the screen."""
   
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

 
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    for pos in hit_positions:
        pygame.draw.circle(WIN, "blue", pos, 15)  

    hit_text = FONT.render(f"Hits: {hit_count}", 1, "white")
    WIN.blit(hit_text, (10, 50))
    
  
    pygame.display.update()

def main():
    run = True

 
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)


    clock = pygame.time.Clock()

  
    start_time = time.time()  
    elapsed_time = 0  


    star_add_increment = 2000  
    star_count = 0 
    stars = []  


    hit_count = 0
    hit_positions = {}  

    while run:
     
        star_count += clock.tick(60)  

      
        elapsed_time = time.time() - start_time

      
        if star_count > star_add_increment:
            for _ in range(3):  
                star_x = random.randint(0, WIDTH - STAR_WIDTH)  
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)  
                stars.append(star)  

           
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False
                break

        keys = pygame.key.get_pressed()  

     
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
    
        if keys[pygame.K_d] and player.x + PLAYER_WIDTH + PLAYER_VEL <= WIDTH:
            player.x += PLAYER_VEL
       
        if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
       
        if keys[pygame.K_s] and player.y + PLAYER_HEIGHT + PLAYER_VEL <= HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:  
            star.y += STAR_VEL  

           
            if star.y > HEIGHT:
                stars.remove(star)
        
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star) 
                hit_count += 1
               
                hit_positions[(star.x + STAR_WIDTH // 2, star.y + STAR_HEIGHT // 2)] = time.time()
                break

        current_time = time.time()
       
        hit_positions = {pos: timestamp for pos, timestamp in hit_positions.items() if current_time - timestamp < 0.007}  

      
        draw(player, elapsed_time, stars, hit_count, hit_positions)


    pygame.quit()

if __name__ == "__main__":
    main()
