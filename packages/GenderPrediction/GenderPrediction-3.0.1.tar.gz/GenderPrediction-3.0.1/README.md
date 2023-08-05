# Gender Prediction

Now predict your Gender just from your First Name.
Enter your Indian name in english alphabets and get your Gender 🙂

### Example Code:

* Predict for Single Name:

```python
from GenderPrediction.gender_prediction import GenderPredictor

input_name = 'ENTER YOUR NAME'
gp = GenderPredictor(name=input_name)
print(gp.predict())
```

* Predict in Batch:
```python
from GenderPrediction.gender_prediction import GenderPredictor

input_name = '[ENTER MULTIPLE NAMES IN A LIST]'
gp = GenderPredictor(name=input_name)
print(gp.batch_predict())
```