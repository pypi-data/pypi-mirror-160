# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clustermil']

package_data = \
{'': ['*']}

install_requires = \
['PuLP>=2.6.0,<3.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'clustermil',
    'version': '0.2.0',
    'description': 'clustermil - clustering based multiple instance learning',
    'long_description': '# clustermil\n\n[![Build Status](https://app.travis-ci.com/inoueakimitsu/clustermil.svg?branch=main)](https://app.travis-ci.com/inoueakimitsu/clustermil)\n<a href="https://github.com/inoueakimitsu/clustermil/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/inoueakimitsu/clustermil"></a> \n\nPython package for multiple instance learning (MIL) for large n_instance dataset.\n\n## Features\n\n- support count-based multiple instance assumptions (see [wikipedia](https://en.wikipedia.org/wiki/Multiple_instance_learning#:~:text=Presence-%2C%20threshold-%2C%20and%20count-based%20assumptions%5Bedit%5D))\n- support multi-class setting\n- support scikit-learn Clustering algorithms (such as `MiniBatchKMeans`)\n- fast even if n_instance is large\n\n## Installation\n\n```bash\npip install clustermil\n```\n\n## Usage\n\n```python\n# Prepare follwing dataset\n#\n# - bags ... list of np.ndarray\n#            (num_instance_in_the_bag * num_features)\n# - lower_threshold ... np.ndarray (num_bags * num_classes)\n# - upper_threshold ... np.ndarray (num_bags * num_classes)\n#\n# bags[i_bag] contains not less than lower_thrshold[i_bag, i_class]\n# i_class instances.\n\n# Prepare single-instance clustering algorithms\nfrom sklearn.cluster import MiniBatchKMeans\nn_clusters = 100\nclustering = MiniBatchKMeans(n_clusters=n_clusters)\nclusters = clustering.fit_predict(np.vstack(bags)) # flatten bags into instances\n\n# Prepare one-hot encoder\nfrom sklearn.preprocessing import OneHotEncoder\nonehot_encoder = OneHotEncoder()\nonehot_encoder.fit(clusters)\n\n# generate ClusterMilClassifier with helper function\nfrom clustermil import generate_mil_classifier\n\nmilclassifier = generate_mil_classifier(\n            clustering,\n            onehot_encoder,\n            bags,\n            lower_threshold,\n            upper_threshold,\n            n_clusters)\n\n# after multiple instance learning,\n# you can predict instance class\nmilclassifier.predict([instance_feature])\n```\n\nSee `tests/test_classification.py` for an example of a fully working test data generation process.\n\n## License\n\nclustermil is available under the MIT License.\n',
    'author': 'Inoue Akimitsu',
    'author_email': 'inoue.akimitsu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inoueakimitsu/clustermil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
