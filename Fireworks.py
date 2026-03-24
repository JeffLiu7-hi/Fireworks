import pygame
import random
import math
 
# --- 1. 初始化设置 ---
pygame.init()
pygame.display.set_caption("2026 跨年盛典 - 作者: JeffLiu777")
 
# 屏幕宽高
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
 
# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # 淡金色，用于祝福语
 
 
# --- 2. 字体加载 (处理中文兼容性) ---
def get_font(size):
    try:
        # 尝试常见中文字体
        font_names = ["simhei", "microsoftyahei", "pingfangsc", "stheiti"]
        match = pygame.font.match_font(font_names[0])
        for name in font_names:
            match = pygame.font.match_font(name)
            if match: break
        if match:
            return pygame.font.Font(match, size)
        return pygame.font.SysFont("arial", size, bold=True)
    except:
        return pygame.font.SysFont("arial", size, bold=True)
 
 
font_huge = get_font(120)
font_text = get_font(80)
font_small = get_font(40)
font_blessing = get_font(32)  # 祝福语字体，稍微小一点，精致一点
 
 
# --- 3. 辅助功能：生成极致鲜艳的颜色 ---
def get_vibrant_color():
    color = pygame.Color(0)
    color.hsva = (random.randint(0, 360), 100, 100, 100)
    return color
 
 
# --- 5. 粒子类 (烟花花瓣) ---
class Particle:
    def __init__(self, x, y, color, explode=False):
        self.x = x
        self.y = y
        self.color = color
        self.explode = explode
        self.alive = True
 
        if self.explode:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 10)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.timer = random.randint(50, 90)
            self.size = random.randint(2, 4)
            self.decay = 0.96
        else:
            self.vx = random.uniform(-1, 1)
            self.vy = -random.uniform(13, 18)
            self.timer = 100
            self.size = 3
            self.decay = 1.0
 
    def move(self):
        self.x += self.vx
        self.y += self.vy
 
        if self.explode:
            self.vy += 0.08
            self.vx *= self.decay
            self.vy *= self.decay
        else:
            self.vy += 0.25
 
        if self.explode:
            self.timer -= 1
            if self.timer <= 0:
                self.alive = False
 
    def draw(self, surface):
        if self.explode:
            if self.timer < 15:
                s = self.size * (self.timer / 15)
            else:
                s = self.size
            if s > 0.5:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(s))
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
 
 
# --- 6. 烟花管理类 ---
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.color = get_vibrant_color()
        self.seed = Particle(self.x, self.y, self.color, explode=False)
        self.particles = []
        self.exploded = False
 
    def update(self):
        if not self.exploded:
            self.seed.move()
            if self.seed.vy >= 0:
                self.explode()
        else:
            for p in self.particles:
                p.move()
            self.particles = [p for p in self.particles if p.alive]
 
    def explode(self):
        self.exploded = True
        amount = random.randint(120, 200)
        for _ in range(amount):
            p_color = self.color if random.random() > 0.2 else (255, 255, 255)
            self.particles.append(Particle(self.seed.x, self.seed.y, p_color, explode=True))
 
    def draw(self, surface):
        if not self.exploded:
            self.seed.draw(surface)
        else:
            for p in self.particles:
                p.draw(surface)
 
 
# --- 7. 艺术字绘制 ---
def draw_rainbow_text(surface, text, font, center_pos, hue):
    color = pygame.Color(0)
    color.hsva = (hue % 360, 100, 100, 100)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=center_pos)
    for offset in [2, 4]:
        shadow = font.render(text, True, (40, 40, 40))
        surface.blit(shadow, (text_rect.x + offset, text_rect.y + offset))
    surface.blit(text_surf, text_rect)
 
 
# [新增] 绘制电影字幕风格文字（淡入淡出，无闪烁）
def draw_subtitle(surface, text, font, center_pos, alpha):
    # 创建文字表面
    text_surf = font.render(text, True, GOLD)  # 使用淡金色
 
    # 创建一个支持透明度的容器
    # 必须复制一个 surface 才能单独设置 alpha
    alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
    alpha_surf.fill((0, 0, 0, 0))  # 透明填充
    alpha_surf.blit(text_surf, (0, 0))
 
    # 设置整体透明度
    alpha_surf.set_alpha(alpha)
 
    text_rect = alpha_surf.get_rect(center=center_pos)
    surface.blit(alpha_surf, text_rect)
 
 
# --- 8. 主程序 ---
def main():
    running = True

    STATE_FIREWORKS = 0
    current_state = STATE_FIREWORKS

    start_ticks = pygame.time.get_ticks()
    firework_start_time = start_ticks

    fireworks = []

    trail_surface = pygame.Surface((WIDTH, HEIGHT))
    trail_surface.set_alpha(40)
    trail_surface.fill(BLACK)

 
    while running:
        current_ticks = pygame.time.get_ticks()
        elapsed_seconds = (current_ticks - start_ticks) / 1000
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # === 烟花盛宴 ===
        screen.blit(trail_surface, (0, 0))

        if random.randint(1, 12) == 1:
            fireworks.append(Firework())

        for fw in fireworks:
            fw.update()
            fw.draw(screen)

        fireworks = [fw for fw in fireworks if not fw.exploded or len(fw.particles) > 0]

        pygame.display.flip()
        clock.tick(60)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()
