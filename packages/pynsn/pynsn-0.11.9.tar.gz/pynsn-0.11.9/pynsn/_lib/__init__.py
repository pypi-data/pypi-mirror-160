from .base_classes import ArrayParameter, AttributeArray
from .dot_array import DotArray
from .rect_array import RectangleArray
from .shapes import Point, Dot, Rectangle
from .picture_file import PictureFile
from .appearance_sampler import AppearanceSampler
from .factory import NSNFactory


# helper for type checking and error raising error
def _check_array_parameter(obj):
    if not isinstance(obj, ArrayParameter):
        raise TypeError("DotArray, RectangleArray or ArrayParameter expected, but not {}".format(
            type(obj).__name__))


def _check_object_array(obj):
    if not isinstance(obj, (DotArray, RectangleArray)):
        raise TypeError("DotArray or RectangleArray expected, but not {}".format(
            type(obj).__name__))

