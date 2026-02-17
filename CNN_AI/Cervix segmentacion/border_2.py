import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

# pip install pillow
YELLOW = (255, 255, 0)

class DrawZoomPanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dibujar (amarillo) + Zoom + Pan")

        self.img_path = None
        self.base_img = None
        self.img = None
        self.draw = None

        self.zoom = 1.0
        self.min_zoom = 0.2
        self.max_zoom = 8.0

        self.brush = 8
        self.last = None

        top = tk.Frame(root)
        top.pack(fill="x")

        tk.Button(top, text="Abrir imagen", command=self.open_image).pack(side="left", padx=5, pady=5)
        tk.Button(top, text="Guardar", command=self.save_image).pack(side="left", padx=5, pady=5)
        tk.Button(top, text="Borrar todo", command=self.clear).pack(side="left", padx=5, pady=5)

        tk.Label(top, text="Grosor").pack(side="left", padx=(15, 5))
        self.brush_slider = tk.Scale(top, from_=1, to=60, orient="horizontal", command=self.set_brush)
        self.brush_slider.set(self.brush)
        self.brush_slider.pack(side="left")

        tk.Label(top, text="Zoom").pack(side="left", padx=(15, 5))
        self.zoom_label = tk.Label(top, text="100%")
        self.zoom_label.pack(side="left")

        tk.Button(top, text="Zoom +", command=lambda: self.set_zoom(self.zoom * 1.25)).pack(side="left", padx=5)
        tk.Button(top, text="Zoom -", command=lambda: self.set_zoom(self.zoom / 1.25)).pack(side="left", padx=5)
        tk.Button(top, text="Reset", command=lambda: self.set_zoom(1.0)).pack(side="left", padx=5)

        # Contenedor con scrollbars
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(frame, bg="black", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.vbar = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar = tk.Scrollbar(frame, orient="horizontal", command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # Dibujar (click izquierdo)
        self.canvas.bind("<ButtonPress-1>", self.on_down)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_up)

        # Pan (arrastrar con botón derecho)
        self.canvas.bind("<ButtonPress-3>", self.pan_start)
        self.canvas.bind("<B3-Motion>", self.pan_move)

        # Zoom con rueda (y trackpad)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # Windows/Mac
        self.canvas.bind("<Button-4>", self.on_mousewheel)    # Linux up
        self.canvas.bind("<Button-5>", self.on_mousewheel)    # Linux down

        # Pan con teclas (flechas)
        self.root.bind("<Left>",  lambda e: self.pan_keys(-40, 0))
        self.root.bind("<Right>", lambda e: self.pan_keys(40, 0))
        self.root.bind("<Up>",    lambda e: self.pan_keys(0, -40))
        self.root.bind("<Down>",  lambda e: self.pan_keys(0, 40))

        self.tk_img = None
        self.img_item = None

    def set_brush(self, v):
        self.brush = int(v)

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        )
        if not path:
            return
        self.img_path = path
        self.base_img = Image.open(path).convert("RGB")
        self.img = self.base_img.copy()
        self.draw = ImageDraw.Draw(self.img)
        self.zoom = 1.0
        self.update_view(reset_scroll=True)

    def set_zoom(self, new_zoom):
        if self.img is None:
            return
        self.zoom = max(self.min_zoom, min(self.max_zoom, float(new_zoom)))
        self.update_view()

    def update_view(self, reset_scroll=False):
        if self.img is None:
            return
        w, h = self.img.size
        zw, zh = int(w * self.zoom), int(h * self.zoom)
        disp = self.img.resize((zw, zh), Image.Resampling.BILINEAR)

        self.tk_img = ImageTk.PhotoImage(disp)
        if self.img_item is None:
            self.canvas.delete("all")
            self.img_item = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        else:
            self.canvas.itemconfig(self.img_item, image=self.tk_img)

        self.canvas.config(scrollregion=(0, 0, zw, zh))
        self.zoom_label.config(text=f"{int(self.zoom * 100)}%")

        if reset_scroll:
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)

    def canvas_to_image_coords(self, cx, cy):
        ix = int(cx / self.zoom)
        iy = int(cy / self.zoom)
        ix = max(0, min(self.img.size[0] - 1, ix))
        iy = max(0, min(self.img.size[1] - 1, iy))
        return ix, iy

    # --- Dibujo ---
    def on_down(self, event):
        if self.img is None:
            return
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        self.last = self.canvas_to_image_coords(cx, cy)

    def on_move(self, event):
        if self.img is None or self.last is None:
            return
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        cur = self.canvas_to_image_coords(cx, cy)

        self.draw.line((self.last[0], self.last[1], cur[0], cur[1]),
                       fill=YELLOW, width=self.brush)
        self.last = cur
        self.update_view()

    def on_up(self, event):
        self.last = None

    # --- Pan con botón derecho ---
    def pan_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # --- Pan con teclas ---
    def pan_keys(self, dx, dy):
        # dx/dy en pixeles del canvas visible
        self.canvas.xview_scroll(int(dx / 10), "units")
        self.canvas.yview_scroll(int(dy / 10), "units")

    # --- Zoom con rueda ---
    def on_mousewheel(self, event):
        if self.img is None:
            return

        if hasattr(event, "num") and event.num in (4, 5):  # Linux
            factor = 1.15 if event.num == 4 else 1 / 1.15
            self.set_zoom(self.zoom * factor)
            return

        if event.delta > 0:
            self.set_zoom(self.zoom * 1.15)
        else:
            self.set_zoom(self.zoom / 1.15)

    def clear(self):
        if self.base_img is None:
            return
        self.img = self.base_img.copy()
        self.draw = ImageDraw.Draw(self.img)
        self.update_view()

    def save_image(self):
        if self.img is None:
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg")]
        )
        if not out:
            return
        self.img.save(out)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawZoomPanApp(root)
    root.mainloop()
