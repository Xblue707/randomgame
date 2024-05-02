import pygame, os, time
from pygame.locals import *
from pygame import mixer
from win32api import GetSystemMetrics

wmul = GetSystemMetrics(0)/1920
hmul = GetSystemMetrics(1)/1080
print(wmul,hmul)


class button:
    def __init__(self, x, y, c1, c2, key):
        self.x = x
        self.y = y
        self.c1 = c1
        self.c2 = c2
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, 500*wmul, 50*hmul)
        self.handled = False


class maps:
    def __init__(self, directory):
        self.directory = directory
        file = open(directory + "/MAP_INFO.txt", "r")
        self.name = file.readline().strip("\n")[6:]
        self.bpm = file.readline().strip("\n")[5:]
        self.artist = file.readline().strip("\n")[8:]
        self.col = (0, 0, 0, 128)
        self.disp = pygame.Rect(25, 25, 1000*wmul, 250*hmul)


# PYGAME INIT HERE
# PYGAME INIT HERE
# PYGAME INIT HERE

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screen.fill((128, 128, 128))

mixer.init()

buttons = [
    button(300*wmul, 900*hmul, (0, 0, 255), (0, 0, 0), pygame.K_LSHIFT),
    button(1000*wmul, 900*hmul, (255, 0, 0), (0, 0, 0), pygame.K_RSHIFT),
    button(300*wmul, 850*hmul, (0, 0, 192), (64, 64, 64), pygame.K_LSHIFT),
    button(1000*wmul, 850*hmul, (192, 0, 0), (64, 64, 64), pygame.K_RSHIFT),
    button(300*wmul, 950*hmul, (0, 0, 192), (64, 64, 64), pygame.K_LSHIFT),
    button(1000*wmul, 950*hmul, (192, 0, 0), (64, 64, 64), pygame.K_RSHIFT),
]

mapss = []

maps_list = os.listdir("C:/Users/Administrator/Documents/GitHub/randomgame/some game/maps")

for m in maps_list:
    directory = "C:/Users/Administrator/Documents/GitHub/randomgame/some game/maps/" + m
    mapss.append(maps(directory))

map_index = 0

# song_dir = mapss[map_index].directory + "/chart_music.mp3"
# mixer.music.set_volume(3)
# mixer.music.load("./maps/anoyo/chart_music.mp3")
# mixer.music.play()

# REAL STUFF
# REAL STUFF
# REAL STUFF

played = 0
state = 0
f = open("C:/Users/Administrator/Documents/GitHub/randomgame/some game/settings.txt")
settings = f.read().split()
scroll_speed = int(settings[0])
offset = int(settings[1])
combo_count = 0

state_reference = {0: "song selection", 1: "playing", 2: "options"}


