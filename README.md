# CO2011 - Mathematical Modeling - Assignment

## What is this?

In this project, I used linear programming to optimize the process of selecting Bitcoin UTXOs for a transaction in order to minimize the transaction fee and reduce the size of the UTXO pool.

This is an assignment for the course CO2011 - Math Modelling at Ho Chi Minh City University of Technology - Semester 2, 2018/2019.

## Report And Jupyter Notebook

* The path to the report is `report/main.pdf`. [link](https://github.com/nhat-m-nguyen/CO2011-Assignment/blob/master/report/main.pdf)
* The path to the Jupyter notebook for model 1 is `src/model1.ipynb`. [link](https://nbviewer.jupyter.org/github/nhat-m-nguyen/CO2011-Assignment/blob/master/src/model1.ipynb)
* The path to the Jupyter notebook for model 2 is `src/model2.ipynb`. [link](https://nbviewer.jupyter.org/github/nhat-m-nguyen/CO2011-Assignment/blob/master/src/model2.ipynb)
* The path to the Jupyter notebook for the result of 2 models is `src/result.ipynb`. [link](https://nbviewer.jupyter.org/github/nhat-m-nguyen/CO2011-Assignment/blob/master/src/result.ipynb)

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
