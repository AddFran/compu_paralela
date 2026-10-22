import pygame
import random
import math
import os
from concurrent.futures import ProcessPoolExecutor

# Configuracion
WIDTH,HEIGHT=1200, 800
NUM_BOIDS=1000
WORKERS=os.cpu_count() or 2
PERCEPTION_RADIUS=50
SEPARATION_RADIUS=25
MOUSE_RADIUS=100
MAX_SPEED=4
MAX_FORCE=0.1

def limit_vector(x,y,maximum):
    length=math.hypot(x,y)
    if length>maximum and length > 0:
        return x*maximum/length, y * maximum / length
    return x, y

def steering(dx,dy,vx,vy):
    length = math.hypot(dx, dy)
    if length == 0:
        return 0, 0

    desired_x=dx/length*MAX_SPEED
    desired_y=dy/length*MAX_SPEED

    return limit_vector(
        desired_x-vx,
        desired_y-vy,
        MAX_FORCE
    )


# Funcion ejecutada por los procesos secundarios
def compute_chunk(task):
    positions,velocities,mouse,start,end=task
    results=[]

    mx,my=mouse

    for i in range(start,end):
        x,y=positions[i]
        vx,vy=velocities[i]

        sep_x=sep_y=0
        ali_x=ali_y=0
        coh_x=coh_y=0

        sep_count = ali_count = coh_count = 0

        # Analizar los vecinos
        for j in range(len(positions)):
            if i==j:
                continue
            ox,oy=positions[j]
            ovx,ovy=velocities[j]

            dx=ox-x
            dy=oy-y
            distance=math.hypot(dx, dy)

            if distance==0:
                continue

            # Separacion
            if distance<SEPARATION_RADIUS:
                sep_x-=dx/distance/distance
                sep_y-=dy/distance/distance
                sep_count+=1

            # Alineacion y cohesion
            if distance<PERCEPTION_RADIUS:
                ali_x+=ovx
                ali_y+=ovy

                coh_x+=ox
                coh_y+=oy

                ali_count+=1
                coh_count+=1

        # Calcular separacion
        if sep_count>0:
            sep_x/=sep_count
            sep_y/=sep_count

            sep_x,sep_y=steering(
                sep_x,sep_y,vx,vy
            )

        # Calcular alineacion
        if ali_count>0:
            ali_x/=ali_count
            ali_y/=ali_count

            ali_x,ali_y=steering(
                ali_x,ali_y,vx,vy
            )

        # Calcular cohesion
        if coh_count>0:
            coh_x=coh_x/coh_count-x
            coh_y=coh_y/coh_count-y
            coh_x,coh_y=steering(coh_x,coh_y,vx,vy)

        # Escapar del mouse
        flee_x=flee_y = 0

        mdx=x-mx
        mdy=y-my
        mouse_distance=math.hypot(mdx,mdy)

        if 0<mouse_distance<MOUSE_RADIUS:
            strength=(MOUSE_RADIUS-mouse_distance)/MOUSE_RADIUS

            flee_x,flee_y=steering(
                mdx,mdy,vx,vy
            )

            flee_x*=strength*3
            flee_y*=strength*3

        # Combinar fuerzas
        ax=sep_x*1.5+ali_x+coh_x+flee_x
        ay=sep_y*1.5+ali_y+coh_y+flee_y

        results.append((ax,ay))
    return results

class Boid:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)

        angle=random.uniform(0,2*math.pi)
        speed=random.uniform(2,MAX_SPEED)

        self.velocity = pygame.math.Vector2(
            math.cos(angle), math.sin(angle)
        ) * speed

        self.acceleration = pygame.math.Vector2(0, 0)

    def update(self):
        self.velocity += self.acceleration

        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)

        self.position += self.velocity
        self.acceleration.update(0, 0)

    def edges(self):
        self.position.x %= WIDTH
        self.position.y %= HEIGHT

    def draw(self, surface):
        angle = math.degrees(
            math.atan2(-self.velocity.y, self.velocity.x)
        ) + 90

        p1 = self.position + pygame.math.Vector2(
            0, -8
        ).rotate(-angle)

        p2 = self.position + pygame.math.Vector2(
            -4, 6
        ).rotate(-angle)

        p3 = self.position + pygame.math.Vector2(
            4, 6
        ).rotate(-angle)

        pygame.draw.polygon(
            surface, (255, 255, 255), [p1, p2, p3]
        )


def main():
    # Solo el proceso principal inicializa Pygame
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "Boids - Computacion Paralela"
    )

    clock = pygame.time.Clock()

    boids = [
        Boid(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT)
        )
        for _ in range(NUM_BOIDS)
    ]

    font=pygame.font.Font(None,24)
    running=True

    # Crear los procesos una sola vez
    with ProcessPoolExecutor(
        max_workers=WORKERS
    ) as executor:

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((20, 20, 30))

            # Guardar el estado actual de los boids
            positions = [
                (b.position.x, b.position.y)
                for b in boids
            ]

            velocities = [
                (b.velocity.x, b.velocity.y)
                for b in boids
            ]

            mouse = pygame.mouse.get_pos()

            # Dividir los calculos entre procesos
            chunk_size=math.ceil(NUM_BOIDS/WORKERS)

            tasks=[]

            for w in range(WORKERS):
                start=w*chunk_size
                end=min(start+chunk_size,NUM_BOIDS)
                if start<end:
                    tasks.append((
                        positions,
                        velocities,
                        mouse,
                        start,
                        end
                    ))

            # Ejecutar calculos en paralelo
            chunks=list(executor.map(compute_chunk, tasks))

            forces = [
                force
                for chunk in chunks
                for force in chunk
            ]

            # Actualizar y dibujar en la ventana principal
            for boid,(ax,ay) in zip(boids, forces):
                boid.acceleration.update(ax, ay)
                boid.update()
                boid.edges()
                boid.draw(screen)

            # Mostrar el radio de escape del mouse
            pygame.draw.circle(
                screen,
                (100, 100, 120),
                mouse,
                MOUSE_RADIUS,
                1
            )
            info = font.render(
                f"Boids: {NUM_BOIDS} | "
                f"Procesos: {WORKERS} | "
                f"FPS: {clock.get_fps():.0f}",
                True,
                (230, 230, 230)
            )
            screen.blit(info, (10, 10))
            pygame.display.flip()
            clock.tick()

    pygame.quit()

if __name__ == "__main__":
    main()  