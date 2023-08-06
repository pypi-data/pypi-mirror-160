import xmnlp

enable = xmnlp.config.MODEL_DIR


def predict(text):
    return xmnlp.sentiment(text)[1]
