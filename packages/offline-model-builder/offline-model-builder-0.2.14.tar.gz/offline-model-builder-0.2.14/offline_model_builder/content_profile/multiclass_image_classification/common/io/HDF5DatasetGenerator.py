# HDF5DatasetGenerator.py

import h5py
import numpy as np
from keras.utils import np_utils


class HDF5DatasetGenerator:
    '''
    Use to generate a dataset for use withing keras framework
    form a HDF5 file.
    '''
    def __init__(self, dbPath, batchSize, preprocessors = None,
        aug = None, binarize = True, classes = 2):
        '''
        '''
        # store the batch size, preprocessors, and data augmentor, 
        # whether or not the labels should be binarized, along with
        # the total number of classes
        self.batchSize = batchSize
        self.preprocessors = preprocessors
        self.aug = aug
        self.binarize = binarize
        self.classes = classes

        # open the HDF5 database for reading and determine the total
        # number of entries in the database
        self.db = h5py.File(dbPath)
        self.numImages = self.db["labels"].shape[0]
    

    def generator(self, passes = np.inf):
        # initialize the epoch count
        epochs = 0

        # keep looping infinitely -- the model will stop once we have
        # reached the desired number of epochs
        while epochs < passes:
            # loop over the HDF5 dataset
            for i in np.arange(0, self.numImages, self.batchSize):
                # extract the iamges and labels from the HDF5 dataset
                images = self.db["images"][i: i + self.batchSize]
                labels = self.db["labels"][i: i + self.batchSize]

                # check to see if the labels should be binarized
                if self.binarize:
                    labels = np_utils.to_categorical(labels, self.classes)

                # check to see if our preprocessors are not None
                if self.preprocessors is not None:
                    # initialize the list of processed images
                    procImages = []

                    # loop over the images
                    for image in images:
                        # loop over the preprocessors and apply each
                        # to the image
                        for p in self.preprocessors:
                            image = p.preprocess(image)
                        
                        # update the list of processed images
                        procImages.append(image)
                    
                    # update the images array to be the processed
                    # images
                    images = np.array(procImages)

                # if the data augmentor exists, apply it
                if self.aug is not None:
                    (images, labels) = next(self.aug.flow(images, labels, batch_size = self.batchSize))
                    
                # yield a tuple of images and labels
                yield (images, labels)
                
            # increment the total number of epochs processed    
            epochs += 1
            print(epochs)


    def close(self):
        '''
        '''
        # cose the datab<se
        self.db.close()