while True:
    # leaving the game
    clock.tick()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            # updating map_index
        if event.type == KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                map_index -= 1
                played = 0
                map_index %= len(mapss)
            if event.key == pygame.K_RSHIFT:
                map_index += 1
                played = 0
                map_index %= len(mapss)
            if event.key == pygame.K_RETURN and state == 0:
                state = 1
                screen.fill((128, 128, 128))
            if event.key == pygame.K_ESCAPE and state == 0:
                state = 2
            if event.key == pygame.K_g and state == 0:
                state = 3

    if state == 0:

        screen.fill((128, 128, 128))

        # displaying the maps
        bg_dir = mapss[map_index].directory + "/song_bg.png"
        bg = pygame.image.load(bg_dir)
        bg = pygame.transform.scale(bg,(1280*wmul,720*hmul))
        screen.blit(bg, (0, 0))
        shape_surf = pygame.Surface(mapss[map_index].disp.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, mapss[map_index].col, shape_surf.get_rect())
        screen.blit(shape_surf, mapss[map_index].disp)
        my_font = pygame.font.SysFont("Microsoft Jhenghei UI", int(60*hmul))
        text_surface = my_font.render(mapss[map_index].name, False, (255, 255, 255))
        screen.blit(text_surface, (50*hmul, 30*wmul))
        text_surface = my_font.render(
            "BPM: " + mapss[map_index].bpm, False, (255, 255, 255)
        )
        screen.blit(text_surface, (50*hmul, 100*wmul))
        text_surface = my_font.render(
            "Artist: " + mapss[map_index].artist, False, (255, 255, 255)
        )
        screen.blit(text_surface, (50*hmul, 170*wmul))
        my_font = pygame.font.SysFont("Microsoft Jhenghei UI", 15)
        text_surface = my_font.render(str(int(clock.get_fps())), False, (255, 255, 255))
        screen.blit(text_surface, (0, 0))
        if played == 0:
            song_dir = mapss[map_index].directory + "/chart_music.mp3"
            mixer.music.load(song_dir)
            mixer.music.set_volume(3)
            mixer.music.play()
            played = 1

        # displaying 2 buttons
        bb = pygame.key.get_pressed()
        for key in buttons:
            if bb[key.key]:
                pygame.draw.rect(screen, key.c1, key.rect)
            else:
                pygame.draw.rect(screen, key.c2, key.rect)

    elif state == 1:
        screen.fill((128, 128, 128))

        # reading the chart
        notes = []
        chart_dir = mapss[map_index].directory + "/chart.txt"
        f = open(chart_dir, "r")
        data = f.readlines()
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == "1":
                    notes.append(
                        pygame.Rect(
                            buttons[x].rect.x,
                            y * -(scroll_speed / 50 * 100)
                            - offset * 10
                            + buttons[x].rect.y,
                            500*wmul,
                            25*hmul,
                        )
                    )
        # initialize songs and stuff
        mixer.music.stop()
        song_dir = mapss[map_index].directory + "/chart_music.mp3"
        mixer.music.load(song_dir)
        mixer.music.set_volume(3)
        mixer.music.play()

        # beat stuff (useless for now im too skill issue to code this)
        # bpm = int(mapss[map_index].bpm)
        # one_beat = 60 / bpm
        # two_beat = one_beat * 2
        # four_beat = one_beat * 4
        # half_beat = one_beat / 2
        # quarter_beat = one_beat / 4
        # eigth_beat = one_beat / 8
        # sixteenth_beat = one_beat / 16
        # third_beat = one_beat / 3

        # testing purposes
        col = [(0, 0, 255), (255, 0, 0)]
        col_ind = 0

        stop = 0

        combo_count = 0

        while True:
            clock.tick(60)
            screen.fill((128, 128, 128))
            my_font = pygame.font.SysFont("Microsoft Jhenghei UI", 15)
            text_surface = my_font.render(
                str(int(clock.get_fps())), False, (255, 255, 255)
            )
            screen.blit(text_surface, (0, 0))
            my_font = pygame.font.SysFont("Microsoft Jhenghei UI", int(80*hmul))
            text_surface = my_font.render(str(combo_count), False, (255, 255, 255))
            screen.blit(text_surface, (900*wmul, 300*hmul))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        stop = 1
            if stop == 1:
                state = 0
                mixer.music.stop()
                played = 0
                break

            bb = pygame.key.get_pressed()
            for key in buttons:
                if bb[key.key]:
                    pygame.draw.rect(screen, key.c1, key.rect)
                    key.handled = False
                else:
                    pygame.draw.rect(screen, key.c2, key.rect)
                    key.handled = True

            for note in notes:
                pygame.draw.rect(screen, col[note.x > 500], note)
                note.y += scroll_speed
                for b in buttons:
                    if b.rect.colliderect(note) and not b.handled:
                        notes.remove(note)
                        b.handled = True
                        combo_count += 1
                        break
                    if note.y > 1100*hmul:
                        notes.remove(note)
                        combo_count = 0
                        break

            pygame.display.update()
    elif state == 2:
        stopstop = False
        selected = [(255, 0, 0), (255, 255, 255)]
        select_index = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 0
                        stopstop = True
                        break
                    if event.key == pygame.K_UP:
                        selected[select_index] = (255, 255, 255)
                        select_index += 1
                        select_index %= len(selected)
                        selected[select_index] = (255, 0, 0)
                    if event.key == pygame.K_DOWN:
                        selected[select_index] = (255, 255, 255)
                        select_index -= 1
                        select_index %= len(selected)
                        selected[select_index] = (255, 0, 0)
                    if event.key == pygame.K_LEFT:
                        if select_index == 0:
                            scroll_speed -= 1
                            if scroll_speed < 0:
                                scroll_speed = 0
                        elif select_index == 1:
                            offset -= 1
                    if event.key == pygame.K_RIGHT:
                        if select_index == 0:
                            scroll_speed += 1
                        elif select_index == 1:
                            offset += 1
            if stopstop:
                f = open("C:/Users/Administrator/Documents/GitHub/randomgame/some game/settings.txt", "w")
                s = [scroll_speed,offset]
                txt = ""
                for elem in s:
                    txt+=str(elem)+"\n"
                f.write(txt)
                f.close()
                break
            screen.fill((128, 128, 128))
            my_font = pygame.font.SysFont("Microsoft Jhenghei UI", 50)
            text_surface = my_font.render(
                "Scroll speed: " + str(scroll_speed), False, selected[0]
            )
            screen.blit(text_surface, (100*wmul, 100*hmul))
            text_surface = my_font.render("Offset: " + str(offset), False, selected[1])
            screen.blit(text_surface, (100*wmul, 200*hmul))
            pygame.display.update()

    else:
        chart_dir = mapss[map_index].directory + "/chart.txt"
        f = open(chart_dir, "w")
        res = ""
        screen.fill((128, 128, 128))
        mixer.music.stop()
        song_dir = mapss[map_index].directory + "/chart_music.mp3"
        mixer.music.load(song_dir)
        mixer.music.set_volume(3)
        mixer.music.play()
        pygame.display.update()
        stop = 0
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        stop = 1
                    if event.key == pygame.K_LSHIFT:
                        res += "1"
                    else:
                        res += "0"
                    if event.key == pygame.K_RSHIFT:
                        res += "1"
                    else:
                        res += "0"
                    res += "\n"
                else:
                    res += "00\n"

            if stop == 1:
                state = 0
                mixer.music.stop()
                played = 0
                break

            pygame.display.update()
        f.write(res)
        state = 0

    pygame.display.update()
