# pattern_manager.py - Pattern Management System
import time
import math
import random
import numpy as np
from config import Config

class PatternManager:
    def __init__(self, led_matrix, audio_processor):
        self.led_matrix = led_matrix
        self.audio_processor = audio_processor
        self.config = Config()
        
        # Current state
        self.current_mode = 0  # 0=AUDIO, 1=AMBIENT, 2=GAMES
        self.current_pattern = 0
        self.pattern_start_time = time.time()
        
        # Pattern instances
        self.audio_patterns = [
            SpectrumAnalyzer(led_matrix, audio_processor),
            WaveformPattern(led_matrix, audio_processor),
            PulsingCircles(led_matrix, audio_processor),
            FrequencyBars(led_matrix, audio_processor)
        ]
        
        self.ambient_patterns = [
            DigitalClock(led_matrix),
            MatrixRain(led_matrix),
            FireEffect(led_matrix),
            PlasmaEffect(led_matrix)
        ]
        
        self.games = [
            Snake(led_matrix),
            ConwayLife(led_matrix),
            Tetris(led_matrix)
        ]
        
        self.pattern_collections = [
            self.audio_patterns,
            self.ambient_patterns,
            self.games
        ]
    
    def next_pattern(self):
        """Switch to next pattern in current mode"""
        current_collection = self.pattern_collections[self.current_mode]
        self.current_pattern = (self.current_pattern + 1) % len(current_collection)
        self.pattern_start_time = time.time()
        print(f"Switched to pattern {self.current_pattern} in mode {self.current_mode}")
    
    def previous_pattern(self):
        """Switch to previous pattern in current mode"""
        current_collection = self.pattern_collections[self.current_mode]
        self.current_pattern = (self.current_pattern - 1) % len(current_collection)
        self.pattern_start_time = time.time()
        print(f"Switched to pattern {self.current_pattern} in mode {self.current_mode}")
    
    def next_mode(self):
        """Switch to next mode (Audio/Ambient/Games)"""
        self.current_mode = (self.current_mode + 1) % len(self.pattern_collections)
        self.current_pattern = 0
        self.pattern_start_time = time.time()
        mode_names = ['AUDIO', 'AMBIENT', 'GAMES']
        print(f"Switched to mode: {mode_names[self.current_mode]}")
    
    def update(self):
        """Update current pattern"""
        current_collection = self.pattern_collections[self.current_mode]
        if current_collection:
            pattern = current_collection[self.current_pattern]
            pattern.update()
    
    def toggle_settings(self):
        """Toggle pattern-specific settings"""
        current_collection = self.pattern_collections[self.current_mode]
        if current_collection:
            pattern = current_collection[self.current_pattern]
            if hasattr(pattern, 'toggle_settings'):
                pattern.toggle_settings()


# Base Pattern Class
class BasePattern:
    def __init__(self, led_matrix):
        self.led_matrix = led_matrix
        self.start_time = time.time()
        
    def get_time(self):
        """Get time since pattern started"""
        return time.time() - self.start_time
    
    def update(self):
        """Override in subclasses"""
        pass


# Audio-Reactive Patterns
class SpectrumAnalyzer(BasePattern):
    def __init__(self, led_matrix, audio_processor):
        super().__init__(led_matrix)
        self.audio_processor = audio_processor
        self.smoothing_factor = 0.7
        self.prev_bands = np.zeros(16)
        
    def update(self):
        self.led_matrix.clear()
        
        # Get frequency band data
        bands = self.audio_processor.get_frequency_bands()
        
        # Smooth the data
        self.prev_bands = (self.smoothing_factor * self.prev_bands + 
                          (1 - self.smoothing_factor) * bands)
        
        # Draw frequency bars
        for i in range(16):
            height = int(self.prev_bands[i] * 16)
            hue = i / 16.0  # Rainbow colors across frequency spectrum
            
            for y in range(height):
                # Color intensity based on height
                saturation = 1.0
                value = (y + 1) / 16.0
                self.led_matrix.set_pixel_hsv(i, 15 - y, hue, saturation, value)


