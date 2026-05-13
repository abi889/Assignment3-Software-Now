"""
Difference generation strategies
"""

from abc import ABC, abstractmethod
import cv2
import numpy as np
import random

class DifferenceStrategy(ABC):
    @abstractmethod
    def apply(self, image, region):
        pass
    
    @abstractmethod
    def get_name(self):
        pass

class ColorShiftStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w].copy()
        shift = random.randint(30, 80)
        channel = random.randint(0, 2)
        roi[:, :, channel] = np.clip(roi[:, :, channel] + shift, 0, 255)
        image[y:y+h, x:x+w] = roi
        return image
    
    def get_name(self):
        return "Color Shift"

class BlurStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        kernel_size = random.choice([3, 5])
        blurred = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
        image[y:y+h, x:x+w] = blurred
        return image
    
    def get_name(self):
        return "Blur"

class NoiseStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        noise = np.random.randint(-30, 31, roi.shape, dtype=np.int16)
        noisy = np.clip(roi.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = noisy
        return image
    
    def get_name(self):
        return "Noise"

class BrightnessStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        brightness = random.randint(40, 80)
        brightened = np.clip(roi.astype(np.int16) + brightness, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = brightened
        return image
    
    def get_name(self):
        return "Brightness"

class ContrastStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        alpha = random.uniform(1.3, 1.8)
        contrasted = np.clip(roi.astype(np.float32) * alpha, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = contrasted
        return image
    
    def get_name(self):
        return "Contrast"

class DifferenceGenerator:
    def __init__(self):
        self.strategies = [
            ColorShiftStrategy(),
            BlurStrategy(),
            NoiseStrategy(),
            BrightnessStrategy(),
            ContrastStrategy()
        ]
    
    def generate_non_overlapping_regions(self, image_shape, num_regions=5):
        height, width = image_shape[:2]
        min_size = 30
        max_size = min(50, width // 3, height // 3)
        regions = []
        
        for _ in range(num_regions):
            for _ in range(100):
                w = random.randint(min_size, max_size)
                h = random.randint(min_size, max_size)
                x = random.randint(0, width - w)
                y = random.randint(0, height - h)
                new_region = (x, y, w, h)
                
                overlap = False
                for existing in regions:
                    x1, y1, w1, h1 = existing
                    if not (x + w + 15 < x1 or x1 + w1 + 15 < x or
                           y + h + 15 < y1 or y1 + h1 + 15 < y):
                        overlap = True
                        break
                
                if not overlap:
                    regions.append(new_region)
                    break
            else:
                regions.append((random.randint(0, width-4), random.randint(0, height-4), 30, 30))
        
        return regions
    
    def generate_differences(self, original_image):
        modified = original_image.copy()
        regions = self.generate_non_overlapping_regions(original_image.shape)
        differences = []
        
        for i, region in enumerate(regions):
            strategy = random.choice(self.strategies)
            modified = strategy.apply(modified, region)
            differences.append({
                'id': i,
                'region': region,
                'strategy': strategy.get_name(),
                'found': False
            })
        
        return modified, differences