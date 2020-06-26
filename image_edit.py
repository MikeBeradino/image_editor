from tkinter import *
import PIL.Image
from PIL import ImageTk
from PIL import ImageOps
from PIL import ImageEnhance
from tkinter.filedialog import *
import tkinter.messagebox
import imghdr
from PIL import ImageDraw
from collections import *
import center_tk_window
import os
import numpy as np

################ DRAW ################
def drawOnImage(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = True
    drawWindow = Toplevel(canvas.data.mainWindow)
    drawWindow.title = "Draw"

    drawFrame = Frame(drawWindow)
    redButton = Button(drawFrame, bg="red", width=2, \
                       command=lambda: colourChosen(drawWindow, canvas, "red"))
    redButton.grid(row=0, column=0)
    blueButton = Button(drawFrame, bg="blue", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "blue"))
    blueButton.grid(row=0, column=1)
    greenButton = Button(drawFrame, bg="green", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "green"))
    greenButton.grid(row=0, column=2)
    magentaButton = Button(drawFrame, bg="magenta", width=2, \
                           command=lambda: colourChosen(drawWindow, canvas, "magenta"))
    magentaButton.grid(row=1, column=0)
    cyanButton = Button(drawFrame, bg="cyan", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "cyan"))
    cyanButton.grid(row=1, column=1)
    yellowButton = Button(drawFrame, bg="yellow", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "yellow"))
    yellowButton.grid(row=1, column=2)
    orangeButton = Button(drawFrame, bg="orange", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "orange"))
    orangeButton.grid(row=2, column=0)
    purpleButton = Button(drawFrame, bg="purple", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "purple"))
    purpleButton.grid(row=2, column=1)
    brownButton = Button(drawFrame, bg="brown", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "brown"))
    brownButton.grid(row=2, column=2)
    blackButton = Button(drawFrame, bg="black", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "black"))
    blackButton.grid(row=3, column=0)
    whiteButton = Button(drawFrame, bg="white", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "white"))
    whiteButton.grid(row=3, column=1)
    grayButton = Button(drawFrame, bg="gray", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "gray"))
    grayButton.grid(row=3, column=2)
    drawFrame.pack(side=BOTTOM)
    center_tk_window.center_on_screen(drawWindow)

