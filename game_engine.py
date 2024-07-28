import pygame
import pygame_gui

class Game:
    def __init__(self):
        pygame.init()

        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Thruster Rocket Simulation')

        rocket_image = pygame.image.load('images/rocket_nofire.png')
        rocket_fire_image = pygame.image.load('images/rocket_fire.png')
        self.rocket_image = pygame.transform.scale(rocket_image, (50, 70))
        self.rocket_fire_image = pygame.transform.scale(rocket_fire_image, (50, 70))

        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

        self.mass = 1.0  # kg
        self.thrust_power = 00.0  # N
        self.rocket_x, self.rocket_y = self.width // 2, self.height - 50
        self.velocity_y = 0.0
        self.acceleration_y = 0.0

        self.gravity = 9.81  # m/s^2
        self.time_step = 0.1  # seconds

        self.init_gui()

    def init_gui(self):
        self.manager = pygame_gui.UIManager((self.width, self.height))

        self.mass_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            start_value=self.mass,
            value_range=(10, 1000),
            manager=self.manager)

        self.thrust_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 170), (200, 30)),
            start_value=self.thrust_power,
            value_range=(0, 10000),
            manager=self.manager)

        self.mass_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 40), (200, 30)),
            text='Mass: {:.2f} kg'.format(self.mass),
            manager=self.manager)

        self.thrust_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 200), (200, 30)),
            text='Thrust: {:.2f} N'.format(self.thrust_power),
            manager=self.manager)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0  # Limit to 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.manager.process_events(event)

            self.manager.update(time_delta)

            mass = self.mass_slider.get_current_value()
            thrust_power = self.thrust_slider.get_current_value()

            self.mass_label.set_text('Mass: {:.2f} kg'.format(mass))
            self.thrust_label.set_text('Thrust: {:.2f} N'.format(thrust_power))

            gravity_force = mass * self.gravity
            thrust_force = thrust_power
            net_force = thrust_force - gravity_force
            self.acceleration_y = net_force / mass

            self.velocity_y += self.acceleration_y * self.time_step
            self.rocket_y -= self.velocity_y * self.time_step

            if self.rocket_y < 0:
                self.rocket_y = 0
                self.velocity_y = 0
            elif self.rocket_y > self.height - 50:
                self.rocket_y = self.height - 50
                self.velocity_y = 0

            self.screen.fill(self.black)

            if thrust_power > 0:
                self.screen.blit(self.rocket_fire_image, (int(self.rocket_x), int(self.rocket_y)))
            else:
                self.screen.blit(self.rocket_image, (int(self.rocket_x), int(self.rocket_y)))

            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()
