import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw

# App constants
APP_TITLE = "King of Thieves Base Designer"
GRID_WIDTH = 14
GRID_HEIGHT = 8
CELL_SIZE = 80
WHITE = 0
BLACK = 1
CANVAS_BG = "white"
GRID_OUTLINE_COLOR = "gray"


class GridDesigner:
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application"""
        self.root = root
        self.root.title(APP_TITLE)
        self.root.resizable(False, False)
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT
        self.cell_size = CELL_SIZE

        # Grid state: 0 = white, 1 = black
        self.grid = self._create_empty_grid()
        self._create_widgets()


    def _create_widgets(self) -> None:
        """Create and layout the GUI widgets"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        canvas_width = self.grid_width * self.cell_size
        canvas_height = self.grid_height * self.cell_size

        self.canvas = tk.Canvas(
            main_frame,
            width=canvas_width,
            height=canvas_height,
            bg=CANVAS_BG,
            borderwidth=1,
            relief="solid",
        )

        self.canvas.pack(pady=(0, 10))
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self._draw_grid()
        button_frame = tk.Frame(main_frame)
        button_frame.pack()

        tk.Button(button_frame, text="Clear Grid", command=self.clear_grid).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Invert Grid Colors", command=self.invert_grid).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export as Image", command=self.export_image).pack(side=tk.LEFT, padx=5)


    def _create_empty_grid(self) -> list[list[int]]:
        """Create an empty (white) grid."""
        return [[WHITE for _ in range(self.grid_width)] for _ in range(self.grid_height)]


    def _draw_grid(self) -> None:
        """Draw the grid on the canvas."""
        self.canvas.delete("all")

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                fill_color = "black" if self.grid[row][col] == BLACK else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2,
                    fill=fill_color, outline=GRID_OUTLINE_COLOR)


    def _on_canvas_click(self, event: tk.Event) -> None:
        """Toggle cell color on mouse click."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= col < self.grid_width and 0 <= row < self.grid_height:
            self.grid[row][col] = BLACK if self.grid[row][col] == WHITE else WHITE
            self._draw_grid()


    def clear_grid(self) -> None:
        """Reset the grid to all white."""
        self.grid = self._create_empty_grid()
        self._draw_grid()


    def invert_grid(self) -> None:
        """Invert all grid colors."""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                self.grid[row][col] = BLACK if self.grid[row][col] == WHITE else WHITE
        self._draw_grid()


    def export_image(self) -> None:
        """Export the grid as a compressed black & white PNG image."""
        image_width = (self.grid_width + 2) * self.cell_size
        image_height = (self.grid_height + 2) * self.cell_size
        image = Image.new("1", (image_width, image_height), WHITE)
        draw = ImageDraw.Draw(image)

        # Draw outer border (black)
        draw.rectangle([0, 0, image_width - 1, image_height - 1],
            fill=BLACK)

        # Draw grid cells
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                img_x = (col + 1) * self.cell_size
                img_y = (row + 1) * self.cell_size
                
                color = BLACK if self.grid[row][col] == BLACK else WHITE
                draw.rectangle([img_x, img_y, img_x + self.cell_size - 1,
                    img_y + self.cell_size - 1], fill=color)

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save grid as...")

        if file_path:
            image.save(file_path, "PNG", optimize=True)
            messagebox.showinfo("Success",
                f"Image successfully saved:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GridDesigner(root)
    root.mainloop()