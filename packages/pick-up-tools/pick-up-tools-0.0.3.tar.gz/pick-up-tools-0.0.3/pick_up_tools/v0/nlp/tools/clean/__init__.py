from .html import *
from ..extractor import Extractor

extractor = Extractor()

clean_text = extractor.clean_text

del extractor
