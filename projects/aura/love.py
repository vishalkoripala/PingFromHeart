import os
import math
import sys
import turtle
import tempfile
import atexit
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

try:
    from PIL import Image
    pillow_available = True
except ImportError:
    pillow_available = False

image_height = 0
image_frames = []

def prepare_image(image_path, max_size=(250, 250)):
    global image_height, image_frames
    image_frames = []
    if not image_path or not os.path.isfile(image_path):
        return None

    is_gif = image_path.lower().endswith(".gif")
    if not pillow_available and not is_gif:
        messagebox.showerror("Image load failed", "Pillow is not installed. Please install Pillow to load non-GIF images.")
        return None

    try:
        if is_gif and not pillow_available:
            image_height = max_size[1]
            return image_path

        fd, temp_path = tempfile.mkstemp(suffix=".gif")
        os.close(fd)
        atexit.register(lambda: os.remove(temp_path) if os.path.exists(temp_path) else None)

        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            img.thumbnail(max_size, Image.LANCZOS)
            image_height = img.height

            black_bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
            alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
            for alpha in alphas:
                faded = Image.blend(black_bg, img, alpha)
                fd2, fade_path = tempfile.mkstemp(suffix=".gif")
                os.close(fd2)
                atexit.register(lambda p=fade_path: os.remove(p) if os.path.exists(p) else None)
                faded.convert("RGB").save(fade_path, format="GIF")
                image_frames.append(fade_path)

            img.save(temp_path, format="GIF")
        return temp_path
    except Exception as exc:
        messagebox.showerror("Image load failed", f"Could not load or convert image: {exc}")
        return None


def draw_heart(points, heart_turtle, screen):
    heart_turtle.penup()
    heart_turtle.goto(points[0])
    heart_turtle.pendown()

    def step(index=0):
        if index < len(points):
            heart_turtle.goto(points[index])
            if index % 5 == 0:
                screen.update()
            screen.ontimer(lambda: step(index + 1), 30)
        else:
            screen.update()
            animate_text(0)

    step()


def animate_text(index=0):
    text_turtle.clear()
    text_turtle.write(message[:index], align="center", font=("Arial", 18, "bold"))
    screen.update()
    if index < len(message):
        screen.ontimer(lambda: animate_text(index + 1), text_speed)
    else:
        if image_file:
            screen.ontimer(show_image, image_delay)


def show_image():
    if image_frames:
        fade_image(0)
    else:
        image_turtle.shape(image_file)
        image_turtle.showturtle()
        screen.update()


def fade_image(index=0):
    if index < len(image_frames):
        image_turtle.shape(image_frames[index])
        image_turtle.showturtle()
        screen.update()
        screen.ontimer(lambda: fade_image(index + 1), 80)
    else:
        if image_file:
            image_turtle.shape(image_file)
            image_turtle.showturtle()
            screen.update()


def register_image_shapes(screen):
    if image_file:
        try:
            screen.addshape(image_file)
        except Exception:
            pass
    for frame in image_frames:
        try:
            screen.addshape(frame)
        except Exception:
            pass


root = tk.Tk()
root.withdraw()

# Allow command-line invocation to skip GUI prompts for deployment.
cli_message = None
cli_image = None
if len(sys.argv) > 1:
    cli_message = sys.argv[1]
    if len(sys.argv) > 2:
        cli_image = sys.argv[2]

if cli_message:
    message = cli_message
else:
    message = simpledialog.askstring("Display Text", "Enter the text to display:")
    if not message:
        message = "I LOVE YOU JAANU💋"

if cli_image:
    image_path = cli_image
else:
    image_path = filedialog.askopenfilename(
        title="Select an image to display in the heart",
        initialdir=os.getcwd(),
        filetypes=[("Image files", "*.gif *.png *.jpg *.jpeg *.bmp *.ico"), ("All files", "*")],
    )
root.destroy()

image_file = prepare_image(image_path) if image_path else None

text_speed = 140
image_delay = 1500

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Aura Love Heart")
screen.tracer(0)
register_image_shapes(screen)

heart_turtle = turtle.Turtle()
heart_turtle.hideturtle()
heart_turtle.color("#ffbcd1")
heart_turtle.pensize(3)
heart_turtle.speed(5)

text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.penup()
text_turtle.color("white")
image_y = 0

text_y = -140 if image_height == 0 else image_y - image_height / 2 - 25
text_turtle.goto(0, text_y)

image_turtle = turtle.Turtle()
image_turtle.hideturtle()
image_turtle.penup()
image_turtle.goto(0, image_y)

points = []
for scale in range(11, 17):
    for i in range(120):
        angle = i * (math.pi * 2) / 120
        x = 16 * (math.sin(angle) ** 3) * scale
        y = (13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle)) * scale
        points.append((x, y))

screen.update()
draw_heart(points, heart_turtle, screen)
turtle.mainloop()