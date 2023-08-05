## About

This is a simple python package of Linear support vector machine model trained on the Minerva dataset. The trained model can be used to
predict the license shortname from the code.

### How to use

- Installing the package:
  - `pip install linearsvc`
- Import the trained model:
  - `from linearsvc import linearsvc`
- How to use:
  - By calling sklearn's predict function:
    `classifier = linearsvc(processed_comment)`
    `predictor = classifier.classify()`
    `short_name = predictor.predict(processed_comment)`
  - By directly calling predict_shortname():
    `classifier = linearsvc(processed_comment)`
    `short_name = classifier.predict_shortname()`
