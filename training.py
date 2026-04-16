import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# -----------------------------
# PATHS
# -----------------------------
train_dir = "dataset/train"
val_dir = "dataset/val"
test_dir = "dataset/test"

# -----------------------------
# PARAMETERS
# -----------------------------
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 15

CLASSES = ["COVID", "Normal", "Pneumonia", "Tuberculosis"]

# -----------------------------
# DATA GENERATORS
# -----------------------------
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

val_gen = ImageDataGenerator(rescale=1./255)
test_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    classes=CLASSES
)

val_data = val_gen.flow_from_directory(
    val_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    classes=CLASSES
)

test_data = test_gen.flow_from_directory(
    test_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    classes=CLASSES,
    shuffle=False
)

print("Class Mapping:", train_data.class_indices)

# -----------------------------
# MODEL
# -----------------------------
base_model = DenseNet121(weights='imagenet', include_top=False)

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
output = Dense(4, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

# -----------------------------
# COMPILE
# -----------------------------
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------------
# CALLBACKS
# -----------------------------
early_stop = EarlyStopping(patience=3, restore_best_weights=True)

# -----------------------------
# TRAIN
# -----------------------------
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=[early_stop]
)

# -----------------------------
# SAVE MODEL
# -----------------------------
model.save("backend/model.h5")

# -----------------------------
# PLOT ACCURACY
# -----------------------------
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Accuracy")
plt.legend(['Train', 'Validation'])
plt.show()

# -----------------------------
# EVALUATION
# -----------------------------
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import seaborn as sns

preds = model.predict(test_data)
y_pred = np.argmax(preds, axis=1)

print("\nClassification Report:\n")
print(classification_report(test_data.classes, y_pred))

cm = confusion_matrix(test_data.classes, y_pred)

sns.heatmap(cm, annot=True, fmt="d")
plt.title("Confusion Matrix")
plt.show()