class WaveformPattern(BasePattern):
    def __init__(self, led_matrix, audio_processor):
        super().__init__(led_matrix)
        self.audio_processor = audio_processor
        self.waveform_history = []
        
    def update(self):
        self.led_matrix.clear()
        
        # Get current volume and add to history
        volume = self.audio_processor.get_volume()
        self.waveform_history.append(volume)
        
        # Keep only last 16 samples (width of matrix)
        if len(self.waveform_history) > 16:
            self.waveform_history.pop(0)
        
        # Draw waveform
        for x in range(len(self.waveform_history)):
            amplitude = self.waveform_history[x]
            center_y = 8
            wave_height = int(amplitude * 8)
            
            # Draw wave from center outward
            for y in range(max(0, center_y - wave_height), 
                          min(16, center_y + wave_height + 1)):
                distance_from_center = abs(y - center_y)
                intensity = max(0, 1.0 - distance_from_center / 8.0)
                
                color = (
                    int(intensity * 255),
                    int(intensity * 100),
                    int(intensity * 255)
                )
                self.led_matrix.set_pixel(x, y, color)


class PulsingCircles(BasePattern):
    def __init__(self, led_matrix, audio_processor):
        super().__init__(led_matrix)
        self.audio_processor = audio_processor
        self.circles = []
        
    def update(self):
        self.led_matrix.clear()
        
        # Create new circle on beat
        if self.audio_processor.is_beat_detected():
            self.circles.append({
                'x': 8,
                'y': 8,
                'radius': 0,
                'max_radius': 12,
                'hue': random.random(),
                'birth_time': time.time()
            })
        
        # Update and draw circles
        current_time = time.time()
        self.circles = [c for c in self.circles if current_time - c['birth_time'] < 2.0]
        
        for circle in self.circles:
            age = current_time - circle['birth_time']
            progress = age / 2.0  # 2 second lifetime
            
            circle['radius'] = progress * circle['max_radius']
            alpha = 1.0 - progress
            
            # Draw circle
            for y in range(16):
                for x in range(16):
                    distance = math.sqrt((x - circle['x'])**2 + (y - circle['y'])**2)
                    if abs(distance - circle['radius']) < 1.0:
                        intensity = alpha * (1.0 - abs(distance - circle['radius']))
                        self.led_matrix.set_pixel_hsv(
                            x, y, 
                            circle['hue'], 
                            1.0, 
                            intensity
                        )


class FrequencyBars(BasePattern):
    def __init__(self, led_matrix, audio_processor):
        super().__init__(led_matrix)
        self.audio_processor = audio_processor
        
    def update(self):
        self.led_matrix.clear()
        
        bands = self.audio_processor.get_frequency_bands()
        
        # Draw as vertical bars with gaps
        for i in range(0, 16, 2):  # Every other column
            band_index = i // 2
            if band_index < len(bands):
                height = int(bands[band_index] * 16)
                
                for y in range(height):
                    # Color from red (bottom) to blue (top)
                    hue = (1.0 - y / 16.0) * 0.8  # Red to blue range
                    self.led_matrix.set_pixel_hsv(i, 15 - y, hue, 1.0, 1.0)
                    if i + 1 < 16:  # Fill the gap
                        self.led_matrix.set_pixel_hsv(i + 1, 15 - y, hue, 1.0, 0.7)


