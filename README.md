# CO2011 - Mathematical Modeling - Assignment

## Report And Jupyter Notebook

* The path to the report is `report/main.pdf`. [link]()
* The path to the Jupyter notebook for model 1 is `src/model1.ipynb`. [link]()
* The path to the Jupyter notebook for model 1 is `src/model1.ipynb`. [link]()

To view the Jupyter notebook, change "Default File Viewer" to "IPython notebook" on the top right corner.

## Brief structure of the project
* `dataset`: The dataset directory
    * `processed`: The directory which stores the preprocessed files and result of models
* `report`: The report directory, which stores the `tex` files and one `pdf` file for the report.
* `src`: Python code and Jupyter notebooks
    * `meta.py`: variables and functions for metadata
    * `model1.py`: code for Model 1
    * `model2.py`: code for Model 2
    * `plot.py`: code for ploting
    * `preprocess.py`: code for preprocessing
    * `realtx.py`: code to process the result of real transactions
    * `transaction.py`: Transaction class
    * `util.py`: utility functions

## Install Mosek

To install Mosek:

```
pip install -f https://download.mosek.com/stable/wheel/index.html Mosek
```

Mosek also requires a license to work. An academic license can be obtained [here](https://www.mosek.com/products/academic-licenses/).