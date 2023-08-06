# -*- coding: utf-8 -*-
from accelbrainbase.samplable_data import SamplableData
from accelbrainbase.iteratable_data import IteratableData
from abc import abstractmethod


class PretextSampler(SamplableData):
    '''
    Sampler for pretext tasks.

    This interface is especially useful 
    for muplti-pretext tasks such as Transformers in 
    the Natural Language Processing.

    Mainly, the subclass of this class 
    `SSDATransformerIterator`
    '''

    @abstractmethod
    def preprocess(self, target_domain_arr):
        '''
        Preprocess observed data points in target domain.

        Args:
            target_domain_arr:      Tensor of observed data points in target domain.
        '''
        raise NotImplementedError()

    def draw(self):
        '''
        Draw samples from distribtions.
        
        Returns:
            `Tuple` of samples.
        '''
        return (
            self.pretext_encoded_observed_arr,
            self.pretext_decoded_observed_arr,
            self.pretext_encoded_mask_arr,
            self.pretext_decoded_mask_arr,
            self.pretext_label_arr,
        )

    __pretext_encoded_observed_arr = None

    def get_pretext_encoded_observed_arr(self):
        return self.__pretext_encoded_observed_arr
    
    def set_pretext_encoded_observed_arr(self, value):
        self.__pretext_encoded_observed_arr = value

    pretext_encoded_observed_arr = property(get_pretext_encoded_observed_arr, set_pretext_encoded_observed_arr)

    __pretext_decoded_observed_arr = None

    def get_pretext_decoded_observed_arr(self):
        return self.__pretext_decoded_observed_arr
    
    def set_pretext_decoded_observed_arr(self, value):
        self.__pretext_decoded_observed_arr = value

    pretext_decoded_observed_arr = property(get_pretext_decoded_observed_arr, set_pretext_decoded_observed_arr)


    __pretext_encoded_mask_arr = None

    def get_pretext_encoded_mask_arr(self):
        return self.__pretext_encoded_mask_arr
    
    def set_pretext_encoded_mask_arr(self, value):
        self.__pretext_encoded_mask_arr = value

    pretext_encoded_mask_arr = property(get_pretext_encoded_mask_arr, set_pretext_encoded_mask_arr)

    __pretext_decoded_mask_arr = None

    def get_pretext_decoded_mask_arr(self):
        return self.__pretext_decoded_mask_arr
    
    def set_pretext_decoded_mask_arr(self, value):
        self.__pretext_decoded_mask_arr = value

    pretext_decoded_mask_arr = property(get_pretext_decoded_mask_arr, set_pretext_decoded_mask_arr)

    __pretext_label_arr = None

    def get_pretext_label_arr(self):
        return self.__pretext_label_arr
    
    def set_pretext_label_arr(self, value):
        self.__pretext_label_arr = value

    pretext_label_arr = property(get_pretext_label_arr, set_pretext_label_arr)
