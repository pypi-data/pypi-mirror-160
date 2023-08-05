import pathlib
import GenderPrediction

PACKAGE_ROOT = pathlib.Path(GenderPrediction.__file__).resolve().parent
model_path = PACKAGE_ROOT / 'gender_model-Bilstm128-25-10-retrained.h5'