import math
import sys
from Microsoft.Xna.Framework import Game, GameTime, Vector2, Vector3, Color, Matrix
from Microsoft.Xna.Framework.Graphics import GraphicsDeviceManager, SpriteBatch, BasicEffect
from Microsoft.Xna.Framework.Input import Keyboard, Keys

class HelloGame(Game):
    def __init__(self, smoke_test=False):
        super().__init__()
        self.Graphics = GraphicsDeviceManager(self)
        self.SmokeTest = smoke_test
        self._drawn_frames = 0
        self._animation_seconds = 0.0
        self._renderer_banner_seconds = 5.0
        self._velocity = Vector2(104.0, 74.0)
        self._position = Vector2.Zero()
        
    def Initialize(self):
        # In a real CNA app, we would set preferred buffer size here
        super().Initialize()

    def LoadContent(self):
        self._sprite_batch = SpriteBatch(self.GraphicsDevice)
        
        # In a real app: self._logo = self.Content.Load("logo")
        self._logo = None # Placeholder
        
        # Solid white 1x1 texture for banner background
        self._solid = None # Placeholder
        
        self._renderer_name = "CNA (Python)"
        self._supports_3d = True # Assume 3D support
        
        if self._supports_3d:
            self._cube_effect = BasicEffect(self.GraphicsDevice)
            self._cube_effect.TextureEnabled = True
            self._cube_effect.Texture = self._logo
            
        vp = self.GraphicsDevice.Viewport
        self._position = Vector2(vp.Width / 2.0, vp.Height / 2.0)
        
        print(f"cna-python-template: renderer {self._renderer_name}")

    def Update(self, gameTime):
        dt = gameTime.ElapsedGameTime
        self._animation_seconds += dt
        
        if Keyboard.GetState().IsKeyDown(Keys.Escape):
            self.Exit()
            
        if not self._supports_3d:
            movement_delta = dt * 2.0
            self._position.X += self._velocity.X * movement_delta
            self._position.Y += self._velocity.Y * movement_delta
            
            vp = self.GraphicsDevice.Viewport
            logo_size = 256.0 # Placeholder
            
            min_x, min_y = logo_size / 2.0, logo_size / 2.0
            max_x, max_y = vp.Width - min_x, vp.Height - min_y
            
            if self._position.X < min_x:
                self._position.X = min_x
                self._velocity.X = abs(self._velocity.X)
            elif self._position.X > max_x:
                self._position.X = max_x
                self._velocity.X = -abs(self._velocity.X)
                
            if self._position.Y < min_y:
                self._position.Y = min_y
                self._velocity.Y = abs(self._velocity.Y)
            elif self._position.Y > max_y:
                self._position.Y = max_y
                self._velocity.Y = -abs(self._velocity.Y)

        super().Update(gameTime)

    def Draw(self, gameTime):
        self.GraphicsDevice.Clear(Color.CornflowerBlue)
        
        if self._supports_3d:
            self._draw_3d_cube()
        else:
            self._draw_2d_logo()
            
        if self._animation_seconds < self._renderer_banner_seconds:
            self._draw_renderer_banner()
            
        if self.SmokeTest:
            self._drawn_frames += 1
            if self._drawn_frames >= 3:
                print(f"cna-python-template: smoke test drew {self._drawn_frames} frames; exiting")
                self.Exit()

        super().Draw(gameTime)

    def _draw_2d_logo(self):
        motion = self._animation_seconds * 2.0
        scale = 0.96 + 0.12 * math.sin(motion * 0.65)
        rotation = 0.11 * math.sin(motion * 0.55)
        origin = Vector2(128.0, 128.0) # Placeholder for logo center
        
        self._sprite_batch.Begin()
        self._sprite_batch.Draw(self._logo, self._position, None, Color.White, rotation, origin, scale)
        self._sprite_batch.End()

    def _draw_3d_cube(self):
        vp = self.GraphicsDevice.Viewport
        aspect = vp.Width / vp.Height
        
        motion = self._animation_seconds * 2.0
        scale = 0.88 + 0.10 * math.sin(motion * 0.48)
        move_x = 1.15 * math.sin(motion * 0.24)
        move_y = 0.65 * math.sin(motion * 0.36)
        
        world = Matrix.CreateScale(scale)
        world = world * Matrix.CreateRotationY(motion * 0.55)
        world = world * Matrix.CreateRotationX(motion * 0.35)
        world = world * Matrix.CreateTranslation(move_x, move_y, 0.0)
        
        self._cube_effect.World = world
        self._cube_effect.View = Matrix.CreateLookAt(Vector3(0, 0, 6), Vector3.Zero(), Vector3.Up())
        self._cube_effect.Projection = Matrix.CreatePerspectiveFieldOfView(0.7853982, aspect, 0.1, 100.0)
        
        self._cube_effect.Apply()
        # Drawing primitives would go here

    def _draw_renderer_banner(self):
        vp = self.GraphicsDevice.Viewport
        name = self._renderer_name.upper()
        
        glyph_cols = len(name) * 6 - 1
        pixel_size = max(1, min(8, (vp.Width - 48) // max(1, glyph_cols)))
        
        text_w = glyph_cols * pixel_size
        text_h = 7 * pixel_size
        text_x = (vp.Width - text_w) // 2
        text_y = vp.Height - text_h - 24
        
        self._sprite_batch.Begin()
        # Draw translucent background
        bg_rect = (text_x - 8, text_y - 8, text_w + 16, text_h + 16)
        self._sprite_batch.DrawRect(self._solid, bg_rect, Color(255, 255, 255, 180))
        
        for i, char in enumerate(name):
            rows = self._get_glyph_rows(char)
            char_x = text_x + i * 6 * pixel_size
            for row in range(7):
                row_data = rows[row]
                for col in range(5):
                    if (row_data >> (4 - col)) & 1:
                        rect = (char_x + col * pixel_size, text_y + row * pixel_size, pixel_size, pixel_size)
                        self._sprite_batch.DrawRect(self._solid, rect, Color.Black)
        self._sprite_batch.End()

    def _get_glyph_rows(self, char):
        # 5x7 bitmap font
        font = {
            'A': [0x04, 0x0A, 0x11, 0x11, 0x1F, 0x11, 0x11],
            'B': [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
            'C': [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
            'D': [0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C],
            'E': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
            'F': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
            'G': [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
            'H': [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
            'I': [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
            'J': [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
            'K': [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
            'L': [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
            'M': [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
            'N': [0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11],
            'O': [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
            'P': [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
            'Q': [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
            'R': [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
            'S': [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
            'T': [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
            'U': [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
            'V': [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
            'W': [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
            'X': [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
            'Y': [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
            'Z': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            '(': [0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02],
            ')': [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
            '-': [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
            '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04],
        }
        return font.get(char, [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F])
