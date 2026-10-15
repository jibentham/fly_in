import pygame
import moderngl


def render_network() -> None:
    pygame.init()
    pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MAJOR_VERSION, 3
            )
    pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MINOR_VERSION, 3
            )
    pygame.display.gl_set_attribute(
            pygame.GL_DEPTH_SIZE, 24
            )
    screen = pygame.display.set_mode((3840, 2160), pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ctx.clear(0.2, 0.3, 0.4, 1.0, depth=1.0)
        #Rendering code goes here
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
