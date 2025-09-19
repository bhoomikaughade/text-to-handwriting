# ✍️ Text to Handwriting Converter  

The **Text to Handwriting Converter** is a Python project that transforms any typed text into an image that looks like it has been written by hand.  
This project uses **Python Pillow (PIL)** library along with custom handwriting fonts (`.ttf` files) to make digital text appear realistic and handwritten.  

It’s useful for:
- Making assignments look handwritten
- Creating personalized notes
- Fun projects with custom handwriting styles

## 🚀 Features

✅ Convert plain text files into handwriting-style images  
✅ Support for **custom handwriting fonts** (e.g., IndieFlower, PatrickHand)  
✅ Adjustable **font size, page width, and margins**  
✅ Natural handwriting effect using random spacing and angle jitter  
✅ Save the final handwriting as a **PNG image**  
✅ Easy to extend with multiple fonts or export to PDF  

## 📂 Project Structure
text-to-handwriting/
│── text2hand.py # Main Python script
│── handwriting.ttf # Handwriting font file (rename your font to this)
│── PatrickHand-Regular.ttf# Handwriting font file
│── input.txt # Text file containing the content
│── output.png # Generated handwriting-style image
│── README.md # Project documentation

## 🛠️ Requirements

 **Python 3.x** installed  
 **Pillow (PIL)** library  

Install dependencies with:
```bash
pip install pillow
python text2hand.py input.txt output.png --font handwriting.ttf --size 48
python text2hand.py input.txt output1.png --font PatrickHand-Regular.ttf --size 48
python text2hand.py input.txt output.pdf --font handwriting.ttf --size 48  #if you want to create pdf


