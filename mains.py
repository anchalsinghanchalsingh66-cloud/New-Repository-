# Visiting Card Scanner GUI

import os
import shutil
from tkinter import *
import tkinter.messagebox as tmsg
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def find_tesseract():
    path = shutil.which("tesseract")
    if path:
        return path
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None

root = Tk()
root.geometry("900x600")
root.minsize(700, 520)
root.title("Visiting Card Scanner")

filename = None
preview_img_ref = None
os.makedirs("Database", exist_ok=True)

tess_path = find_tesseract()
if tess_path:
    pytesseract.pytesseract.tesseract_cmd = tess_path
else:
    tmsg.showwarning(
        "Tesseract not found",
        "Install Tesseract OCR engine first.\n"
        "Default path: C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )

def upload_file():
    global filename, preview_img_ref
    home = os.path.expanduser("~")
    filename = filedialog.askopenfilename(
        initialdir=home,
        title="Select a card image",
        filetypes=[
                  ("All Image Files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                   ("JPEG", "*.jpg *.jpeg"),
                   ("PNG", "*.png"),
                  ("All files", "*.*"),
]
    )
    if not filename:
        p_label_var.set("You have not selected any image.")
        l.config(fg="red")
        return

    p_label_var.set("Image uploaded successfully")
    l.config(fg="#0CDD19")
    try:
        img = Image.open(filename)
        img.thumbnail((500, 300))
        preview_img_ref = ImageTk.PhotoImage(img)
        preview_label.config(image=preview_img_ref)
        preview_label_text.config(text=os.path.basename(filename))
    except Exception as e:
        preview_label.config(image="")
        preview_label_text.config(text="")
        tmsg.showerror("Error", f"Could not open image:\n{e}")

def extract_details(text):
    import re

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # EMAIL
    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)

    # PHONE
    phones = re.findall(r'\+?\d[\d\s\-]{8,}\d', text)

    # NAME (smart logic)
    name = "Not found"
    for line in lines:
        if not any(word in line.lower() for word in ["email", "www", "phone", "+"]):
            if len(line.split()) <= 4:
                name = line
                break

    return name, phones, emails

def convert():
    if not filename:
        t.delete("1.0", END)
        t.insert("1.0", "You have not provided any image to convert.")
        tmsg.showwarning("Alert!", "Please upload an image first.")
        return

    if not shutil.which("tesseract") and not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        tmsg.showwarning("Tesseract not found", "Please install the Tesseract OCR engine first.")
        return

    try:
        c_label_var.set("Processing...")
        root.update_idletasks()
        img = Image.open(filename).convert("L")
        text = pytesseract.image_to_string(img)
        # 🔥 Extract details
        name, phones, emails = extract_details(text)


        result = f"""
          Name: {name}
          Phone: {phones[0] if phones else "Not found"}
          Email: {emails[0] if emails else "Not found"}



         Full Text:
          {text}
         """

        t.delete("1.0", END)
        t.insert("1.0", result)
        base = os.path.splitext(os.path.basename(filename))[0]
        out_path = os.path.join("Database", f"{base}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        c_label_var.set(f"Saved: {out_path}")
    except Exception as e:
        t.delete("1.0", END)
        t.insert("1.0", "Conversion failed.")
        tmsg.showerror("Error", f"Conversion failed:\n{e}")

mainmenu = Menu(root)
mainmenu.config(font=("Times", 12))

m1 = Menu(mainmenu, tearoff=0)
m1.add_command(label="Scan/Upload Visiting or Business cards and get the text", font=("Times", 11))
mainmenu.add_cascade(label="Aim", menu=m1)

m2 = Menu(mainmenu, tearoff=0)
m2.add_command(label="|| Diploma in IT Student ||", font=("Times", 11))
m2.add_command(label="|| Python + OCR (Tesseract) ||", font=("Times", 11))
mainmenu.add_cascade(label="About", menu=m2)

m3 = Menu(mainmenu, tearoff=0)
m3.add_command(label="E-mail: anchalsingh@gmail.com", font=("Times", 11))
m3.add_separator()
m3.add_command(label="Developer: Anchal Singh", font=("Times", 11))
mainmenu.add_cascade(label="7398094040", menu=m3)
root.config(menu=mainmenu)

Label(text="Visiting Card Scanner", bg="#FAD2B8", fg="#39322D", font=("Times", 18, "bold")).pack(fill="x")
Label(text="Python + Tkinter + Tesseract OCR", bg="#FAD2B8", fg="#39322D", font=("Times New Roman", 12, "italic")).pack(fill="x")

f1 = Frame(root, bg="white")
f1.pack(pady=10, fill="x")
Label(f1, text="Browse photo to upload", width=25, font=("Times", 14), bg="white").pack(side="left", padx=10)
Label(f1, text="Formats: JPG/PNG/JPEG/BMP/WEBP", bg="white", width=35).pack(side="left", padx=5)
Button(f1, text="Upload card", bg="#F58D4B", font=("Times", 14), width=20, command=upload_file).pack(side="right", padx=10)

p_label_var = StringVar(value="Please upload an image to scan")
l = Label(root, textvariable=p_label_var, fg="red", bg="white")
l.pack(fill="x")

preview_frame = Frame(root, bg="#f7f7f7", bd=1, relief="sunken")
preview_frame.pack(padx=10, pady=5, fill="both", expand=True)
preview_label = Label(preview_frame, bg="#f7f7f7")
preview_label.pack(pady=6)
preview_label_text = Label(preview_frame, text="", bg="#f7f7f7", fg="#333")
preview_label_text.pack()

Button(root, text="Scan and Convert", bg="#F58D4B", font=("Times", 15), width=25, command=convert).pack(pady=8)

c_label_var = StringVar(value="Ready for conversion")
Label(root, textvariable=c_label_var, anchor="w").pack(fill="x")

t = Text(root, height=9, font=("Times", 13))
t.pack(side="bottom", fill="x", padx=8, pady=6)
t.insert("1.0", "Text of converted card will be shown here...")

# ================= FOOTER =================
footer = Frame(root, bg="#3f3f46", height=30)
footer.pack(fill=X, side=BOTTOM)

footer_label = Label(
    footer,
    text="Developer: Anchal Singh      © 2025",
    font=("Times", 10, "italic"),
    bg="#3f3f46",
    fg="white"
)
footer_label.pack(pady=5)
root.mainloop()