# Ambient Patterns
class DigitalClock(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        self.digit_patterns = {
            '0': [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
            '1': [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
            '2': [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
            '3': [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],
            '4': [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
            '5': [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
            '6': [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
            '7': [[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
            '8': [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
            '9': [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]],
            ':': [[0],[1],[0],[1],[0]]
        }
        
    def draw_digit(self, digit, start_x, start_y, color):
        if digit in self.digit_patterns:
            pattern = self.digit_patterns[digit]
            for y, row in enumerate(pattern):
                for x, pixel in enumerate(row):
                    if pixel and start_x + x < 16 and start_y + y < 16:
                        self.led_matrix.set_pixel(start_x + x, start_y + y, color)
    
    def update(self):
        self.led_matrix.clear()
        
        # Get current time
        current_time = time.strftime("%H:%M")
        
        # Color cycles through rainbow
        hue = (self.get_time() * 0.1) % 1.0
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))
        
        # Draw time centered
        self.draw_digit(current_time[0], 1, 6, color)   # H
        self.draw_digit(current_time[1], 5, 6, color)   # H
        self.draw_digit(':', 8, 6, color)               # :
        self.draw_digit(current_time[3], 10, 6, color)  # M
        self.draw_digit(current_time[4], 14, 6, color)  # M


class MatrixRain(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        self.drops = []
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
    def update(self):
        # Fade existing pixels
        for y in range(16):
            for x in range(16):
                current = self.led_matrix.buffer[y, x]
                faded = [max(0, c - 15) for c in current]
                self.led_matrix.set_pixel(x, y, faded)
        
        # Add new drops randomly
        if random.random() < 0.3:
            self.drops.append({
                'x': random.randint(0, 15),
                'y': 0,
                'speed': random.uniform(0.5, 2.0),
                'last_update': time.time()
            })
        
        # Update drops
        current_time = time.time()
        for drop in self.drops[:]:
            if current_time - drop['last_update'] > 1.0 / drop['speed']:
                drop['y'] += 1
                drop['last_update'] = current_time
                
                if drop['y'] < 16:
                    # Bright green for leading edge
                    self.led_matrix.set_pixel(drop['x'], drop['y'], (0, 255, 0))
                else:
                    self.drops.remove(drop)


class FireEffect(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        self.heat = np.zeros((16, 16))
        
    def update(self):
        # Cool down every cell a little
        self.heat *= 0.95
        
        # Add random heat at bottom
        for x in range(16):
            if random.random() < 0.8:
                self.heat[15, x] = min(1.0, self.heat[15, x] + random.uniform(0.3, 1.0))
        
        # Heat rises and spreads
        new_heat = self.heat.copy()
        for y in range(14, -1, -1):
            for x in range(16):
                # Average with neighbors and cell below
                neighbors = []
                for dy in range(2):
                    for dx in range(-1, 2):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < 16 and 0 <= nx < 16:
                            neighbors.append(self.heat[ny, nx])
                
                new_heat[y, x] = np.mean(neighbors) * 0.98
        
        self.heat = new_heat
        
        # Convert heat to fire colors
        for y in range(16):
            for x in range(16):
                heat_val = self.heat[y, x]
                if heat_val > 0.1:
                    # Fire gradient: black -> red -> orange -> yellow -> white
                    if heat_val < 0.3:
                        # Red
                        intensity = heat_val / 0.3
                        color = (int(255 * intensity), 0, 0)
                    elif heat_val < 0.6:
                        # Orange
                        intensity = (heat_val - 0.3) / 0.3
                        color = (255, int(128 * intensity), 0)
                    elif heat_val < 0.9:
                        # Yellow
                        intensity = (heat_val - 0.6) / 0.3
                        color = (255, 128 + int(127 * intensity), 0)
                    else:
                        # White
                        intensity = (heat_val - 0.9) / 0.1
                        white_add = int(255 * intensity)
                        color = (255, 255, white_add)
                    
                    self.led_matrix.set_pixel(x, y, color)


class PlasmaEffect(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        
    def update(self):
        t = self.get_time()
        
        for y in range(16):
            for x in range(16):
                # Create plasma effect using sine waves
                v1 = math.sin((x + t) * 0.5)
                v2 = math.sin((y + t) * 0.4)
                v3 = math.sin((x + y + t) * 0.3)
                v4 = math.sin(math.sqrt((x - 8)**2 + (y - 8)**2) + t)
                
                plasma = (v1 + v2 + v3 + v4) / 4.0
                
                # Convert to color
                hue = (plasma + 1.0) / 2.0  # Normalize to 0-1
                self.led_matrix.set_pixel_hsv(x, y, hue, 1.0, 1.0)


# Simple Games
class Snake(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        self.snake = [(8, 8), (8, 9), (8, 10)]
        self.direction = (0, -1)  # Moving up
        self.food = (4, 4)
        self.last_move = time.time()
        self.move_interval = 0.5
        
    def update(self):
        self.led_matrix.clear()
        
        # Move snake
        current_time = time.time()
        if current_time - self.last_move > self.move_interval:
            head = self.snake[0]
            new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
            
            # Wrap around edges
            new_head = (new_head[0] % 16, new_head[1] % 16)
            
            # Check if food eaten
            if new_head == self.food:
                self.snake.insert(0, new_head)
                self.food = (random.randint(0, 15), random.randint(0, 15))
                self.move_interval *= 0.95  # Speed up slightly
            else:
                self.snake.insert(0, new_head)
                self.snake.pop()
            
            # Random direction change occasionally
            if random.random() < 0.1:
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                self.direction = random.choice(directions)
            
            self.last_move = current_time
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            intensity = 1.0 - (i / len(self.snake)) * 0.7
            color = (0, int(255 * intensity), 0)
            self.led_matrix.set_pixel(x, y, color)
        
        # Draw food
        self.led_matrix.set_pixel(self.food[0], self.food[1], (255, 0, 0))


class ConwayLife(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        self.grid = np.random.choice([0, 1], size=(16, 16), p=[0.7, 0.3])
        self.last_update = time.time()
        self.update_interval = 0.2
        
    def update(self):
        current_time = time.time()
        if current_time - self.last_update > self.update_interval:
            self.grid = self.next_generation()
            self.last_update = current_time
            
            # Reset if all dead
            if np.sum(self.grid) == 0:
                self.grid = np.random.choice([0, 1], size=(16, 16), p=[0.8, 0.2])
        
        # Draw grid
        self.led_matrix.clear()
        for y in range(16):
            for x in range(16):
                if self.grid[y, x]:
                    # Age-based coloring (simulate with random intensity)
                    intensity = random.uniform(0.5, 1.0)
                    color = (int(255 * intensity), int(255 * intensity), 0)
                    self.led_matrix.set_pixel(x, y, color)
    
    def next_generation(self):
        new_grid = np.zeros_like(self.grid)
        
        for y in range(16):
            for x in range(16):
                # Count neighbors (with wrapping)
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ny, nx = (y + dy) % 16, (x + dx) % 16
                        neighbors += self.grid[ny, nx]
                
                # Conway's rules
                if self.grid[y, x] == 1:  # Alive
                    if neighbors in [2, 3]:
                        new_grid[y, x] = 1
                else:  # Dead
                    if neighbors == 3:
                        new_grid[y, x] = 1
        
        return new_grid


class Tetris(BasePattern):
    def __init__(self, led_matrix):
        super().__init__(led_matrix)
        self.grid = np.zeros((16, 16))
        self.current_piece = self.create_random_piece()
        self.piece_x, self.piece_y = 8, 0
        self.last_drop = time.time()
        self.drop_interval = 1.0
        
    def create_random_piece(self):
        pieces = [
            [[1, 1, 1, 1]],  # I piece
            [[1, 1], [1, 1]],  # O piece
            [[0, 1, 0], [1, 1, 1]],  # T piece
            [[1, 1, 0], [0, 1, 1]],  # S piece
        ]
        return random.choice(pieces)
    
    def update(self):
        current_time = time.time()
        
        # Drop piece
        if current_time - self.last_drop > self.drop_interval:
            if self.can_move(0, 1):
                self.piece_y += 1
            else:
                self.place_piece()
                self.clear_lines()
                self.current_piece = self.create_random_piece()
                self.piece_x, self.piece_y = 8, 0
            
            self.last_drop = current_time
        
        # Random horizontal movement
        if random.random() < 0.1:
            dx = random.choice([-1, 1])
            if self.can_move(dx, 0):
                self.piece_x += dx
        
        # Draw everything
        self.led_matrix.clear()
        
        # Draw placed pieces
        for y in range(16):
            for x in range(16):
                if self.grid[y, x]:
                    self.led_matrix.set_pixel(x, y, (100, 100, 100))
        
        # Draw current piece
        for py, row in enumerate(self.current_piece):
            for px, cell in enumerate(row):
                if cell:
                    x, y = self.piece_x + px, self.piece_y + py
                    if 0 <= x < 16 and 0 <= y < 16:
                        self.led_matrix.set_pixel(x, y, (255, 255, 0))
    
    def can_move(self, dx, dy):
        for py, row in enumerate(self.current_piece):
            for px, cell in enumerate(row):
                if cell:
                    x, y = self.piece_x + px + dx, self.piece_y + py + dy
                    if x < 0 or x >= 16 or y >= 16 or (y >= 0 and self.grid[y, x]):
                        return False
        return True
    
    def place_piece(self):
        for py, row in enumerate(self.current_piece):
            for px, cell in enumerate(row):
                if cell:
                    x, y = self.piece_x + px, self.piece_y + py
                    if 0 <= x < 16 and 0 <= y < 16:
                        self.grid[y, x] = 1
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(16):
            if np.all(self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            self.grid = np.delete(self.grid, y, axis=0)
            self.grid = np.vstack([np.zeros((1, 16)), self.grid])