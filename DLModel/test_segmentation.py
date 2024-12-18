from glob import glob
import os
import cv2
import keras
import numpy as np
from sklearn.model_selection import train_test_split
from metrics import iou

W=256
H=256


def extract_infected_area(image, mask):
    """
    Extract the portion of the image corresponding to the mask.
    
    Args:
    - image: The original image (shape: H x W x 3)
    - mask: The binary mask (shape: H x W x 1)
    
    Returns:
    - Extracted portion of the image (shape: H x W x 3)
    """
    
    mask = (mask > 0.5).astype(np.uint8)  
    infected_area = image * mask  
    
    return infected_area


def read_image(path):
    x = cv2.imread(path, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (W, H))
    x = x/255.0
    x = x.astype(np.float32)
    return x

def read_mask(path):
    x = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x = cv2.resize(x, (W, H))
    x = x/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x, axis=-1)
    return x

def load_data(path, split=0.2):
    images = sorted(glob(os.path.join(path, "images", "*.jpg")))
    masks = sorted(glob(os.path.join(path, "mask", "*.png")))
    return (images,masks)


if __name__ == "__main__":
    dataset_path = os.path.join("Dataset")
    (train_x, train_y) = load_data(dataset_path)

    segmentation_model = keras.models.load_model("model.keras",compile=False)

    for i in zip(train_x,train_y):
        test_x_image = read_image(i[0])
        test_y_image = read_mask(i[1])
        test_x_image = np.expand_dims(test_x_image,axis=0)

        res = segmentation_model.predict(test_x_image)

        res_image = np.squeeze(res)
        res_image = np.expand_dims(res_image, axis=-1)

        
        iou_score = iou(np.expand_dims(res_image,axis=0),np.expand_dims(test_y_image,axis=0))

        if(iou_score > 0.5):
        
            infect = extract_infected_area((test_x_image * 255).astype(np.uint8),res_image)
            infect = np.squeeze(infect)
            combined = infect
        else:
            combined = test_x_image
            combined = np.squeeze(combined)
            combined = ((combined*255).astype(np.uint8))

        name = i[0].split("/")

        cv2.imwrite(os.path.join('segmented_images',name[-1]), combined)
        