def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image != None:
        canvas.data.drawColour = colour
        canvas.data.mainWindow.bind("<B1-Motion>", \
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()

def drawDraw(event, canvas):
    if canvas.data.drawOn == True:
        x = int(round((event.x - canvas.data.imageTopX) * canvas.data.imageScale))
        y = int(round((event.y - canvas.data.imageTopY) * canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=canvas.data.drawColour, \
                     outline=None)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)
######################## FEATURES ###########################
def closeHistWindow(canvas):
    canvas.data.histWindowClose = True

def histogram(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    histWindow = Toplevel(canvas.data.mainWindow)
    histWindow.title("Histogram")
    histWindow.configure(background='gray20')

    canvas.data.histCanvasWidth = 350
    canvas.data.histCanvasHeight = 200
    histCanvas = Canvas(histWindow, width=canvas.data.histCanvasWidth, height=canvas.data.histCanvasHeight, background="gray50")

    histCanvas.pack()


    redSlider = Scale(histWindow, from_=0, to=2, resolution = .1 , length=200, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                       bg="gray20",
                       fg="lime green",
                       highlightbackground="gray", activebackground="deep sky blue", troughcolor="Red", label="RED")
    redSlider.set(1)
    #redSlider.grid(row=1, column=0, sticky=N)
    redSlider.pack()
    
    greenSlider = Scale(histWindow, from_=0, to=2, resolution = .1 ,length=200, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                         bg="gray20",
                         fg="lime green",
                         highlightbackground="gray", activebackground="deep sky blue", troughcolor="Green", label="GREEN")
    #greenSlider.grid(row=2, column=0, sticky=S)
    greenSlider.set(1)
    greenSlider.pack()
    blueSlider = Scale(histWindow, from_=0, to=2, resolution = .1 ,length=200, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                        bg="gray20",
                        fg="lime green",
                        highlightbackground="gray", activebackground="deep sky blue", troughcolor="Blue",label="BLUE")
    #blueSlider.grid(row=3, column=0)
    blueSlider.set(1)
    blueSlider.pack()

    OkHistFrame = Frame(histWindow)
    OkHistButton = Button(OkHistFrame, text="OK",command=lambda: canvas.after(200, lambda: changeColours(canvas, redSlider,blueSlider, greenSlider, histWindow, histCanvas, initialRGB)),background="gray20",fg="lime green",font=('Helvetica', '8'),)

    OkHistButton.grid(row=1, column=1)
    OkHistFrame.pack(side=RIGHT)
    initialRGB = (1, 1, 1)
    center_tk_window.center_on_screen(histWindow)
    changeColours(canvas, redSlider, blueSlider,greenSlider, histWindow, histCanvas, initialRGB)

def changeColours(canvas, redSlider, blueSlider,greenSlider, histWindow, histCanvas, previousRGB):
    if canvas.data.histWindowClose == True:
        histWindow.destroy()
        canvas.data.histWindowClose = False
    else:

        if canvas.data.image != None and histWindow.winfo_exists():
            sliderValR = redSlider.get()
            sliderValG = greenSlider.get()
            sliderValB = blueSlider.get()
            Matrix = (float(sliderValR), 0, 0,0,
                      0, float(sliderValG), 0, 0,
                      0, 0, float(sliderValB), 0)
            # Apply transform and save
            canvas.data.image = canvas.data.image.convert("RGB", Matrix)
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
            displayHistogram(canvas, histWindow, histCanvas)

def displayHistogram(canvas, histWindow, histCanvas):
    histCanvasWidth = canvas.data.histCanvasWidth
    histCanvasHeight = canvas.data.histCanvasHeight
    margin = 50
    if canvas.data.image != None:
        histCanvas.delete(ALL)
        im = canvas.data.image
        # x-axis
        histCanvas.create_line(margin - 1, histCanvasHeight - margin + 1, \
                               margin - 1 + 258, histCanvasHeight - margin + 1)
        xmarkerStart = margin - 1
        for i in range(0, 257, 64):
            xmarker = "%d" % (i)
            histCanvas.create_text(xmarkerStart + i, \
                                   histCanvasHeight - margin + 7, text=xmarker)
        # y-axis
        histCanvas.create_line(margin - 1, \
                               histCanvasHeight - margin + 1, margin - 1, margin)
        ymarkerStart = histCanvasHeight - margin + 1
        for i in range(0, histCanvasHeight - 2 * margin + 1, 50):
            ymarker = "%d" % (i)
            histCanvas.create_text(margin - 1 - 10, \
                                   ymarkerStart - i, text=ymarker)

        R, G, B = im.histogram()[:256], im.histogram()[256:512], \
                  im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo = R[i]
            histCanvas.create_oval(i + margin, \
                                   histCanvasHeight - pixelNo / 100.0 - 1 - margin, i + 2 + margin, \
                                   histCanvasHeight - pixelNo / 100.0 + 1 - margin, \
                                   fill="red", outline="red")
        for i in range(len(G)):
            pixelNo = G[i]
            histCanvas.create_oval(i + margin, \
                                   histCanvasHeight - pixelNo / 100.0 - 1 - margin, i + 2 + margin, \
                                   histCanvasHeight - pixelNo / 100.0 + 1 - margin, \
                                   fill="green", outline="green")
        for i in range(len(B)):
            pixelNo = B[i]
            histCanvas.create_oval(i + margin, \
                                   histCanvasHeight - pixelNo / 100.0 - 1 - margin, i + 2 + margin, \
                                   histCanvasHeight - pixelNo / 100.0 + 1 - margin, \
                                   fill="blue", outline="blue")

def colourPop(canvas):
    canvas.data.cropPopToHappen = False
    canvas.data.colourPopToHappen = True
    canvas.data.drawOn = False
    tkinter.messagebox.showinfo(title="Colour Pop", message="Click on a part of the image which you want in colour",
                                parent=canvas.data.mainWindow)
    if canvas.data.cropPopToHappen == False:

        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: getPixel(event, canvas))

def getPixel(event, canvas):

    try:

        if canvas.data.colourPopToHappen == True and \
                canvas.data.cropPopToHappen == False and canvas.data.image != None:
            data = []

            canvas.data.pixelx = \
                int(round((event.x - canvas.data.imageTopX) * canvas.data.imageScale))
            canvas.data.pixely = \
                int(round((event.y - canvas.data.imageTopY) * canvas.data.imageScale))
            pixelr, pixelg, pixelb = \
                canvas.data.image.getpixel((canvas.data.pixelx, canvas.data.pixely))

            tolerance = 60
            for y in range(canvas.data.image.size[1]):
                for x in range(canvas.data.image.size[0]):
                    r, g, b = canvas.data.image.getpixel((x, y))
                    avg = int(round((r + g + b) / 3.0))

                    if (abs(r - pixelr) > tolerance or
                            abs(g - pixelg) > tolerance or
                            abs(b - pixelb) > tolerance):
                        R, G, B = avg, avg, avg
                    else:
                        R, G, B = r, g, b
                    data.append((R, G, B))
            canvas.data.image.putdata(data)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
    except:
        pass
    canvas.data.colourPopToHappen = False

def crop(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.drawOn = False
    # have to check if crop button is pressed or not, otherwise,
    # the root events which point to
    # different functions based on what button has been pressed
    # will get mixed up
    canvas.data.cropPopToHappen = True
    tkinter.messagebox.showinfo(title="Crop", \
                                message="Draw cropping rectangle and press Enter", \
                                parent=canvas.data.mainWindow)
    if canvas.data.image != None:
        canvas.data.mainWindow.bind("<ButtonPress-1>", \
                                    lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>", \
                                    lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", \
                                    lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    # detects the start of the crop rectangle
    if canvas.data.endCrop == False and canvas.data.cropPopToHappen == True:
        canvas.data.startCropX = event.x
        canvas.data.startCropY = event.y

def drawCrop(event, canvas):
    # keeps extending the crop rectange as the user extends
    # his desired crop rectangle
    if canvas.data.endCrop == False and canvas.data.cropPopToHappen == True:
        canvas.data.tempCropX = event.x
        canvas.data.tempCropY = event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                canvas.data.tempCropX, \
                                canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

def endCrop(event, canvas):
    # set canvas.data.endCrop=True so that button pressed movements
    # are not caught anymore but set it to False when "Enter"
    # is pressed so that crop can be performed another time too
    if canvas.data.cropPopToHappen == True:
        canvas.data.endCrop = True
        canvas.data.endCropX = event.x
        canvas.data.endCropY = event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                canvas.data.endCropX, \
                                canvas.data.endCropY, fill="gray", stipple="gray12", width=0)
        canvas.data.mainWindow.bind("<Return>", \
                                    lambda event: performCrop(event, canvas))

def performCrop(event, canvas):
    canvas.data.image = \
        canvas.data.image.crop( \
            (int(round((canvas.data.startCropX - canvas.data.imageTopX) * canvas.data.imageScale)),
             int(round((canvas.data.startCropY - canvas.data.imageTopY) * canvas.data.imageScale)),
             int(round((canvas.data.endCropX - canvas.data.imageTopX) * canvas.data.imageScale)),
             int(round((canvas.data.endCropY - canvas.data.imageTopY) * canvas.data.imageScale))))
    canvas.data.endCrop = False
    canvas.data.cropPopToHappen = False
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk = makeImageForTk(canvas)
    drawImage(canvas)

def apply(canvas):
        save(canvas)


def Split_image_CMYK(canvas):
    if canvas.data.image != None:
        threshold_val = Edge_slider.get()
        int_threshold_val = int(threshold_val)
        #### make directory to pack image stack in
        nospace_tail = tail.replace(" ", "")
        dirName = str(nospace_tail.split(".")[0])
        path = os.getcwd()
        absolute_path = ("/"+path+"/" + dirName)
        try:
            os.mkdir( absolute_path)
        except FileExistsError:
            print("Directory ", dirName, " already exists")
        ##############################################
        #gets file that is selected
        img = canvas.data.image
        #need to check how many chanels are presetn
        px = img.load()
        chanel_numb = len(px[0,0])
        #if 4 chanels are avalible check if val is 0
        if chanel_numb == 4:
                ##############################################
                ##############################################
                #black
                ##############################################
                ##############################################
                img= img.convert('RGBA')
                data = np.array(img)  # "data" is a height x width x 4 numpy array
                red_temp, green_temp, blue_temp, alpha_temp = data.T  # Temporarily unpack the bands for readability
                black = (red_temp <= int_threshold_val) & (blue_temp <= int_threshold_val) & (green_temp <= int_threshold_val)
                data[..., :-1][black.T] = (0, 0, 0)  # Transpose back needed
                white = (red_temp >= int_threshold_val) | (blue_temp >= int_threshold_val) | (green_temp >= int_threshold_val)
                data[..., :-1][white.T] = (255, 255, 255)  # Transpose back needed
                for i in range (255):
                    gray = (red_temp == int(i) ) & (blue_temp == int(i)) & (green_temp == int(i))
                    data[..., :-1][gray.T] = (int(i),int(i), int(i))  # Transpose back needed
                black_img = PIL.Image.fromarray(data)
                black_img.show()
                ##############################################
                ##############################################
                #cmy
                ##############################################
                ##############################################
                data_clean = np.array(img)  # "data" is a height x width x 4 numpy array
                red_temp, green_temp, blue_temp, alpha_temp = data_clean.T  # Temporarily unpack the bands for readability
                black_clean = (red_temp <= int_threshold_val) & (blue_temp <= int_threshold_val) & (green_temp <= int_threshold_val)
                data_clean[..., :-1][black_clean.T] = (255, 255, 255)  # Transpose back needed
                for i in range (255):
                    gray = (red_temp == int(i) ) & (blue_temp == int(i)) & (green_temp == int(i))
                    data_clean[..., :-1][gray.T] = (255,255, 255)  # Transpose back needed
                clean_img = PIL.Image.fromarray(data_clean)
                clean_img.show()
                ##############################################
                ##############################################
                #gray
                ##############################################
                ##############################################
                data_gray = np.array(img)  # "data" is a height x width x 4 numpy array
                red_temp2, green_temp2, blue_temp2, alpha_temp2 = data_gray.T  # Temporarily unpack the bands for readability
                for i in range (255):
                    print("here")
                    gray = (red_temp2 == int(i) ) & (blue_temp2 == int(i)) & (green_temp2 == int(i))
                    data_gray[..., :-1][gray.T] = (int(i),int(i), int(i))  # Transpose back needed
                no_cmyk = (red_temp2 != blue_temp2) | (blue_temp2 != green_temp2) | (red_temp2 != green_temp2)
                data_gray[..., :-1][no_cmyk.T] = (255,255,255)  # Transpose back needed
                black_clean = (red_temp2 <= int_threshold_val) & (blue_temp2 <= int_threshold_val) & (green_temp2 <= int_threshold_val)
                data_gray[..., :-1][black_clean.T] = (255, 255, 255)  # Transpose back needed
                gray_img  = PIL.Image.fromarray(data_gray)
                gray_img.show()
                ##############################################
                ##############################################
                red, green, blue, black = clean_img.convert('CMYK').split()

        if chanel_numb != 4:
            tkinter.messagebox.showinfo("ERROR", "Please use a 4 channel image")

        if chanel_numb ==4:
            im_invert = ImageOps.invert(red)
            im_invert.save(absolute_path+'/'+dirName+'-cyan.tiff')
            im_invert = ImageOps.invert(green)
            im_invert.save(absolute_path+'/'+dirName+'-magenta.tiff')
            im_invert = ImageOps.invert(blue)
            im_invert.save(absolute_path+'/'+dirName+'-yellow.tiff')
            black_img.save(absolute_path+'/'+dirName+'-black.tiff')
            gray_img.save(absolute_path+'/'+dirName+'-gray.tiff')

def rotate(canvas):

    if canvas.data.image != None:
        angel = rotate_slider.get()
        canvas.data.image = canvas.data.image.rotate(float(angel))
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def Sharpness(canvas):
    print("sharp")
    if canvas.data.image != None:
        enhancer = ImageEnhance.Sharpness(canvas.data.image)
        sharp_val = Sharpness_slider.get()
        canvas.data.image =enhancer.enhance(float(sharp_val))
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def Contrast(canvas):
    print("conrast")
    if canvas.data.image != None:
        enhancer = ImageEnhance.Contrast(canvas.data.image)
        contarst_val = Contrast_slider.get()
        canvas.data.image =enhancer.enhance(float(contarst_val))
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def Color_shift(canvas):
    print("bright")
    if canvas.data.image != None:
        enhancer = ImageEnhance.Color(canvas.data.image)
        color_val = Color_slider.get()
        canvas.data.image = enhancer.enhance(float(color_val))
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def brightness(canvas):
    print("bright")
    if canvas.data.image != None:
        enhancer = ImageEnhance.Brightness(canvas.data.image)
        bright_val = bright_slider.get()
        canvas.data.image =enhancer.enhance(float(bright_val))
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def reset(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    ### change back to original image
    if canvas.data.image != None:
        canvas.data.image = canvas.data.originalImage.copy()
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def mirror(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.mirror(canvas.data.image)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def flip(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.flip(canvas.data.image)

        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def transpose(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    # I treated the image as a continuous list of pixel values row-wise
    # and simply excnaged the rows and the coloums
    # in oder to make it rotate clockewise, I reversed all the rows
    if canvas.data.image != None:
        imageData = list(canvas.data.image.getdata())
        newData = []
        newimg = PIL.Image.new(canvas.data.image.mode, \
                           (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in range(canvas.data.image.size[0]):
            addrow = []
            for j in range(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData += addrow
        newimg.putdata(newData)
        canvas.data.image = newimg.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def Color_Mode(canvas):

    if canvas.data.image != None:
        dithering = FLOYDSTEINBERG.get()
        color_numbers = numb_colors_P.get()
        color_mode = (var_set.get())
        pallet = (WEB.get())
        if color_mode ==  "1-Bit-B/W " :

            canvas.data.image = canvas.data.image.convert("1", dither=int(dithering))
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)

        if color_mode == "8-bit-GRAY" :

            canvas.data.image = canvas.data.image.convert("L", dither=int(dithering))
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)

        if color_mode == "Mapped    " :

            canvas.data.image = canvas.data.image.convert("P", dither=int(dithering), palette=int(pallet),colors= int(color_numbers))
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
        if color_mode == "8-bit-RGB ":
            canvas.data.image = canvas.data.image.convert("RGB")
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)

        if color_mode == "8-bit-CMYK":
            canvas.data.image = canvas.data.image.convert("CMYK")
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)

############### FILTERS ######################

def covertGray(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    #### The existing method to convert to a grayscale image converts the ####
    ####         image mode, so I used my own function to convert         ####
    # value of each channel of a pixel is set to the average of the original
    # values of the channels
    if canvas.data.image != None:
        data = []
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b = canvas.data.image.getpixel((row, col))
                avg = int(round((r + g + b) / 3.0))
                R, G, B = avg, avg, avg
                data.append((R, G, B))
        canvas.data.image.putdata(data)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def sepia(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    # this method first converts the image to B&W and then adds the
    # same amount of red and green to every pixel
    if canvas.data.image != None:
        sepiaData = []
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b = canvas.data.image.getpixel((row, col))
                avg = int(round((r + g + b) / 3.0))
                R, G, B = avg + 100, avg + 50, avg
                sepiaData.append((R, G, B))
        canvas.data.image.putdata(sepiaData)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def invert(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.invert(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

def solarize(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    solarizeWindow = Toplevel(canvas.data.mainWindow)
    solarizeWindow.title("Solarize")
    solarizeSlider = Scale(solarizeWindow, from_=0, to=255, orient=HORIZONTAL)
    solarizeSlider.pack()
    OkSolarizeFrame = Frame(solarizeWindow)
    OkSolarizeButton = Button(OkSolarizeFrame, text="OK",
                              command=lambda: closeSolarizeWindow(canvas))
    OkSolarizeButton.grid(row=0, column=0)
    OkSolarizeFrame.pack(side=BOTTOM)
    ### beacsue intial silderVal=0
    performSolarize(canvas, solarizeWindow, solarizeSlider, 255)

def performSolarize(canvas, solarizeWindow, solarizeSlider, previousThreshold):
    if canvas.data.solarizeWindowClose == True:
        solarizeWindow.destroy()
        canvas.data.solarizeWindowClose = False

    else:
        # the  slider denotes the % of solarization that the user wants,
        # so the threshold (above which pixels are inverted) is inversely
        # related to the slider value
        if solarizeWindow.winfo_exists():
            sliderVal = solarizeSlider.get()
            threshold_ = 255 - sliderVal
            if canvas.data.image != None and threshold_ != previousThreshold:
                canvas.data.image = ImageOps.solarize(canvas.data.image,
                                                      threshold=threshold_)
                canvas.data.imageForTk = makeImageForTk(canvas)
                drawImage(canvas)
            canvas.after(200, lambda: performSolarize(canvas,
                                                      solarizeWindow, solarizeSlider, threshold_))

def closeSolarizeWindow(canvas):
    if canvas.data.image != None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.solarizeWindowClose = True

def posterize(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    # we basically reduce the range of colurs from 256 to 5 bits
    # and so, assign a single new value to each colour value
    # in each succesive range
    posterData = []
    if canvas.data.image != None:
        for col in range(canvas.data.imageSize[1]):
            for row in range(canvas.data.imageSize[0]):
                r, g, b = canvas.data.image.getpixel((row, col))
                if r in range(32):
                    R = 0
                elif r in range(32, 96):
                    R = 64
                elif r in range(96, 160):
                    R = 128
                elif r in range(160, 224):
                    R = 192
                elif r in range(224, 256):
                    R = 255
                if g in range(32):
                    G = 0
                elif g in range(32, 96):
                    G = 64
                elif g in range(96, 160):
                    G = 128
                elif r in range(160, 224):
                    g = 192
                elif r in range(224, 256):
                    G = 255
                if b in range(32):
                    B = 0
                elif b in range(32, 96):
                    B = 64
                elif b in range(96, 160):
                    B = 128
                elif b in range(160, 224):
                    B = 192
                elif b in range(224, 256):
                    B = 255
                posterData.append((R, G, B))
        canvas.data.image.putdata(posterData)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)

############# MENU COMMANDS ################

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image != None:
        filename = asksaveasfilename(defaultextension=".jpg")
        im = canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image != None:
        im = canvas.data.image
        im.save(canvas.data.imageLocation)

def newImage(canvas):
    imageName = askopenfilename()
    filetype = ""
    # make sure it's an image file
    try:
        filetype = imghdr.what(imageName)
    except:
        tkinter.messagebox.showinfo(title="Image File",
                                    message="Choose an Image File!", parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:

        canvas.data.imageLocation = imageName
        global tail
        head, tail = os.path.split(imageName)


        print(imageName)
        im = PIL.Image.open(imageName)
        canvas.data.image = im
        canvas.data.originalImage = im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize = im.size  # Original Image dimensions
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)
    else:
        tkinter.messagebox.showinfo(title="Image File",
                                    message="Choose an Image File!", parent=canvas.data.mainWindow)

######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im = canvas.data.image
    if canvas.data.image != None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
        imageWidth = canvas.data.image.size[0]
        imageHeight = canvas.data.image.size[1]
        # To make biggest version of the image fit inside the canvas
        if imageWidth > imageHeight:
            resizedImage = im.resize((canvas.data.width, \
                                      int(round(float(imageHeight) * canvas.data.width / imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale = float(imageWidth) / canvas.data.width
        else:
            resizedImage = im.resize((int(round(float(imageWidth) * canvas.data.height / imageHeight)), \
                                      canvas.data.height))
            canvas.data.imageScale = float(imageHeight) / canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm = resizedImage
        return ImageTk.PhotoImage(resizedImage)

def drawImage(canvas):
    if canvas.data.image != None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0,
                            canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX = int(round(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0))
        canvas.data.imageTopY = int(round(canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0))

############ INITIALIZE ##############
def init(root, canvas):
    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image = None
    canvas.data.angleSelected = None
    canvas.data.rotateWindowClose = False
    canvas.data.brightnessWindowClose = False
    canvas.data.brightnessLevel = None
    canvas.data.histWindowClose = False
    canvas.data.solarizeWindowClose = False
    canvas.data.posterizeWindowClose = False
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.endCrop = False
    canvas.data.drawOn = True
    canvas.data.undoQueue = deque([], 10)
    canvas.data.redoQueue = deque([], 10)
    canvas.configure(background='gray10')
    canvas.pack(side=RIGHT)

def buttonsInit(root, canvas):
    backgroundColour = "gray20"
    highlightbackground = "gray20"
    activebackground = "deepskyblue"
    fg = "lime green"
    buttonWidth = 15
    buttonHeight = 1
    toolKitFrame = Frame(root)

    lbl = Label(toolKitFrame, text="Black_threshold", bg="gray20", fg="lime green")
    lbl.grid(column=1, row=0, columnspan=3, sticky='we')

    cropButton = Button(toolKitFrame, text="Crop",
                        activebackground=activebackground, fg=fg,highlightbackground=highlightbackground,
                        background=backgroundColour,
                        width=buttonWidth, height=buttonHeight,
                        command=lambda: crop(canvas))
    cropButton.grid(row=12, column=0)
    '''
    RGB_split_Button = Button(toolKitFrame, text="RGB_split",
                        activebackground=activebackground, fg=fg,highlightbackground=highlightbackground,
                        background=backgroundColour,font=('Helvetica', '9'),
                        width=int(buttonWidth/2), height=buttonHeight,
                        command=lambda: Split_image_RGB(canvas))
    RGB_split_Button.grid(row=3, column=1,sticky=W)

    CMY_split_Button = Button(toolKitFrame, text="CMY_split",
                        activebackground=activebackground, fg=fg,highlightbackground=highlightbackground,
                        background=backgroundColour,font=('Helvetica', '9'),
                        width=int(buttonWidth/2), height=buttonHeight,
                        command=lambda: Split_image_CMY(canvas))
    CMY_split_Button.grid(row=3, column=1,sticky= E)
    '''
    CMYK_split_Button = Button(toolKitFrame, text="Split_CMYK_G",
                        activebackground=activebackground, fg=fg,highlightbackground=highlightbackground,
                        background=backgroundColour,
                        width=buttonWidth, height=buttonHeight,
                        command=lambda: Split_image_CMYK(canvas))
    CMYK_split_Button.grid(row=2, column=1)
    '''
    RGBA_split_Button = Button(toolKitFrame, text="RGBA_split",
                        activebackground=activebackground, fg=fg,highlightbackground=highlightbackground,
                        background=backgroundColour,font=('Helvetica', '9'),
                        width=int(buttonWidth/2), height=buttonHeight,
                        command=lambda: Split_image_RGBA(canvas))
    RGBA_split_Button.grid(row=2, column=1, sticky = E)
    '''

    rotateButton = Button(toolKitFrame, text="Rotate",
                          highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                          background=backgroundColour,
                          width=buttonWidth, height=buttonHeight,
                          command=lambda: rotate(canvas))
    rotateButton.grid(row=7, column=0)
    apply_Button = Button(toolKitFrame, text="Apply",
                          highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                          background=backgroundColour,
                          width=buttonWidth, height=buttonHeight,
                          command=lambda: apply(canvas))
    apply_Button.grid(row=1, column=0)

    brightnessButton = Button(toolKitFrame, text="Brightness",
                              highlightbackground=highlightbackground, anchor = "w",activebackground=activebackground,
                              fg=fg,
                              background=backgroundColour,
                              width=int(buttonWidth), height=buttonHeight,
                              command=lambda: brightness(canvas))
    brightnessButton.grid(row=8, column=0)

    '''
    brightness_undo_Button = Button(toolKitFrame, text="UNDO",
                                  highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                                  background=backgroundColour, width=int(buttonWidth / 4),
                                  height=buttonHeight, command=lambda: Contrast(canvas))
    brightness_undo_Button.grid(row=8, column=0, sticky=E)
    '''
    histogramButton = Button(toolKitFrame, text="Histogram",
                             highlightbackground=highlightbackground, activebackground=activebackground,
                             fg=fg,
                             background=backgroundColour,
                             width=buttonWidth, height=buttonHeight ,
                             command=lambda: histogram(canvas))
    histogramButton.grid(row=3, column=0)
    '''
    colourPopButton = Button(toolKitFrame, text="Colour_pop",
                             highlightbackground=highlightbackground, activebackground=activebackground,
                             fg=fg,
                             background=backgroundColour,
                             width=buttonWidth, height=buttonHeight,
                             command=lambda: colourPop(canvas))
    colourPopButton.grid(row=13, column=0)
    '''
    drawButton = Button(toolKitFrame, text="Draw",
                        highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                        background=backgroundColour, width=buttonWidth,
                        height=buttonHeight, command=lambda: drawOnImage(canvas))
    drawButton.grid(row=2, column=0)
    resetButton = Button(toolKitFrame, text="Reset",
                         highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=buttonWidth,
                         height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=0, column=0)

    mirrorButton = Button(toolKitFrame, text="Mirror",
                          highlightbackground=highlightbackground, activebackground=activebackground, fg="lime green",
                          background=backgroundColour,
                          width=int(buttonWidth / 4), height=buttonHeight,
                          command=lambda: mirror(canvas))
    mirrorButton.grid(row=5, column=0, sticky=W)

    flipButton = Button(toolKitFrame, text="Flip",
                        highlightbackground=highlightbackground, activebackground=activebackground, fg="lime green",
                        background=backgroundColour,
                        width=int(buttonWidth / 4), height=buttonHeight,
                        command=lambda: flip(canvas))
    flipButton.grid(row=5, column=0, sticky=S)

    transposeButton = Button(toolKitFrame, text="Trans",
                             highlightbackground=highlightbackground, activebackground=activebackground,
                             fg="lime green",
                             background=backgroundColour, width=int(buttonWidth / 4),
                             height=buttonHeight, command=lambda: transpose(canvas))
    transposeButton.grid(row=5, column=0, sticky=E)


    ColorButton = Button(toolKitFrame, text="Color",
                         highlightbackground=highlightbackground,anchor = "w", activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=int(buttonWidth),
                         height=buttonHeight, command=lambda: Color_shift(canvas))
    ColorButton.grid(row=9, column=0)
    '''
    Color_undo_Button = Button(toolKitFrame, text="UNDO",
                         highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=int(buttonWidth/4),
                         height=buttonHeight, command=lambda: Contrast(canvas))
    Color_undo_Button.grid(row=9, column=0, sticky = E)
    '''
    ContrastButton = Button(toolKitFrame, text="Contrast",
                         highlightbackground=highlightbackground, anchor = "w", activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=int(buttonWidth),
                         height=buttonHeight, command=lambda: Contrast(canvas))
    ContrastButton.grid(row=10, column=0)
    '''
    Contrast_undo_Button = Button(toolKitFrame, text="UNDO",
                         highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=int(buttonWidth/4),
                         height=buttonHeight, command=lambda: Contrast(canvas))
    Contrast_undo_Button.grid(row=10, column=0, sticky = E)
    '''
    SharpnessButton = Button(toolKitFrame, text="Sharpness",
                         highlightbackground=highlightbackground, anchor = "w",activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=int(buttonWidth),
                         height=buttonHeight, command=lambda: Sharpness(canvas))
    SharpnessButton.grid(row=11,column=0)
    '''
    Sharpness_undo_Button = Button(toolKitFrame, text="UNDO",
                         highlightbackground=highlightbackground, activebackground=activebackground, fg=fg,
                         background=backgroundColour, width=int(buttonWidth/4),
                         height=buttonHeight, command=lambda: Contrast(canvas))
    Sharpness_undo_Button.grid(row=11, column=0, sticky = E)
    '''
    #################################### SCALES ####################################
    global rotate_slider
    rotate_slider = Scale(toolKitFrame, from_=-180, to=180, resolution=90,length=140, width=7, font=('Helvetica', '8'),
                          orient=HORIZONTAL,
                          bg="gray20",
                          fg="lime green",
                          highlightbackground="gray", activebackground="deep sky blue", troughcolor="White")
    rotate_slider.grid(row=7, column=1)
    global bright_slider
    bright_slider = Scale(toolKitFrame, from_=0.0, to=2.0, resolution=.01, length=140, width=7, font=('Helvetica', '8'),
                          orient=HORIZONTAL,
                          bg="gray20",
                          fg="lime green",
                          highlightbackground="gray", activebackground="deep sky blue", troughcolor="DarkOrchid1")
    bright_slider.grid(row=8, column=1)
    bright_slider.set(1)
    '''
    global Red_slider
    Red_slider = Scale(toolKitFrame, from_=0, to=255, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                       bg="gray20",
                       fg="lime green",
                       highlightbackground="gray", activebackground="deep sky blue", troughcolor="Red")
    Red_slider.grid(row=3, column=1, sticky=N)
    global Green_slider
    Green_slider = Scale(toolKitFrame, from_=0, to=255, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                         bg="gray20",
                         fg="lime green",
                         highlightbackground="gray", activebackground="deep sky blue", troughcolor="Green")
    Green_slider.grid(row=3, column=1, sticky=S)
    global Blue_slider
    Blue_slider = Scale(toolKitFrame, from_=0, to=255, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                        bg="gray20",
                        fg="lime green",
                        highlightbackground="gray", activebackground="deep sky blue", troughcolor="Blue")
    Blue_slider.grid(row=3, column=1)
    '''
    global Color_slider
    Color_slider = Scale(toolKitFrame,from_=0.0, to=3.0, resolution=.01, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                        bg="gray20",
                        fg="lime green",
                        highlightbackground="gray", activebackground="deep sky blue", troughcolor="DarkOrchid2")
    Color_slider.grid(row=9, column=1)
    Color_slider.set(1)
    global Contrast_slider
    Contrast_slider = Scale(toolKitFrame, from_=-3.0, to=3.0, resolution=.05, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                        bg="gray20",
                        fg="lime green",
                        highlightbackground="gray", activebackground="deep sky blue", troughcolor="DarkOrchid3")
    Contrast_slider.grid(row=10, column=1)
    Contrast_slider.set(1)
    global Edge_slider
    Edge_slider = Scale(toolKitFrame, from_=0, to=60, resolution=1, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                        bg="gray20",
                        fg="lime green",
                        highlightbackground="gray", activebackground="deep sky blue", troughcolor="DarkOrchid4")
    Edge_slider.grid(row=1, column=1)
    Edge_slider.set(10)
    toolKitFrame.configure(background='gray20')


    global Sharpness_slider
    Sharpness_slider = Scale(toolKitFrame, from_=-3.0, to=3.0, resolution=.05, length=140, width=7, font=('Helvetica', '8'), orient=HORIZONTAL,
                        bg="gray20",
                        fg="lime green",
                        highlightbackground="gray", activebackground="deep sky blue", troughcolor="DarkOrchid4")
    Sharpness_slider.grid(row=11, column=1)
    toolKitFrame.configure(background='gray20')
    toolKitFrame.place(x=0, y=0)





    #################################### color_modes ####################################
    Label(root, text="COLOR_Mode", anchor="center", bg="gray20", fg="lime green").place(x=0, y=365, height=20, width=150)
    Color_MODES = [
        ("1-Bit-B/W ", "1-Bit-B/W "),
        ("8-bit-GRAY", "8-bit-GRAY"),
        ("Mapped    ", "Mapped    "),
        ("8-bit-RGB ", "8-bit-RGB "),
        ("8-bit-CMYK", "8-bit-CMYK"),
    ]
    global var_set
    var_set = StringVar()
    var_set.set("L")  # initialize
    count = 0
    for text, mode in Color_MODES:
        b = Radiobutton(root, text=text, variable=var_set, value=mode, bg="gray20", fg="lime green",
                        highlightbackground="gray20", activebackground="deep sky blue").place(x=0, y=385 + count)
        count = count + 20
    var_set.set("8-bit-RGB ")

    #*** check button ***
    global FLOYDSTEINBERG
    FLOYDSTEINBERG = StringVar()
    dithering_mode = Checkbutton(root, text ="Dither", anchor="e",variable=FLOYDSTEINBERG, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    dithering_mode.deselect()
    dithering_mode.place(x=0, y=485)

    #*** check button ***
    global WEB
    WEB = StringVar()
    dithering_mode = Checkbutton(root, text ="ADAPTIVE", anchor="e",variable=WEB, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    dithering_mode.deselect()
    dithering_mode.place(x=138, y=425)

    # *** color_box ***
    global numb_colors_P
    numb_colors_P = StringVar(root, value='8')
    color_box_entry = Entry(root, textvariable=numb_colors_P)
    color_box_entry.place(x=103, y=425, height=20, width=35)

    Button(root, text='Convert_color_mode',  command=lambda: Color_Mode(canvas), bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=507, height=35, width=150)

def menuInit(root, canvas):
    menubar = Menu(root)
    menubar.add_command(label="New", command=lambda: newImage(canvas))
    menubar.add_command(label="Save", command=lambda: save(canvas))
    ## Filter pull-down Menu
    filtermenu = Menu(menubar, tearoff=0)
    filtermenu.add_command(label="Black and White",
                           command=lambda: covertGray(canvas))
    filtermenu.add_command(label="Sepia",
                           command=lambda: sepia(canvas))
    filtermenu.add_command(label="Invert",
                           command=lambda: invert(canvas))
    filtermenu.add_command(label="Solarize",
                           command=lambda: solarize(canvas))
    filtermenu.add_command(label="Posterize",
                           command=lambda: posterize(canvas))
    menubar.add_cascade(label="Filter", menu=filtermenu)

    root.config(menu=menubar)

def run():
    root_width = "900"
    root_height = "600"
    root = Tk()
    root.geometry(root_width + "x" + root_height)  # Width x Height
    root.title("raster-edit")
    canvasWidth = 600
    canvasHeight = 500
    # ***main menue***
    menu = Menu(root)
    root.config(menu=menu)

    root.configure(background='gray20')


    canvas = Canvas(root, width=canvasWidth, height=canvasHeight,
                    background="gray20")

    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.mainWindow = root
    init(root, canvas)
    #root.bind("<Key>", lambda event: keyPressed(canvas, event))
    # and launch the app
    center_tk_window.center_on_screen(root)

    root.mainloop()  # This call BLOCKS (so your program waits)

run()
