import tensorflow as tf
import numpy as np
import cv2
import matplotlib.cm as cm

def get_gradcam(img_path, model, output_path):
    img = cv2.imread(img_path)
    img_resized = cv2.resize(img, (224,224)) / 255.0
    img_array = np.expand_dims(img_resized, axis=0)

    last_conv_layer = model.get_layer("conv5_block16_concat")

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [last_conv_layer.output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, np.argmax(predictions[0])]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))

    heatmap = conv_outputs[0] @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = np.maximum(heatmap,0) / np.max(heatmap)

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)

    heatmap = cm.jet(heatmap)[:,:,:3] * 255
    superimposed = heatmap * 0.4 + img

    cv2.imwrite(output_path, superimposed)
    return output_path