import os
import shutil
import random
from PathConstants import *


def count_files_for_class(dir_path):
    count = 0
    for _ in os.listdir(dir_path):
        count += 1
    return count


# prints a summary of the contents of the data to the console
def print_dir_summary(dir_path):
    for folder in os.listdir(dir_path):
        print("\nDirectory name: ", folder, "\nFiles found: ", count_files_for_class(os.path.join(dir_path, folder)))


# returns a list of tuples with file count and class name in descending order
def get_class_order(dir_path):
    classes = [f for f in os.listdir(dir_path)]
    count = [count_files_for_class(os.path.join(dir_path, folder)) for folder in os.listdir(dir_path)]
    return sorted(set(zip(count, classes)), reverse=True)


# organizes data to allow for easy batch creation later on. output folder is called data-organized
def organize_data(data_dir_path, classes, validation_size, testing_size):
    # if our directory for training data has not already been made make it
    if not os.path.isdir(ORGANIZED_DATA_DIRECTORY):
        os.chdir(data_dir_path)
        os.mkdir('train')
        os.mkdir('valid')
        os.mkdir('test')

        for class_name in classes:
            # move class data into train dir & create class files inside of valid and test
            shutil.move(f'{class_name}', 'train')
            os.mkdir(f'valid/{class_name}')
            os.mkdir(f'test/{class_name}')

            # select and move validation samples
            validation_samples = random.sample(os.listdir(f'train/{class_name}'), validation_size)
            for vs in validation_samples:
                shutil.move(f'train/{class_name}/{vs}', f'valid/{class_name}')
            print('created validation directory')

            # select and move testing samples
            test_samples = random.sample(os.listdir(f'train/{class_name}'), testing_size)
            for ts in test_samples:
                shutil.move(f'train/{class_name}/{ts}', f'test/{class_name}')
            print('created testing directory')
        # move os path back
        os.chdir('../..')
    else:
        print(f'DIRECTORY: "{ORGANIZED_DATA_DIRECTORY}" already exists \ndata will not be moved')
    # if our directory for organized data has not been made make it
    if not os.path.isdir(ORGANIZED_DATA_DIRECTORY):
        os.mkdir(ORGANIZED_DATA_DIRECTORY)
        shutil.move(os.path.join(data_dir_path, 'train/'), ORGANIZED_DATA_DIRECTORY)
        shutil.move(os.path.join(data_dir_path, 'valid/'), ORGANIZED_DATA_DIRECTORY)
        shutil.move(os.path.join(data_dir_path, 'test/'), ORGANIZED_DATA_DIRECTORY)


def sort_files():
    # create ordered list of tuples
    ordered_classes = get_class_order(DATA_PATH)
    # only use the classes with the most data
    ordered_classes = ordered_classes[:CLASSES_TO_WORK_WITH]

    class_labels = []
    for i, j in ordered_classes:
        print(j, ": ", i)
        class_labels.append(j)

    organize_data(DATA_PATH, class_labels, VALIDATION_SIZE, TEST_SIZE)
    print(f"DONE - Organized data should be at ../{ORGANIZED_DATA_DIRECTORY}..")


sort_files()
