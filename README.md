# Carclassifier

Python (Flask) application that classifies opinions (in Polish) about cars. The algorithm itself (exploiting `SGDCClassifier`) 
and application template is based on Chapter 8 and 9 of [Sebastian Raschka's](https://github.com/rasbt)
[Python Machine Learning Book](https://github.com/rasbt/python-machine-learning-book). 
Training data set was fetched from [motofakty.pl](https://www.motofakty.pl/) by using `BeautifulSoup` Python library.

## Preprocessing

As Polish grammar is quite complicated, data cleaning was the crucial point of our analysis.

Data were preprocessed according to the following algorithm (see `analysis.ipynb`):
- fetching important tokens (emoticons and rates)
- removing non-alphanumeric characters
- removing terms that contain digits
- setting all characters to lowercase
- replacing Polish letters with Latin ones
- joining *nie* with subsequent word (its position in sentence matters)
- removing irrelevant words (one-letter, meaningless in Polish, car-specific)
- removing some Polish endings (not much as lots of them matters)

The above rules are rather *ad-hoc* but work sufficiently well.

## Potential problems

When deploying on [pythonanywhere.org](http://pszczerbiak.pythonanywhere.com/)
I encountered an error related to `sklearn` version incompatibility. As my classifier was pickled with version 0.19, 
please make sure that the same version is installed on the server. If not, simply upgrade the package in bash console 
(see [doc](https://help.pythonanywhere.com/pages/InstallingNewModules/)):
```
pip3.6 install --user --upgrade scikit-learn==0.19.1
```
