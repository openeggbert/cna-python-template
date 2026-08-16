import math
import cna
from cna import Vector2, Color

class HelloGame(cna.Game):
    def __init__(self):
        super().__init__()
        self.graphics = cna.GraphicsDeviceManager(self)
        self.content.root_directory = "Content"

    def initialize(self):
        self.graphics.preferred_back_buffer_width = 1280
        self.graphics.preferred_back_buffer_height = 720
        self.graphics.apply_changes()
        super().initialize()

    def load_content(self):
        self.sprite_batch = cna.SpriteBatch(self.graphics_device)
        self.logo = self.content.load_texture2d("logo")
        self.position = Vector2(0, 0)

    def update(self, game_time):
        time = game_time.total_game_time.total_seconds()
        self.position.x = 640.0 + 200.0 * math.sin(time)
        self.position.y = 360.0 + 200.0 * math.cos(time)
        super().update(game_time)

    def draw(self, game_time):
        self.graphics_device.clear(Color.CORNFLOWER_BLUE)
        self.sprite_batch.begin()
        self.sprite_batch.draw(self.logo, self.position, Color.WHITE)
        self.sprite_batch.end()
        super().draw(game_time)
