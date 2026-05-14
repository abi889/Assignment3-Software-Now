      """
Game Controller
"""

class GameController:
    def __init__(self):
        self.current_image = None
        self.modified_image = None
        self.differences = []
        self.found_count = 0
        self.mistakes = 0
        self.max_mistakes = 3
        self.game_active = True
        self.game_won = False
    
    def set_images(self, original, modified, differences):
        self.current_image = original
        self.modified_image = modified
        self.differences = differences
        self.found_count = 0
        self.mistakes = 0
        self.game_active = True
        self.game_won = False
    
    def check_click(self, x, y, tolerance=25):
        if not self.game_active:
            return False, False, True
        
        for diff in self.differences:
            if not diff['found']:
                rx, ry, rw, rh = diff['region']
                if (rx - tolerance <= x <= rx + rw + tolerance and
                    ry - tolerance <= y <= ry + rh + tolerance):
                    diff['found'] = True
                    self.found_count += 1
                    
                    if self.found_count == len(self.differences):
                        self.game_active = False
                        self.game_won = True
                        return True, True, False
                    return True, False, False
        
        self.mistakes += 1
        if self.mistakes >= self.max_mistakes:
            self.game_active = False
            return False, False, True
        
        return False, False, False
    
    def reveal_all(self):
        revealed = []
        for diff in self.differences:
            if not diff['found']:
                diff['found'] = True
                self.found_count += 1
                revealed.append(diff)
        self.game_active = False
        return revealed
    
    def get_remaining_count(self):
        return len(self.differences) - self.found_count
    
    def get_mistakes_remaining(self):
        return self.max_mistakes - self.mistakes
    
    def is_game_over(self):
        return not self.game_active or self.mistakes >= self.max_mistakes
    
    def reset(self):
        self.differences = []
        self.found_count = 0
        self.mistakes = 0
        self.game_active = True
        self.game_won = False
