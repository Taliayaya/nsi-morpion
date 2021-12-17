import pygame

surf = pygame.display.set_mode((900, 900))
run = True
while run:
    pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(0, 0, 300, 300))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("vous avez appuyé sur la touche espace")
            elif event.key == pygame.K_a:
                print("vous avez appuyé sur la touche A")
            elif event.key == pygame.K_RETURN:
                print("vous avez appuyé sur la touche Entrée")
            else:
                print("vous avez appuyé sur une touche")
    pygame.display.flip()
pygame.quit()
