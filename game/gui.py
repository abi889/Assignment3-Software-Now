"""
Main GUI Application
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

from game.difference import DifferenceGenerator
from game.controller import GameController


class SpotTheDifferenceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spot the Difference Game")
        self.root.geometry("1400x850")
        self.root.configure(bg='#2c3e50')
        
        self.controller = GameController()
        self.diff_generator = DifferenceGenerator()
        
        self.original_photo = None
        self.modified_photo = None
        self.original_image_original = None
        self.modified_image_original = None
        
        self.scale_x_orig = 1
        self.scale_y_orig = 1
        self.scale_x_mod = 1
        self.scale_y_mod = 1
        self.original_offset = None
        self.modified_offset = None
        self.display_width = 550
        self.display_height = 550
        
        self._setup_gui()
    
    def _setup_gui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(title_frame, text="🔍 SPOT THE DIFFERENCE 🔍",
                               font=('Arial', 24, 'bold'),
                               fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.load_btn = tk.Button(control_frame, text="📁 Load Image",
                                  font=('Arial', 12, 'bold'),
                                  bg='#3498db', fg='white',
                                  padx=20, pady=5,
                                  command=self.load_image)
        self.load_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.reveal_btn = tk.Button(control_frame, text="🔍 Reveal All",
                                    font=('Arial', 12, 'bold'),
                                    bg='#e67e22', fg='white',
                                    padx=20, pady=5,
                                    command=self.reveal_differences)
        self.reveal_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        score_frame = tk.Frame(control_frame, bg='#34495e')
        score_frame.pack(side=tk.RIGHT, padx=20)
        
        self.remaining_label = tk.Label(score_frame, 
                                        text="⭐ Remaining: 0",
                                        font=('Arial', 14, 'bold'),
                                        fg='#f1c40f', bg='#34495e')
        self.remaining_label.pack(side=tk.LEFT, padx=15)
        
        self.mistakes_label = tk.Label(score_frame,
                                       text="❌ Mistakes: 0/3",
                                       font=('Arial', 14, 'bold'),
                                       fg='#e74c3c', bg='#34495e')
        self.mistakes_label.pack(side=tk.LEFT, padx=15)
        
        # Images
        images_frame = tk.Frame(self.root, bg='#2c3e50')
        images_frame.pack(pady=20)
        
        original_container = tk.Frame(images_frame, bg='#2c3e50')
        original_container.pack(side=tk.LEFT, padx=20)
        
        original_title = tk.Label(original_container, text="ORIGINAL IMAGE",
                                  font=('Arial', 14, 'bold'),
                                  fg='#2ecc71', bg='#2c3e50')
        original_title.pack()
        
        self.original_canvas = tk.Canvas(original_container, 
                                         width=self.display_width, 
                                         height=self.display_height,
                                         bg='#7f8c8d',
                                         relief=tk.SUNKEN,
                                         bd=3)
        self.original_canvas.pack(pady=5)
        
        modified_container = tk.Frame(images_frame, bg='#2c3e50')
        modified_container.pack(side=tk.RIGHT, padx=20)
        
        modified_title = tk.Label(modified_container, text="MODIFIED IMAGE (Click Here)",
                                  font=('Arial', 14, 'bold'),
                                  fg='#e74c3c', bg='#2c3e50')
        modified_title.pack()
        
        self.modified_canvas = tk.Canvas(modified_container,
                                         width=self.display_width,
                                         height=self.display_height,
                                         bg='#7f8c8d',
                                         relief=tk.SUNKEN,
                                         bd=3,
                                         cursor='hand2')
        self.modified_canvas.pack(pady=5)
        
        self.modified_canvas.bind("<Button-1>", self.on_image_click)
        
        # Status Bar
        self.status_frame = tk.Frame(self.root, bg='#ecf0f1', relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(self.status_frame, text="✅ Ready - Load an image to start!",
                                     font=('Arial', 10),
                                     fg='#2c3e50', bg='#ecf0f1')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if not file_path:
            return
        
        try:
            img = cv2.imread(file_path)
            if img is None:
                raise ValueError("Could not load image")
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            modified_img, differences = self.diff_generator.generate_differences(img)
            
            self.original_image_original = img
            self.modified_image_original = modified_img
            
            self.controller.reset()
            self.controller.set_images(img, modified_img, differences)
            
            self.display_images()
            self.update_score_display()
            self.status_label.config(text="✅ Game started! Find the 5 differences!", fg='#27ae60')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def display_images(self):
        if self.original_image_original is None:
            return
        
        original_resized, self.original_offset = self.resize_with_padding(
            self.original_image_original, self.display_width, self.display_height
        )
        self.original_photo = ImageTk.PhotoImage(image=Image.fromarray(original_resized))
        self.original_canvas.delete("all")
        self.original_canvas.create_image(self.display_width//2, self.display_height//2,
                                          image=self.original_photo)
        
        modified_resized, self.modified_offset = self.resize_with_padding(
            self.modified_image_original, self.display_width, self.display_height
        )
        self.modified_photo = ImageTk.PhotoImage(image=Image.fromarray(modified_resized))
        self.modified_canvas.delete("all")
        self.modified_canvas.create_image(self.display_width//2, self.display_height//2,
                                          image=self.modified_photo)
        
        h_orig, w_orig = self.original_image_original.shape[:2]
        h_mod, w_mod = self.modified_image_original.shape[:2]
        
        _, _, img_w_orig, img_h_orig = self.original_offset
        _, _, img_w_mod, img_h_mod = self.modified_offset
        
        self.scale_x_orig = w_orig / img_w_orig if img_w_orig > 0 else 1
        self.scale_y_orig = h_orig / img_h_orig if img_h_orig > 0 else 1
        self.scale_x_mod = w_mod / img_w_mod if img_w_mod > 0 else 1
        self.scale_y_mod = h_mod / img_h_mod if img_h_mod > 0 else 1
    
    def resize_with_padding(self, image, target_width, target_height):
        h, w = image.shape[:2]
        aspect = w / h
        
        if w > h:
            new_w = target_width - 20
            new_h = int(new_w / aspect)
        else:
            new_h = target_height - 20
            new_w = int(new_h * aspect)
        
        resized = cv2.resize(image, (new_w, new_h))
        
        padded = np.ones((target_height, target_width, 3), dtype=np.uint8) * 128
        y_offset = (target_height - new_h) // 2
        x_offset = (target_width - new_w) // 2
        padded[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        offset = (x_offset, y_offset, new_w, new_h)
        return padded, offset
    
    def on_image_click(self, event):
        if not self.controller.game_active:
            if self.controller.found_count == 5:
                messagebox.showinfo("Game Complete!", "🎉 You found all differences!")
            else:
                messagebox.showinfo("Game Over!", f"😢 Game Over! You made {self.controller.mistakes} mistakes.")
            return
        
        x_offset, y_offset, img_w, img_h = self.modified_offset
        
        if (x_offset <= event.x <= x_offset + img_w and 
            y_offset <= event.y <= y_offset + img_h):
            
            img_x = (event.x - x_offset) * self.scale_x_mod
            img_y = (event.y - y_offset) * self.scale_y_mod
            
            is_match, is_win, is_game_over = self.controller.check_click(img_x, img_y)
            
            if is_match:
                self.draw_all_found_circles()
                self.update_score_display()
                remaining = self.controller.get_remaining_count()
                self.status_label.config(text=f"🎯 Found! {remaining} remaining.", fg='#27ae60')
                
                if is_win:
                    messagebox.showinfo("Victory!", "🎉 You found all 5 differences!")
            
            elif is_game_over:
                self.update_score_display()
                self.draw_all_found_circles()
                messagebox.showinfo("Game Over!", f"😔 Game Over! {self.controller.mistakes} mistakes.")
            
            else:
                self.update_score_display()
                mistakes_left = self.controller.get_mistakes_remaining()
                self.status_label.config(text=f"❌ Wrong! {mistakes_left} mistakes left.", fg='#e74c3c')
    
    def draw_all_found_circles(self):
        self.display_images()
        
        for diff in self.controller.differences:
            if diff['found']:
                self.draw_circle_on_canvas(self.original_canvas, diff['region'], 
                                          self.scale_x_orig, self.scale_y_orig,
                                          self.original_offset, 'red')
                self.draw_circle_on_canvas(self.modified_canvas, diff['region'],
                                          self.scale_x_mod, self.scale_y_mod,
                                          self.modified_offset, 'red')
    
    def draw_circle_on_canvas(self, canvas, region, scale_x, scale_y, offset, color):
        x, y, w, h = region
        x_offset, y_offset, _, _ = offset

        canvas_cx = x / scale_x + x_offset + (w / scale_x) / 2
        canvas_cy = y / scale_y + y_offset + (h / scale_y) / 2
        radius = max(w / scale_x, h / scale_y) / 2
        canvas.create_oval(canvas_cx - radius, canvas_cy - radius,
                          canvas_cx + radius, canvas_cy + radius,
                          outline=color, width=4)
    
    def reveal_differences(self):
        if self.controller.current_image is None:
            messagebox.showinfo("No Image", "Please load an image first!")
            return
        
        if not self.controller.game_active:
            messagebox.showinfo("Game Over", "Game is already over!")
            return
        
        revealed = self.controller.reveal_all()
        
        if revealed:
            self.display_images()
            
            for diff in self.controller.differences:
                color = 'blue' if diff in revealed else 'red'
                self.draw_circle_on_canvas(self.original_canvas, diff['region'],
                                          self.scale_x_orig, self.scale_y_orig,
                                          self.original_offset, color)
                self.draw_circle_on_canvas(self.modified_canvas, diff['region'],
                                          self.scale_x_mod, self.scale_y_mod,
                                          self.modified_offset, color)
            
            self.update_score_display()
            self.root.update()
            messagebox.showinfo("Revealed", f"{len(revealed)} differences revealed in blue.")
    
    def update_score_display(self):
        remaining = self.controller.get_remaining_count()
        mistakes = self.controller.mistakes
        self.remaining_label.config(text=f"⭐ Remaining: {remaining}")
        self.mistakes_label.config(text=f"❌ Mistakes: {mistakes}/{self.controller.max_mistakes}")
    
    def run(self):
        self.root.mainloop()
