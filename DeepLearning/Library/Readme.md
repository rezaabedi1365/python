
### install tensorflow
Methor1
```
conda create --name tf_env 
    #conda env list
    #conda remove -n ENV_NAME --all
conda activate tf_env
    #conda deactivate tf_env

conda install -c conda-forge tensorflow
conda install -c conda-forge keras

conda install ipykernel
python -m ipykernel install --user --name=tfenv

```
Method2
```
#run cmd with administrator permision
cd c:\windows\users\Your_User
python -m venv myenv
#verify:
dir | findstr myenv

myenv\Scripts\activate

pip install tensorflow
```
verify resault :
```
#new jupyter notbook create and run without error
import tensorflow as tf
from tenserflow import keras

#OR
import tensorflow as tf
print(tf.__version__)
```
verify installation
```
pip list
pip list | findstr tensorflow
pip list | grep tensorflow
which tensorflow # Linux
```

### install pandas
```
pip install pandas
pip show pandas
which pandas
```
import
```
python
>>> import pandas
>>> print(pandas)
```
### install numpy
```
pip install numpy
pip show numpy
which numpy
```
import
```
python
>>> import numpy
>>> print(numpy)
```
### install scikit-learn
```
pip install scikit-learn
pip show scikit-learn
which scikit-learn
```
import
```
python
>>> import scikit-learn
>>> print(scikit-learn)
```
### install matplotlib
```
pip install matplotlib
pip show matplotlib
which matplotlib
```
import
```
python
>>> import matplotlib
>>> print(matplotlib)
```
### install PyTorch
```
pip install torch torchvision torchaudio
pip show torch
which torch
```
import
```
python
>>> import torch 
>>> print(torch )
```
