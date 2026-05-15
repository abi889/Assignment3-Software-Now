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
        overlay = roi.copy()
        overlay[:, :, 2] = np.clip(overlay[:, :, 2] + 120, 0, 255)
        
        cv2.rectangle(
            overlay,
            (5, 5),
            (w - 5, h - 5),
            (255, 255, 255),
            3
        )
        
        image[y:y+h, x:x+w] = overlay
        return image
    
    def get_name(self):
        return "Color Shift"

class BlurStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        kernel_size = random.choice([9, 11])
        blurred = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
        image[y:y+h, x:x+w] = blurred
        return image
    
    def get_name(self):
        return "Blur"

class NoiseStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        noise = np.random.randint(-80, 81, roi.shape, dtype=np.int16)
        noisy = np.clip(roi.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = noisy
        return image
    
    def get_name(self):
        return "Noise"

class BrightnessStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        brightness = random.randint(90, 140)
        brightened = np.clip(roi.astype(np.int16) + brightness, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = brightened
        return image
    
    def get_name(self):
        return "Brightness"

class ContrastStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        alpha = random.uniform(2.0, 3.0)
        contrasted = np.clip(roi.astype(np.float32) * alpha, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = contrasted
        return image
    
    def get_name(self):
        return "Contrast"

class ShapeAdditionStrategy(DifferenceStrategy):
    def apply(self, image, region):
        x, y, w, h = region
        center_x = x + w // 2
        center_y = y + h // 2
        radius = min(w, h) // 4
        color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )
        cv2.circle(
            image,
            (center_x, center_y),
            radius,
            color,
            -1
        )
        return image
    def get_name(self):
        return "Shape Addition"

class DifferenceGenerator:
    def __init__(self):
        self.strategies = [
            ColorShiftStrategy(),
            BlurStrategy(),
            NoiseStrategy(),
            BrightnessStrategy(),
            ContrastStrategy(),
            ShapeAdditionStrategy()
        ]
    
    def generate_non_overlapping_regions(self, image_shape, num_regions=5):
        height, width = image_shape[:2]
        
        min_size = 70
        max_size = 120
        
        margin = 50
        regions = []
        
        attempts = 0
        
        while len(regions) < num_regions and attempts < 500:
            attempts += 1

            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            
            x = random.randint(margin, width - w - margin)
            y = random.randint(margin, height - h - margin)
            
            new_region = (x, y, w, h)
            
            overlap = False
            
            for existing in regions:
                x1, y1, w1, h1 = existing
                
                if not (
                    x + w + 20 < x1 or
                    x1 + w1 + 20 < x or
                    y + h + 20 < y1 or
                    y1 + h1 + 20 < y
                ):
                    overlap = True
                    break
            if not overlap:
                regions.append(new_region)
        
        return regions
    
    
    def generate_differences(self, original_image):
        modified = original_image.copy()
        regions = self.generate_non_overlapping_regions(original_image.shape)
        differences = []
        
        for i, region in enumerate(regions):
            strategy = self.strategies[i % len(self.strategies)]
            modified = strategy.apply(modified, region)
            differences.append({
                'id': i,
                'region': region,
                'strategy': strategy.get_name(),
                'found': False
            })
        
        return modified, differences
           
