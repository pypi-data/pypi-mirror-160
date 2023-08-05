# -*- coding: utf-8 -*-
# ImageToArrayPreprocessor.py
'''
'''


from keras.preprocessing.image import img_to_array


class ImageToArrayPreprocessor:
    '''
    '''
    def __init__(self, dataFormat = None):
        '''
        Store image data format
        '''
        self.dataFormat = dataFormat


    def preprocess(self, image):
        # apply the keras utility function that correctly
        # rearranges the dimensions of the image
        return img_to_array(image, data_format = self.dataFormat)


    