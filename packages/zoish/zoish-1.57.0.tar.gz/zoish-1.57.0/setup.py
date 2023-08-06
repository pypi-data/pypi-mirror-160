# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zoish', 'zoish.examples', 'zoish.feature_selectors', 'zoish.utils']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.0.6,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'fasttreeshap>=0.1.2,<0.2.0',
 'feature-engine>=1.4.1,<2.0.0',
 'imblearn>=0.0,<0.1',
 'lightgbm>=3.3.2,<4.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numba>=0.55.2,<0.56.0',
 'numpy<1.57.0',
 'optuna>=2.10.1,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pip-licenses>=3.5.4,<4.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'shap>=0.41.0,<0.42.0',
 'xgboost>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'zoish',
    'version': '1.57.0',
    'description': 'This project uses shapely values for selecting Top n features compatible with scikit learn pipeline',
    'long_description': '# Zoish\n\nZoish is a package built to ease machine learning development. One of its main parts is a class that uses  [SHAP](https://arxiv.org/abs/1705.07874) (SHapley Additive exPlanation)  for a better feature selection. It is compatible with [scikit-learn](https://scikit-learn.org) pipeline . This package  uses [FastTreeSHAP](https://arxiv.org/abs/2109.09847) while calculation shap values and [SHAP](https://shap.readthedocs.io/en/latest/index.html) for plotting. \n\n\n## Introduction\n\nScallyShapFeatureSelector of Zoish package can receive various parameters. From a tree-based estimator class to its tunning parameters and from Grid search, Random Search, or Optuna to their parameters. Samples will be split to train and validation set, and then optimization will estimate optimal related parameters.\n\n After that, the best subset of features with higher shap values will be returned. This subset can be used as the next steps of the Sklearn pipeline. \n\n\n## Installation\n\nZoish package is available on PyPI and can be installed with pip:\n\n```sh\npip install zoish\n```\n\n\n## Supported estimators\n\n- XGBRegressor  [XGBoost](https://github.com/dmlc/xgboost)\n- XGBClassifier [XGBoost](https://github.com/dmlc/xgboost)\n- RandomForestClassifier \n- RandomForestRegressor \n- CatBoostClassifier \n- CatBoostRegressor \n- BalancedRandomForestClassifier \n- LGBMClassifier [LightGBM](https://github.com/microsoft/LightGBM)\n- LGBMRegressor [LightGBM](https://github.com/microsoft/LightGBM)\n\n## Usage\n\n- Find features using specific tree-based models with the highest shap values after hyper-parameter optimization\n- Plot the shap summary plot for selected features\n- Return a sorted two-column Pandas data frame with a list of features and shap values. \n\n\n## Examples \n\n### Import required libraries\n```\nfrom zoish.feature_selectors.zoish_feature_selector import ScallyShapFeatureSelector\nimport xgboost\nfrom optuna.pruners import HyperbandPruner\nfrom optuna.samplers._tpe.sampler import TPESampler\nfrom sklearn.model_selection import KFold,train_test_split\nimport pandas as pd\nfrom sklearn.pipeline import Pipeline\nfrom feature_engine.imputation import (\n    CategoricalImputer,\n    MeanMedianImputer\n    )\nfrom category_encoders import OrdinalEncoder\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import (\n    r2_score\n    )\nfrom zoish.utils.helper_funcs import catboost\n```\n\n### Computer Hardware Data Set (a regression problem)\n```\nurldata= "https://archive.ics.uci.edu/ml/machine-learning-databases/cpu-performance/machine.data"\n# column names\ncol_names=[\n    "vendor name",\n    "Model Name",\n    "MYCT",\n    "MMIN",\n    "MMAX",\n    "CACH",\n    "CHMIN",\n    "CHMAX",\n    "PRP"\n]\n# read data\ndata = pd.read_csv(urldata,header=None,names=col_names,sep=\',\')\n```\n### Train test split\n```\nX = data.loc[:, data.columns != "PRP"]\ny = data.loc[:, data.columns == "PRP"]\nX_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.33, random_state=42)\n```\n### Find feature types for later use\n```\nint_cols =  X_train.select_dtypes(include=[\'int\']).columns.tolist()\nfloat_cols =  X_train.select_dtypes(include=[\'float\']).columns.tolist()\ncat_cols =  X_train.select_dtypes(include=[\'object\']).columns.tolist()\n```\n\n###  Define Feature selector and set its arguments  \n```\nSFC_CATREG_OPTUNA = ScallyShapFeatureSelector(\n        n_features=5,\n        estimator=catboost.CatBoostRegressor(),\n        estimator_params={\n                  # desired lower bound and upper bound for depth\n                  \'depth\'         : [6,10],\n                  # desired lower bound and upper bound for depth\n                  \'learning_rate\' : [0.05, 0.1],  \n                    },\n        hyper_parameter_optimization_method="optuna",\n        shap_version="v0",\n        measure_of_accuracy="r2",\n        list_of_obligatory_features=[],\n        test_size=0.33,\n        cv=KFold(n_splits=3, random_state=42, shuffle=True),\n        with_shap_summary_plot=True,\n        with_stratified=False,\n        verbose=0,\n        random_state=42,\n        n_jobs=-1,\n        n_iter=100,\n        eval_metric=None,\n        number_of_trials=20,\n        sampler=TPESampler(),\n        pruner=HyperbandPruner(),\n    )\n```\n\n### Build sklearn Pipeline  \n```\npipeline =Pipeline([\n            # int missing values imputers\n            (\'intimputer\', MeanMedianImputer(\n                imputation_method=\'median\', variables=int_cols)),\n            # category missing values imputers\n            (\'catimputer\', CategoricalImputer(variables=cat_cols)),\n            #\n            (\'catencoder\', OrdinalEncoder()),\n            # feature selection\n            (\'SFC_CATREG_OPTUNA\', SFC_CATREG_OPTUNA),\n            # add any regression model from sklearn e.g., LinearRegression\n            (\'regression\', LinearRegression())\n\n\n ])\n\npipeline.fit(X_train,y_train)\ny_pred = pipeline.predict(X_test)\n\n\nprint(\'r2 score : \')\nprint(r2_score(y_test,y_pred))\n\n```\n\nMore examples are available in the [examples](https://github.com/drhosseinjavedani/zoish/tree/main/zoish/examples). \n\n## License\nLicensed under the [BSD 2-Clause](https://opensource.org/licenses/BSD-2-Clause) License.',
    'author': 'drhosseinjavedani',
    'author_email': 'h.javedani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drhosseinjavedani/zoish',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
