# Readme
`ResiliPy` provides an accessible machine-learning based framework for classifying mice according to their stress resilience based on tracking data.

## Motivation
Resilience research in mice using the chronic social defeat paradigm commonly depends on the social interaction (SI) ratio to group animals into those that are susceptible and resilient to stress. The SI ratio only considers the time spent near the aggressor mouse during the social interaction test, not considering many possible indicators of resilient or susceptible behaviour.

Here `ResiliPy` offers an alternative labelling approach that does not consider the distance to the aggressor animal directly, but rather takes the relative distances for each time point into consideration, setting up a distribution of relative distance measures. Using percentiles from this distribution gives more detailed information about the overall behaviour of the animals. In combination with preassigned resilience labels, a machine learning model is trained to classify new animals by their resilience.

To simplify use, the classification and pre-processing process has been integrated into a graphical user interface. Accordingly, no programming knowledge is required to use `ResiliPy`.

## Structure
`ResiliPy` consists of three main modules:
### Labeller
The Labeller performs the classification task itself on a dataset of unlabelled animals. Based on a loaded machine-learning model, an imported pre-processed (see Preprocessor) dataset can be classified.
### Preprocessor
The given classification approach requires relative distance distributions extracted from the tracking data. This process if performed with the Preprocessor. Given raw Ethovision tracking files, the coordinates are transformed into the needed format. The extracted dataset can subsequently be used for labelling.
### Builder
For classification, it is highly advisable to use a model that has been trained with comparable data. New machine learning models can be imported and used in `ResiliPy`. An optimised model can be imported into the Builder together with training data to create a *.model* file. This is then imported into the Labeller for classification.

# Installation & Launch
With Python installed, `ResiliPy` can be installed via the Python Packaging Index (PyPI). In the terminal or command promt, type:
```bash
pip install resilipy
```
`ResiliPy` can be launched by typing in the terminal:
```bash
python -m resilipy
```

## References

## License
MIT License (MIT). See [License](http://https://gitlab.rlp.net/vdietric/resilipy/-/blob/main/LICENSE "License") file for details.
