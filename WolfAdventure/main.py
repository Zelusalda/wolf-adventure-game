# -*- coding: utf-8 -*-
import random
import math
from pygame import Rect

WIDTH = 320
HEIGHT = 384
TILE_SIZE = 32

HERO_SPEED = 2
ENEMY_SPEED = 1
ANIMATION_SPEED = 0.10

STATE_MENU = 0
STATE_GAME = 1
STATE_GAMEOVER = 2
STATE_INSTRUCTIONS = 3

COLOR_WALL = (34, 139, 34)
COLOR_FLOOR = (101, 67, 33)
COLOR_UI_BG = (20, 20, 20)
COLOR_HEALTH_BAR = (200, 0, 0)
COLOR_HEALTH_FILL = (0, 200, 0)

game_state = STATE_MENU
current_level = 0
audio_enabled = True
music_playing = False

MAPS = [
    ["##########", "#........#", "#..##....#", "#........#", "#....##..#", "#........#", "#..##....#", "#........#",
     "#........#", "##########"],
    ["##########", "#........#", "#.####...#", "#...#....#", "#..##..#.#", "#........#", "#....##..#", "#.#......#",
     "#........#", "##########"]
]


class Entity:
    def __init__(self, gx, gy, speed):
        self.grid_x, self.grid_y = gx, gy
        self.x, self.y = gx * TILE_SIZE, gy * TILE_SIZE
        self.target_x, self.target_y = self.x, self.y
        self.speed = speed
        self.is_moving = False
        self.is_dead = False
        self.anim_frame = 0
        self.anim_timer = 0

    def update_position(self):
        if self.x < self.target_x:
            self.x = min(self.x + self.speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.speed, self.target_x)
        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)
        if self.x == self.target_x and self.y == self.target_y: self.is_moving = False

    def get_animation_frame(self, frames):
        self.anim_timer += ANIMATION_SPEED
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % len(frames)
        return frames[self.anim_frame]

    def get_rect(self):
        return Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)


class Hero(Entity):
    def __init__(self, gx, gy):
        super().__init__(gx, gy, HERO_SPEED)
        self.walk_sprites = ["hero_walk_1", "hero_walk_2"]
        self.image = self.walk_sprites[0]
        self.health, self.max_health = 5, 5
        self.facing_direction = (0, 1)
        self.invincibility_frames = 0
        self.attack_cooldown = 0
        self.axe_visible, self.axe_pos, self.axe_timer = False, (0, 0), 0

    def move(self, dx, dy):
        if self.is_moving or self.is_dead: return
        nx, ny = self.grid_x + dx, self.grid_y + dy
        if MAPS[current_level][ny][nx] != "#":
            self.facing_direction = (dx, dy)
            self.grid_x, self.grid_y = nx, ny
            self.target_x, self.target_y = nx * TILE_SIZE, ny * TILE_SIZE
            self.is_moving = True

    def update(self):
        if self.is_dead:
            self.image = "hero_dead"
            return
        if self.is_moving: self.update_position()
        self.image = self.get_animation_frame(self.walk_sprites)

        if self.invincibility_frames > 0: self.invincibility_frames -= 1
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        if self.axe_timer > 0:
            self.axe_timer -= 1
        else:
            self.axe_visible = False

    def take_damage(self):
        """Método que lida com o herói recebendo dano."""
        if self.invincibility_frames <= 0 and not self.is_dead:
            self.health -= 1
            self.invincibility_frames = 60
            play_effect("hero_hit")
            if self.health <= 0:
                self.is_dead = True
                play_effect("hero_death")
                music.stop()

    def reset_stats(self):
        self.health = self.max_health
        self.is_dead = False
        self.grid_x, self.grid_y = 1, 1
        self.x = self.target_x = TILE_SIZE
        self.y = self.target_y = TILE_SIZE
        self.invincibility_frames = 0


class Enemy(Entity):
    def __init__(self, gx, gy):
        super().__init__(gx, gy, ENEMY_SPEED)
        self.walk_sprites = ["enemy_walk_1", "enemy_walk_2"]
        self.image = self.walk_sprites[0]
        self.hp = 1

    def update(self, target_hero):
        if self.is_dead:
            self.image = "enemy_dead"
            return
        if not self.is_moving:
            dx = 0;
            dy = 0
            if random.random() < 0.5:
                dx = 1 if target_hero.grid_x > self.grid_x else -1 if target_hero.grid_x < self.grid_x else 0
                dy = 1 if target_hero.grid_y > self.grid_y else -1 if target_hero.grid_y < self.grid_y else 0
            else:
                dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            nx, ny = self.grid_x + dx, self.grid_y + dy
            if MAPS[current_level][ny][nx] != "#":
                self.grid_x, self.grid_y = nx, ny
                self.target_x, self.target_y = nx * TILE_SIZE, ny * TILE_SIZE
                self.is_moving = True
        self.update_position()
        self.image = self.get_animation_frame(self.walk_sprites)


hero = Hero(1, 1)
enemies = []
btn_start = Rect(110, 110, 100, 35)
btn_instr = Rect(110, 160, 100, 35)
btn_audio = Rect(110, 210, 100, 35)
btn_exit = Rect(110, 260, 100, 35)


def play_effect(name):
    if audio_enabled:
        try:
            getattr(sounds, name).play()
        except:
            pass


