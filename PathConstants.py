NAME_LABELS = ['Abe Simpson', 'Apu', 'Bart Simpson',
               'Monty Burns', 'Chief Wiggum', 'Homer Simpson',
               'Kent Brockman', 'Krusty the Clown', 'Lisa Simpson',
               'Marge Simpson', 'Milhouse', 'Moe szyslak',
               'Ned Flanders', 'Principal Skinner', 'Sideshow Bob']

# file name that organized data will be output too
ORGANIZED_DATA_DIRECTORY = 'data-organized/'
# path where unorganized data is stored
DATA_PATH = 'data/simpsons_dataset/'
# number of classes this will change how many character the model can identify
CLASSES_TO_WORK_WITH = 15
# Batch size
BATCH_SIZE = 50
# training epochs
TRAINING_EPOCHS = 5
# Image target size the model will use parts of the mobile_net model
# this model expects input of shape (224, 224, 3)
IMAGE_SIZE = (224, 224)
# validation sample size in # of images
VALIDATION_SIZE = 50
# test sample size in # of images
TEST_SIZE = 20
'''
    note the training size will be the rest of the data provided
    note the size of these should not exceed the dataset for the character with the least images available
'''
