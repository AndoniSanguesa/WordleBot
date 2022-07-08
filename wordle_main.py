import pygame as pg

done = False

def run_game(screen, game_object):
    pg.init()

    done = False
    clock = pg.time.Clock()

    while not done:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            else:
                game_object.handle_event(event)

        screen.fill((80, 80, 80))
        game_object.draw()

        pg.display.flip()
    