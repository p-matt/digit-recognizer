import numpy as np
from tensorflow.keras.models import load_model
from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk
from skimage.transform import resize

model = load_model("../data/single/model")
new_images = []


def compute(output_00, output_01, output_predictions, canvas):
    file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    X = preprocess(img, output_00, output_01, output_predictions, canvas)
    y = predict(X, output_00, output_01, output_predictions, canvas)


def preprocess(img, output_00, output_01, output_predictions, canvas):
    X = np.array(ImageOps.grayscale(img)).astype("float32")
    X_show = Image.fromarray(resize(np.array(ImageOps.grayscale(img)).astype("float32"), (112, 112)))
    update_image(0, X_show, output_00, output_01, output_predictions, canvas)

    X = resize(X, (28, 28))
    X_show = Image.fromarray(X)
    update_image(1, X_show, output_00, output_01, output_predictions, canvas)

    X = - (X - 127.5) / 127.5
    return X


def predict(X, output_00, output_01, output_predictions, canvas):
    y_preds = model.predict(X.reshape(1, 28, 28))
    y_pred = np.argmax(y_preds)

    img = Image.open(f"assets/{y_pred}.png")
    update_image(2, img, output_00, output_01, output_predictions, canvas)
    return y_pred


def update_image(old_image, new_image, output_00, output_01, output_predictions, canvas):
    old_image = output_00 if old_image == 0 else output_01 if old_image == 1 else output_predictions
    new_image = ImageTk.PhotoImage(new_image)
    new_images.append(new_image)

    canvas.itemconfig(old_image, image=new_image)
    canvas.update_idletasks()
