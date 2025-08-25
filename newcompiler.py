from PIL import Image
import pyperclip
#from math import *
def genTurtle(image_path, target=400000):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")
    #img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    #img = img.convert("L")  # Convert to grayscale
    #img = img.convert("RGB")
    alpp = 6 #average lines per pix. can 4 be ok?
    maxp = target // alpp #find maxpixel
    #max_pixel = target // avg lines per pix
    total_pixels = w * h 
    scaler = min((maxp / total_pixels) ** 0.5, 1.0) 
    #scaler = min(sqrt((maxp / total_pixels)) , 1.0)
    w_new = max(1, int(w * scaler))
    h_new = max(1, int(h * scaler))
    img = img.resize((w_new, h_new), Image.LANCZOS) #lanczos algorithm.
    w, h = img.size
    print(f"Downscaled image: {w}x{h} pixels (~{target} lines).")

    mcw, mch = 1000, 500 #maxcanvash , maxcanvasw --> turtle req: 1000,500 . scale to fit
    pixel_size = max(1, min(mcw // w, mch // h))
    print(f"Pixel size set to {pixel_size} to fit canvas {mcw}x{mch}.")

    pixels = img.load() #load image

    start_x = - (w * pixel_size) // 2
    start_y = (h * pixel_size) // 2

    runs_data = []  # tuples: (x, y, width, height, r, g, b)
    #NOTE:
    #width height all the same for each one.
    #can remove it??? 
    #it includes run but most cases dont need?
    #note: please use good varsss
    for y in range(h): #iterate through the full height to h-1 
        py = start_y - y * pixel_size #choose starting y coord, NEED TO CENTER IMAGE!!!
        last_color = None
        #last_color = False
        run_start = None
        #run_start = False
        for x in range(w): #iterate through full width to w-1
            r, g, b = pixels[x, y] #access pixels at x,y
            if (r, g, b) != last_color: 
                if run_start is not None: #[r r b b b g g] run 1 red run 2 blue run 3 green
                    px0 = start_x + run_start * pixel_size #starting run pos
                    px1 = start_x + x * pixel_size #ending run pos
                    runs_data.append((px0, py, px1 - px0, pixel_size,
                                      last_color[0], last_color[1], last_color[2])) 
                run_start = x
                last_color = (r, g, b)

        if run_start is not None:
            px0 = start_x + run_start * pixel_size
            px1 = start_x + w * pixel_size
            runs_data.append((px0, py, px1 - px0, pixel_size,
                              last_color[0], last_color[1], last_color[2])) #single pixel

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
        lines.append(f"    ({x}, {y}, {rw}, {rh}, {r}, {g}, {b}),") #x,y,rw,rh,r,g,b

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
        print(f"Couldn't copy to clipboard: {e}\\nStill returning code string.") 
        #error for character not found if wrongly typed
        

    return code

if __name__ == '__main__':
    genTurtle(input('File place: '), target=600000)
