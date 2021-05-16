import cv2
import numpy as np
import dlib 
from skimage.io import imread_collection
import os
from PIL import Image
import sys
from imutils import face_utils

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

DEBUG_PATH = 'debug/'

def loadImages(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def landmark_debug(img, face):
    landmarks = predictor(image=img, box=face)
    l_data = []
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        l_data.append((x,y))
        cv2.circle(img=img, center=(int(x), int(y)), radius=1, color=(0, 255, 0), thickness=-1)
    return img, l_data

def landmark(img, face):
    landmarks = predictor(image=img, box=face)
    return face_utils.shape_to_np(landmarks).tolist()

def lms_for_peeks(path, lmpath, prefix):
    save_path_lm = lmpath + "landmarks"+ "_" + prefix
    images = loadImages(path)
    lms = []

    i = 1
    for image in images:
        faces = detector(image)
        if (len(faces) > 0):
            lm = landmark(image, faces[0])
            lms.append(lm)
            i += 1

    np.save(save_path_lm, np.array(lms))

def lms_for_peeks_debug(path, lmpath, prefix):
    save_path_lm = lmpath + "landmarks" + "_" + prefix
    images = loadImages(path)
    lms = []

    i = 1
    for image in images:
        faces = detector(image)
        if (len(faces) > 0):
            img, lm = landmark_debug(image, faces[0])
            img = Image.fromarray(img)
            img.save(DEBUG_PATH + str(i) + ".jpeg")
            lms.append(lm)
            i += 1

    np.save(save_path_lm, np.array(lms))

if __name__ == "__main__":
    debug = sys.argv[1]
    prefix = sys.argv[2]

    image_path = 'data/' + prefix + '/'
    npy_path = 'npy/'
    
    if (debug == 'true'):
        lms_for_peeks_debug(image_path, npy_path, prefix)
    else:
        lms_for_peeks(image_path, npy_path, prefix)
        