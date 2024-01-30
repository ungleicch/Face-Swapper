import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from PIL import ImageFont

def sharpen_highboost(image, alpha=1.5, sigma=1):
    blurred = cv2.GaussianBlur(image, (0, 0), 3)
    highboosted = cv2.addWeighted(image, alpha+1, blurred, -alpha, 0)
    smooth_highboosted = cv2.GaussianBlur(highboosted, (0, 0), sigma)
    return smooth_highboosted

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(320, 320))
swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)

def select_face(img_path, app, msg="Select face"):
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = app.get(img)

    if not faces:
        print("No faces found. Please select another picture.")
        return None

    selected_face = None

    def on_key_press(event):
        nonlocal selected_face
        key = event.char
        if key.isdigit():
            index = int(key)
            if 0 <= index < len(faces):
                selected_face = faces[index]
                root.destroy()

    root = tk.Tk()
    root.title(msg)

    img_pil = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img_pil)
    font_path = "Arial.ttf"
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)

    for idx, face in enumerate(faces):
        bbox = face.bbox.astype(int)
        draw.rectangle([(bbox[0], bbox[1]), (bbox[2], bbox[3])], outline="red", width=2)
        draw.text((bbox[0], bbox[1] - font_size), str(idx), fill="red", font=font)

    photo = ImageTk.PhotoImage(image=img_pil)
    canvas = tk.Canvas(root, width=img.shape[1], height=img.shape[0])
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.bind("<Key>", on_key_press)
    canvas.focus_set()
    root.mainloop()

    return selected_face

def swap_faces(source_img_path, target_img_path, app, swapper):
    source_face = select_face(source_img_path, app, "Select face from image 1 (this is the face that is placed over the other one)")
    if not source_face:
        return

    target_img = cv2.imread(target_img_path)
    target_faces = app.get(target_img)
    if not target_faces:
        print("No faces found in the target image. Process canceled.")
        return

    target_img_preview = target_img.copy()
    for idx, face in enumerate(target_faces):
        bbox = face.bbox.astype(int)
        cv2.rectangle(target_img_preview, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(target_img_preview, str(idx), (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow("Faces in the target image", target_img_preview)
    cv2.waitKey(1)

    def validate_face_indices(face_indices_str, num_faces):
        try:
            indices = [int(idx) for idx in face_indices_str.split(';') if idx.strip()]
            if all(0 <= idx < num_faces for idx in indices):
                return indices
            else:
                messagebox.showerror("Error", "Invalid face indices entered.")
                return None
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please use numbers only.")
            return None

    def apply_swaps(face_indices, apply_sharpening, target_img):
        nonlocal target_img_preview
        for index in face_indices:
            if 0 <= index < len(target_faces):
                target_face = target_faces[index]
                swapped_img = swapper.get(target_img, target_face, source_face, paste_back=True)
                target_img = swapped_img.copy()

                if apply_sharpening:
                    x, y, w, h = target_face.bbox.astype(int).flatten()
                    swapped_face_region = target_img[y:y+h, x:x+w]
                    sharpened_face = sharpen_highboost(swapped_face_region)
                    target_img[y:y+h, x:x+w] = sharpened_face

        cv2.destroyAllWindows()
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if output_path:
            cv2.imwrite(output_path, target_img)

    root = tk.Tk()
    root.title("Exchange faces")

    def on_swap_selected():
        face_indices_str = entry.get()
        face_indices = validate_face_indices(face_indices_str, len(target_faces))
        if face_indices is not None:
            apply_sharpening = sharpen_var.get() == 1
            apply_swaps(face_indices, apply_sharpening, target_img.copy())
            root.destroy()

    def on_swap_all():
        apply_sharpening = sharpen_var.get() == 1
        apply_swaps(range(len(target_faces)), apply_sharpening, target_img.copy())
        root.destroy()

    label = tk.Label(root, text="Enter the numbers of the faces you want to exchange (separated by ';'):")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    sharpen_var = tk.IntVar()
    sharpen_check = tk.Checkbutton(root, text="Apply sharpening", variable=sharpen_var)
    sharpen_check.pack()

    swap_button = tk.Button(root, text="Exchange selected faces", command=on_swap_selected)
    swap_button.pack()

    swap_all_button = tk.Button(root, text="Exchange all faces", command=on_swap_all)
    swap_all_button.pack()

    root.mainloop()

def open_file_dialog(title="Select file"):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title)
    root.destroy()
    return file_path

source_img_path = open_file_dialog("Select source image")
target_img_path = open_file_dialog("Select target image")
if source_img_path and target_img_path:
    swap_faces(source_img_path, target_img_path, app, swapper)
else:
    print("No file selected. Process canceled.")
