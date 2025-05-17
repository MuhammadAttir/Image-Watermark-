from tkinter import *
from tkinter import filedialog,messagebox
from PIL import Image, ImageTk,ImageDraw,ImageFont

window=Tk()
window.geometry('800x900')  # Taller height
window.config(bg='#2e2e2e')
window.title('Image Watermark App')

# Global variables
img = None
image_path = ""
canvas_width, canvas_height = 500, 350
FILE_TYPES = [("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("GIF", "*.gif")]

#----------------------------------------------Other Functions--------------------------------------------------------------

# Font for Watermark
def get_font(size=70):
    try:
        return ImageFont.truetype("arialbd.ttf", size)  # 'arialbd.ttf' is Arial Bold
    except:
        try:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()

# Position For Watermark``
def draw_centered_text(image, text, font, fill=(255, 0, 0)):
    draw = ImageDraw.Draw(image)

    # Use getbbox for accurate text dimensions
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img_width, img_height = image.size
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2
    draw.text((x, y), text, font=font, fill=fill)



#----------------------------------------------Command Functions--------------------------------------------------------------

def upload_image():
    global img ,image_path,canvas_width, canvas_height,FILE_TYPES
    
    image_path=filedialog.askopenfilename(title='Select a File',filetypes=FILE_TYPES)
    
    if image_path:

        img=Image.open(image_path)
        display_image=img.copy()
        display_image.thumbnail((canvas_width,canvas_height))
        
        upload_img = ImageTk.PhotoImage(display_image)
        
        # Adjsuting Canvas Image
        x=(canvas_width-display_image.width)//2
        y=(canvas_height-display_image.height)//2
        
        canvas.image = upload_img
        canvas.delete('all')
        canvas.create_image(x,y,anchor=NW,image=upload_img)
    else:
        messagebox.showerror(title='Incorrect Path or Format', message='Please correct the format or path for the image.')
        return
    
def add_watermark():
    global img, image_path

    if not image_path:
        messagebox.showerror("Error", "No Image Uploaded.")
        return

    watermark_text = text.get()
    if not watermark_text.strip():
        messagebox.showerror("Input Error", "Please enter a watermark text.")
        return
       
    display_img = img.copy()
    display_img.thumbnail((canvas_width, canvas_height))
    
    # Use centered watermark function
    font = get_font()
    draw_centered_text(display_img, watermark_text, font, fill=(255, 102, 0))

    x = (canvas_width - display_img.width) // 2
    y = (canvas_height - display_img.height) // 2

    upload_img = ImageTk.PhotoImage(display_img)
    canvas.image = upload_img
    canvas.delete('all')
    canvas.create_image(x, y, anchor=NW, image=upload_img)

def save_image():
    global img, image_path, FILE_TYPES

    if not image_path:
        messagebox.showerror("Error", "No image uploaded.")
        return
    
    watermark_text = text.get()
    if not watermark_text.strip():
        messagebox.showerror("Input Error", "Please enter watermark text.")
        return

    watermark_img = img.copy()
    font = get_font(135)
    draw_centered_text(watermark_img, watermark_text, font, fill=(255, 0, 0))

    save_path = filedialog.asksaveasfilename(
        filetypes=FILE_TYPES,
        title='Save Watermark Image',
        defaultextension='.png')
    
    if save_path:
        try:
            watermark_img.save(save_path)
            messagebox.showinfo("Success", f"Image saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{e}")

#-----------------------------------------------Main UI--------------------------------------------------------------

# App Label
title_label=Label(text='💧 Image Watermark Tool',
                font=("Segoe UI", 18, "bold"),
                bg='#2e2e2e',
                fg='white')
title_label.pack(pady=10)

#Upload Button
upload_btn=Button(text='Upload Image',
                font=("Helvetica", 16, "italic"),
                bg='green',
                fg='white',
                width=15,
                height=2,
                activebackground='green',
                command=upload_image)
upload_btn.pack(pady=20)

# Canvas to show image
canvas = Canvas(window, width=500, height=350, bg='#4d4d4d', highlightthickness=2, highlightbackground="white")
canvas.pack(pady=10)

# Text Entry
text=Entry(width=50,font=("Arial", 14))
text.insert(0,'')
text.pack(pady=15,ipady=5)

#Frame
btn_frame=Frame(window,bg='#2e2e2e')
btn_frame.pack(pady=10)

# Add Watermark Button
watermark_btn=Button(btn_frame,text='Add Watermark',
                font=("Helvetica", 16, "italic"),
                bg='green',
                fg='white',
                width=15,
                height=2,
                activebackground='green',
                command=add_watermark)
watermark_btn.pack(side=LEFT,pady=15,padx=20)

# Save Image Button
save_btn=Button(btn_frame,text='Save Image',
                font=("Helvetica", 16, "italic"),
                bg='green',
                fg='white',
                width=15,
                height=2,
                activebackground='green',
                command=save_image)
save_btn.pack(pady=15,padx=20,side=RIGHT)

window.mainloop()