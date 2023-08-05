from GenderPrediction.gender_prediction import GenderPredictor

input_name = 'ENTER YOUR NAME'
gp = GenderPredictor(name=input_name)
print(gp.predict())