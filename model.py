import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.models.load_model("model.h5")

classes = ["COVID", "Normal", "Pneumonia", "Tuberculosis"]

def predict_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (224,224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)[0]
    idx = np.argmax(preds)

    return classes[idx], float(preds[idx])