import cv2 as cv
from time import sleep
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from PathConstants import *

WAIT_TIME = 1 / 15  # 15 fps
RESULTS_WIDTH = 800
RESULTS_HEIGHT = 500

# set tensorflow to run on cpu here because waiting for it to load all the cudnn files takes too long
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def run_stuff():
    # capture from web cam
    capture = cv.VideoCapture(0)
    simp_model = load_model(r'models\simp_model_98_test_acc.h5')
    if not os.path.isdir(ORGANIZED_DATA_DIRECTORY):
        os.mkdir('live')

    while True:
        is_true, frame = capture.read()
        cv.imshow("video", frame)
        file_location = "live/current_frame.jpg"
        cv.imwrite(file_location, frame)
        guesses = give_ordered_guesses(simp_model, file_location)
        print(guesses)
        draw_guesses(guesses)
        sleep(WAIT_TIME)
        # press esc to quit
        if cv.waitKey(30) & 0xFF == 27:
            break

    capture.release()
    cv.destroyAllWindows()


def prepare_image(input_path):
    img = image.load_img(input_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)


def find_readable_predictions(predictions, labels):
    label_map = {}
    for i in range(len(labels)):
        label_map[i] = predictions[0][i]
    label_map = sorted(label_map.items(), key=lambda x: x[1], reverse=True)

    return [labels[label_map[i][0]] for i in range(len(labels))]


def give_ordered_guesses(model, image_path):
    processed_image = prepare_image(image_path)
    numpy_arr_predictions = model.predict(processed_image)
    return find_readable_predictions(numpy_arr_predictions, NAME_LABELS)


def draw_guesses(guesses):
    blank = np.zeros((RESULTS_HEIGHT, RESULTS_WIDTH, 1), dtype='uint8')
    cv.putText(blank, "1. " + guesses[0], (0 + RESULTS_WIDTH // 6, 0 + 80), cv.FONT_HERSHEY_TRIPLEX, 1.25,
               (255, 0, 0))
    cv.putText(blank, "2. " + guesses[1], (0 + RESULTS_WIDTH // 5, 0 + 160), cv.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0))
    cv.putText(blank, "3. " + guesses[2], (0 + RESULTS_WIDTH // 4, 0 + 240), cv.FONT_HERSHEY_TRIPLEX, 0.75,
               (255, 0, 0))
    cv.imshow("Guesses", blank)


run_stuff()

cv.waitKey(0)