def toggle_music():
    global music_playing
    if audio_enabled and game_state == STATE_GAME:
        if not music_playing:
            music.play("background_music")
            music.set_volume(0.4)
            music_playing = True
    else:
        music.stop()
        music_playing = False


def spawn_entities():
    enemies.clear()
    count = 2 + (current_level * 2)
    while len(enemies) < count:
        ex, ey = random.randint(3, 8), random.randint(3, 8)
        if MAPS[current_level][ey][ex] == ".": enemies.append(Enemy(ex, ey))


def update():
    global current_level, game_state
    if game_state != STATE_GAME: return

    hero.update()
    if hero.is_dead:
        game_state = STATE_GAMEOVER
        return

    if not hero.is_moving:
        if keyboard.left or keyboard.a:
            hero.move(-1, 0)
        elif keyboard.right or keyboard.d:
            hero.move(1, 0)
        elif keyboard.up or keyboard.w:
            hero.move(0, -1)
        elif keyboard.down or keyboard.s:
            hero.move(0, 1)

    if keyboard.space and hero.attack_cooldown == 0:
        hero.attack_cooldown = 30
        hx, hy = hero.facing_direction
        hero.axe_pos = (hero.x + hx * TILE_SIZE, hero.y + hy * TILE_SIZE)
        hero.axe_visible, hero.axe_timer = True, 10
        hitbox = hero.get_rect().union(Rect(hero.axe_pos[0], hero.axe_pos[1], TILE_SIZE, TILE_SIZE))
        for e in enemies:
            if not e.is_dead and hitbox.colliderect(e.get_rect()):
                e.hp -= 1
                if e.hp <= 0: e.is_dead = True; play_effect("enemy_hit")

    all_enemies_dead = True
    for e in enemies:
        e.update(hero)
        if not e.is_dead:
            all_enemies_dead = False
            # Verifica colisão herói/inimigo
            if hero.get_rect().colliderect(e.get_rect()):
                hero.take_damage()

    if all_enemies_dead and enemies:
        play_effect("level_up")
        if hero.health < hero.max_health: hero.health += 1
        current_level = (current_level + 1) % len(MAPS)
        hero.grid_x, hero.grid_y = 1, 1
        hero.x, hero.y = TILE_SIZE, TILE_SIZE
        hero.target_x, hero.target_y = TILE_SIZE, TILE_SIZE
        spawn_entities()


def on_mouse_down(pos):
    global game_state, audio_enabled, current_level
    if game_state == STATE_MENU:
        if btn_start.collidepoint(pos):
            current_level = 0
            hero.reset_stats()
            game_state = STATE_GAME
            spawn_entities()
            toggle_music()
        elif btn_instr.collidepoint(pos):
            game_state = STATE_INSTRUCTIONS
        elif btn_audio.collidepoint(pos):
            audio_enabled = not audio_enabled
            toggle_music()
        elif btn_exit.collidepoint(pos):
            exit()
    elif game_state in [STATE_INSTRUCTIONS, STATE_GAMEOVER]:
        game_state = STATE_MENU


def draw():
    screen.clear()
    if game_state == STATE_MENU:
        screen.fill((20, 40, 20))
        screen.draw.text("WOLF ADVENTURE", center=(WIDTH // 2, 60), fontsize=40)
        screen.draw.filled_rect(btn_start, (50, 150, 50))
        screen.draw.text("START", center=btn_start.center, fontsize=25)
        screen.draw.filled_rect(btn_instr, (100, 100, 100))
        screen.draw.text("HOW TO PLAY", center=btn_instr.center, fontsize=15)
        screen.draw.filled_rect(btn_audio, (50, 50, 150))
        screen.draw.text("AUDIO: " + ("ON" if audio_enabled else "OFF"), center=btn_audio.center, fontsize=18)
        screen.draw.filled_rect(btn_exit, (150, 50, 50))
        screen.draw.text("EXIT", center=btn_exit.center, fontsize=18)

    elif game_state == STATE_INSTRUCTIONS:
        screen.fill((30, 30, 30))
        screen.draw.text("INSTRUCTIONS", center=(WIDTH // 2, 50), fontsize=35, color="yellow")
        instr = "- Move: WASD / Arrows\n- Attack: SPACE\n- Goal: Clear the level\n\n- Pass Level: +1 HP\n- Hitbox: Your square + front!"
        screen.draw.text(instr, (40, 120), fontsize=20)
        screen.draw.text("Click to go back", center=(WIDTH // 2, 330), fontsize=18, color="gray")

    else:
        for y, row in enumerate(MAPS[current_level]):
            for x, char in enumerate(row):
                color = COLOR_WALL if char == "#" else COLOR_FLOOR
                screen.draw.filled_rect(Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), color)
        for e in enemies: screen.blit(e.image, (e.x, e.y))
        if hero.axe_visible: screen.blit("axe", hero.axe_pos)
        if hero.invincibility_frames % 6 < 3: screen.blit(hero.image, (hero.x, hero.y))
        screen.draw.filled_rect(Rect(0, 320, WIDTH, 64), COLOR_UI_BG)
        screen.draw.text(f"LEVEL: {current_level + 1}", (10, 335), fontsize=20)
        screen.draw.filled_rect(Rect(150, 340, 150, 15), COLOR_HEALTH_BAR)
        screen.draw.filled_rect(Rect(150, 340, (hero.health / hero.max_health) * 150, 15), COLOR_HEALTH_FILL)
        if game_state == STATE_GAMEOVER:
            screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")