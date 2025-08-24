from PIL import Image
import pyperclip
 
def genTurtle(image_path, target_lines=400000):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")

    avg_lines_per_pixel = 6
    max_pixels = target_lines // avg_lines_per_pixel
    total_pixels = w * h
    scale_pixels = min((max_pixels / total_pixels) ** 0.5, 1.0)
    w_new = max(1, int(w * scale_pixels))
    h_new = max(1, int(h * scale_pixels))
    img = img.resize((w_new, h_new), Image.LANCZOS)
    w, h = img.size
    print(f"Downscaled image: {w}x{h} pixels (~{target_lines} lines).")

    max_canvas_w, max_canvas_h = 1000, 500
    pixel_size = max(1, min(max_canvas_w // w, max_canvas_h // h))
    print(f"Pixel size set to {pixel_size} to fit canvas {max_canvas_w}x{max_canvas_h}.")

    pixels = img.load()

    start_x = - (w * pixel_size) // 2
    start_y = (h * pixel_size) // 2

    runs_data = []  # tuples: (x, y, width, height, r, g, b)

    for y in range(h):
        py = start_y - y * pixel_size
        last_color = None
        run_start = None
        for x in range(w):
            r, g, b = pixels[x, y]
            if (r, g, b) != last_color:
                if run_start is not None:
                    px0 = start_x + run_start * pixel_size
                    px1 = start_x + x * pixel_size
                    runs_data.append((px0, py, px1 - px0, pixel_size,
                                      last_color[0], last_color[1], last_color[2]))
                run_start = x
                last_color = (r, g, b)

        if run_start is not None:
            px0 = start_x + run_start * pixel_size
            px1 = start_x + w * pixel_size
            runs_data.append((px0, py, px1 - px0, pixel_size,
                              last_color[0], last_color[1], last_color[2]))

    lines = [
        "import turtle as t",
        "t.colormode(255)",
        "t.speed(0)",
        "t.hideturtle()",
        "t.penup()",
        "t.tracer(False)",
        "",
        "def draw_rect(w, h):",
        "    t.begin_fill()",
        "    for _ in range(2):",
        "        t.forward(w); t.left(90); t.forward(h); t.left(90)",
        "    t.end_fill()",
        "    t.penup()",
        "",
        "def draw_all(runs):",
        "    for x, y, w, h, r, g, b in runs:",
        "        t.color(r, g, b)",
        "        t.penup(); t.goto(x, y); t.setheading(0); t.pendown()",
        "        draw_rect(w, h)",
        "",
        "runs = ["
    ]

    # Add the data compactly
    for (x, y, rw, rh, r, g, b) in runs_data:
        lines.append(f"    ({x}, {y}, {rw}, {rh}, {r}, {g}, {b}),")

    lines += [
        "]",
        "draw_all(runs)",
        "t.update(); t.done()"
    ]

    code = "\n".join(lines)
    try:
        pyperclip.copy(code)
        print(f"Clipboard ready! Render size: {w * pixel_size}x{h * pixel_size}, pixel_size = {pixel_size}")
    except Exception as e:
        print(f\"Couldn't copy to clipboard: {e}\\nStill returning code string.\")

    return code

if __name__ == '__main__':
    genTurtle(input('File place: '), target_lines=600000)
