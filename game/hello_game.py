from __future__ import annotations

import math
from pathlib import Path

from Microsoft.Xna.Framework import Color, Game, GraphicsDeviceManager, PlayerIndex, Vector2
from Microsoft.Xna.Framework.Graphics import SpriteBatch, SpriteEffects, Texture2D
from Microsoft.Xna.Framework.Input import ButtonState, Buttons, GamePad, Keyboard, Keys, Mouse


class HelloGame(Game):
    """Small real CNA 2D game; there is no simulated or managed-only render path."""

    def __init__(self, requested_frames: int | None = None) -> None:
        super().__init__()
        if requested_frames is not None and requested_frames <= 0:
            raise ValueError("requested_frames must be positive")
        self.Graphics = GraphicsDeviceManager(self)
        self.RequestedFrames = requested_frames
        self.DrawnFrames = 0
        self._animation_seconds = 0.0
        self._velocity = Vector2(104.0, 74.0)
        self._position = Vector2.Zero
        self._logo: Texture2D | None = None
        self._sprite_batch: SpriteBatch | None = None

    def LoadContent(self) -> None:
        logo_path = Path(__file__).resolve().parents[1] / "Content" / "logo.png"
        with logo_path.open("rb") as stream:
            self._logo = Texture2D.FromStream(self.GraphicsDevice, stream)
        self._sprite_batch = SpriteBatch(self.GraphicsDevice)
        viewport = self.GraphicsDevice.Viewport
        self._position = Vector2(viewport.Width / 2.0, viewport.Height / 2.0)

    def Update(self, gameTime) -> None:
        keyboard = Keyboard.GetState()
        mouse = Mouse.GetState()
        gamepad = GamePad.GetState(PlayerIndex.One)
        if keyboard.IsKeyDown(Keys.Escape):
            self.Exit()

        # Polling mouse/gamepad is part of the real canary. Connected input may
        # influence motion; HEADLESS legitimately reports no device/buttons.
        speed = 1.5 if mouse.LeftButton is ButtonState.Pressed else 1.0
        if gamepad.IsConnected and gamepad.IsButtonDown(Buttons.A):
            speed = 2.0
        elapsed = gameTime.ElapsedGameTime.total_seconds()
        self._animation_seconds += elapsed
        self._position.X += self._velocity.X * elapsed * speed
        self._position.Y += self._velocity.Y * elapsed * speed

        viewport = self.GraphicsDevice.Viewport
        half_width = self._logo.Width / 2.0 if self._logo is not None else 0.0
        half_height = self._logo.Height / 2.0 if self._logo is not None else 0.0
        if self._position.X < half_width:
            self._position.X = half_width
            self._velocity.X = abs(self._velocity.X)
        elif self._position.X > viewport.Width - half_width:
            self._position.X = viewport.Width - half_width
            self._velocity.X = -abs(self._velocity.X)
        if self._position.Y < half_height:
            self._position.Y = half_height
            self._velocity.Y = abs(self._velocity.Y)
        elif self._position.Y > viewport.Height - half_height:
            self._position.Y = viewport.Height - half_height
            self._velocity.Y = -abs(self._velocity.Y)

    def Draw(self, gameTime) -> None:
        self.GraphicsDevice.Clear(Color.CornflowerBlue)
        scale = 0.96 + 0.12 * math.sin(self._animation_seconds * 1.3)
        rotation = 0.11 * math.sin(self._animation_seconds * 1.1)
        origin = Vector2(self._logo.Width / 2.0, self._logo.Height / 2.0)
        self._sprite_batch.Begin()
        self._sprite_batch.Draw(
            self._logo,
            self._position,
            None,
            Color.White,
            rotation,
            origin,
            scale,
            SpriteEffects.None_,
            0.0,
        )
        self._sprite_batch.End()
        self.DrawnFrames += 1
        if self.RequestedFrames is not None and self.DrawnFrames == self.RequestedFrames:
            self.Exit()

    def UnloadContent(self) -> None:
        if self._sprite_batch is not None:
            self._sprite_batch.Dispose()
        if self._logo is not None:
            self._logo.Dispose()
