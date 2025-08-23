
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
    w_new, h_new = max(1, int(w * scale_pixels)), max(1, int(h * scale_pixels))
    img = img.resize((w_new, h_new), Image.LANCZOS)
    w, h = img.size
    print(f"Downscaled image: {w}x{h} pixels (~{target_lines} lines).")

    max_canvas_w, max_canvas_h = 1000, 500
    pixel_size = max(1, min(max_canvas_w // w, max_canvas_h // h))
    print(f"Pixel size set to {pixel_size} to fit canvas {max_canvas_w}x{max_canvas_h}.")

    pixels = img.load()
    lines = [
        "import turtle",
        "turtle.colormode(255)",
        "turtle.speed(0)",
        "turtle.hideturtle()",
        "turtle.penup()",
        "turtle.tracer(False)"
    ]

    start_x = - (w * pixel_size) // 2
    start_y = (h * pixel_size) // 2

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

                    lines.append(
                        f"turtle.color({last_color[0]},{last_color[1]},{last_color[2]}); "
                        f"turtle.penup(); turtle.goto({px0},{py}); turtle.pendown(); "
                        f"turtle.begin_fill(); turtle.setheading(0); "
                        f"turtle.forward({px1-px0}); turtle.left(90); "
                        f"turtle.forward({pixel_size}); turtle.left(90); "
                        f"turtle.forward({px1-px0}); turtle.left(90); "
                        f"turtle.forward({pixel_size}); turtle.left(90); "
                        f"turtle.end_fill(); turtle.penup()"
                    )
                run_start = x
                last_color = (r, g, b)

        if run_start is not None:
            px0 = start_x + run_start * pixel_size
            px1 = start_x + w * pixel_size
            lines.append(
                f"turtle.color({last_color[0]},{last_color[1]},{last_color[2]}); "
                f"turtle.penup(); turtle.goto({px0},{py}); turtle.pendown(); "
                f"turtle.begin_fill(); turtle.setheading(0); "
                f"turtle.forward({px1-px0}); turtle.left(90); "
                f"turtle.forward({pixel_size}); turtle.left(90); "
                f"turtle.forward({px1-px0}); turtle.left(90); "
                f"turtle.forward({pixel_size}); turtle.left(90); "
                f"turtle.end_fill(); turtle.penup()"
            )

    lines.append("turtle.update(); turtle.done()")
    code = "\n".join(lines)
    pyperclip.copy(code)
    print(f"✅ Clipboard ready! Render size: {w * pixel_size}x{h * pixel_size}, pixel_size = {pixel_size}")

    return code

if __name__ == "__main__":
    genTurtle(input("File place: "), target_lines=600000)

