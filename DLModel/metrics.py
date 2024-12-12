import tensorflow as tf
from tensorflow import keras



def iou(y_true, y_pred):
    y_pred = tf.clip_by_value(y_pred, 0.0, 1.0)
    intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    union = tf.reduce_sum(y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3]) - intersection
    iou_score = (intersection + 1e-15) / (union + 1e-15)
    return tf.reduce_mean(iou_score, axis=0)


smooth = 1e-15


def dice_coef(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)  # Ensure correct type
    y_pred = tf.cast(y_pred, tf.float32)  # Ensure correct type
    intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    dice_score = (2. * intersection + smooth) / (tf.reduce_sum(y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3]) + smooth)
    return tf.reduce_mean(dice_score, axis=0)


# Dice Loss
def dice_loss(y_true, y_pred):
    return 1.0 - dice_coef(y_true, y_pred)
