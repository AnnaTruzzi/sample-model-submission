import functools
import torch
from collections import OrderedDict

from deepcluster import alexnet 
from model_tools.activations.pytorch import PytorchWrapper
from model_tools.activations.pytorch import load_preprocess_images

from test import test_models

"""
Template module for a base model submission to brain-score
"""

def get_model_list():
    """
    This method defines all submitted model names. It returns a list of model names.
    The name is then used in the get_model method to fetch the actual model instance.
    If the submission contains only one model, return a one item list.
    :return: a list of model string names
    """
    return ['deepcluster','deepcluster_untrained']


def get_model(name):
    """
    This method fetches an instance of a base model. The instance has to be callable and return a xarray object,
    containing activations. There exist standard wrapper implementations for common libraries, like pytorch and
    keras. Checkout the examples folder, to see more. For custom implementations check out the implementation of the
    wrappers.
    :param name: the name of the model to fetch
    :return: the model instance
    """
    if name == 'deepcluster':
        model = alexnet(sobel=True, bn=True, out=10000) 
        checkpoint = torch.load('deepcluster/checkpoint_dc.pth.tar')['state_dict']
        checkpoint_new = OrderedDict()
        for k, v in checkpoint.items():
            name = k.replace(".module", '') # remove 'module.' of dataparallel
            checkpoint_new[name]=v
        model.load_state_dict(checkpoint_new)
        model.cuda()
    if name == 'deepcluster_untrained':
        model = alexnet(sobel=True, bn=True, out=10000) 
        model.cuda()
    preprocessing = functools.partial(load_preprocess_images, image_size=224)
    wrapper = PytorchWrapper(identifier='deepcluster', model=model, preprocessing=preprocessing)
    wrapper.image_size = 224
    return wrapper


def get_layers(name):
    """
    This method returns a list of string layer names to consider per model. The benchmarks maps brain regions to
    layers and uses this list as a set of possible layers. The lists doesn't have to contain all layers, the less the
    faster the benchmark process works. Additionally the given layers have to produce an activations vector of at least
    size 25! The layer names are delivered back to the model instance and have to be resolved in there. For a pytorch
    model, the layer name are for instance dot concatenated per module, e.g. "features.2".
    :param name: the name of the model, to return the layers for
    :return: a list of strings containing all layers, that should be considered as brain area.
    """
#    assert name == 'deepcluster'
    return ['_model.features[2]','_model.features[6]','_model.features[10]','_model.features[13]','_model.features[16]','_model.classifier[2]','_model.classifier[5]']

if __name__ == '__main__':
    test_models.test_base_models(__name__)



