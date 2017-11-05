# Learned representation for Offline Handwritten Signature Verification

This repository contains the code and instructions to use the trained CNN models described in [1] to extract features for Offline Handwritten Signatures. It also includes links to download extracted features from the GPDS, MCYT, CEDAR datasets.

Based on codes from - https://github.com/luizgh/sigver_wiwd

[1] Hafemann, Luiz G., Robert Sabourin, and Luiz S. Oliveira. "Learning Features for Offline Handwritten Signature Verification using Deep Convolutional Neural Networks" http://dx.doi.org/10.1016/j.patcog.2017.05.012 ([preprint](https://arxiv.org/abs/1705.05787))

Topics:

* [Installation](#installation): How to set-up the dependencies / download the models to extract features from new signatures
* [Datasets](#datasets): Download extracted features (using the proposed models) for the GPDS, MCYT, CEDAR and Brazilian PUC-PR datasets (.mat files - do not require any pre-processing code)


# Installation

## Pre-requisites 

The code is written in Python 2.
```
virtualenv pyenv
source pyenv/bin/activate
```

The following libraries are required

* Scipy version 0.18
* Pillow version 3.0.0
* OpenCV
* Theano
* Lasagne

They can be installed by running the following commands: 

```
pip install scipy
pip install pillow
pip install opencv-python
pip install matplotlib
pip install "Theano==0.9"
pip install https://github.com/Lasagne/Lasagne/archive/master.zip
```

I tested the code in Mac OSX. This code can be used with or without GPUs - to use a GPU with Theano, follow the instructions in this [link](http://deeplearning.net/software/theano/tutorial/using_gpu.html). Note that Theano takes time to compile the model, so it is much faster to instantiate the model once and run forward propagation for many images (instead of calling many times a script that instantiates the model and run forward propagation for a single image).

## Downloading the models

* Clone (or download) this repository
* Download the pre-trained models from the [project page](https://www.etsmtl.ca/Unites-de-recherche/LIVIA/Recherche-et-innovation/Projets/Signature-Verification)
  * Save / unzip the models in the "models" folder

Or simply run the following: 
```
git clone https://github.com/luizgh/sigver_wiwd.git
cd sigver_wiwd/models
wget "https://storage.googleapis.com/luizgh-datasets/models/signet_models.zip"
unzip signet_models.zip
``` 

## Testing 

Run ```jupyter notebook```. 

Look for the notebook "interactive_example.ipynb". You can also visualize it directly [here](https://github.com/luizgh/sigver_wiwd/blob/master/interactive_example.ipynb)

# Datasets

To faciliate further research, we are also making available the features extracted for each of the four datasets used in this work (GPDS, MCYT, CEDAR, Brazilian PUC-PR), using the models SigNet and SigNet-F (with lambda=0.95).

 |Dataset | SigNet | SigNet-F |
 | --- | --- | --- |
 | GPDS | [GPDS_signet](https://storage.googleapis.com/luizgh-datasets/datasets/gpds_signet.zip) | [GPDS_signet_f](https://storage.googleapis.com/luizgh-datasets/datasets/gpds_signet_f.zip) |
| MCYT | [MCYT_signet](https://storage.googleapis.com/luizgh-datasets/datasets/mcyt_signet.zip) | [MCYT_signet_f](https://storage.googleapis.com/luizgh-datasets/datasets/mcyt_signet_f.zip) |
| CEDAR | [CEDAR_signet](https://storage.googleapis.com/luizgh-datasets/datasets/cedar_signet.zip) | [CEDAR_signet_f](https://storage.googleapis.com/luizgh-datasets/datasets/cedar_signet_f.zip) |

There are two files for each user: real_X.mat and forg_X.mat. The first contains a matrix of size N x 2048, containing the feature vectors of N genuine signatures from that user. The second contains a matrix of size M x 2048, containing the feature vectors of each of the M skilled forgeries made targetting the user. 

# Citation

Without these open source works it would have been impossible to come up with a working system:

[1] Hafemann, Luiz G., Robert Sabourin, and Luiz S. Oliveira. "Learning Features for Offline Handwritten Signature Verification using Deep Convolutional Neural Networks" http://dx.doi.org/10.1016/j.patcog.2017.05.012 ([preprint](https://arxiv.org/abs/1705.05787))

We are using the following dataset. Here are the papers that introduced these sets:

GPDS: Vargas, J.F., M.A. Ferrer, C.M. Travieso, and J.B. Alonso. 2007. “Off-Line Handwritten Signature GPDS-960 Corpus.” In Document Analysis and Recognition, 9th I    nternational Conference on, 2:764–68. doi:10.1109/ICDAR.2007.4377018.

MCYT: Ortega-Garcia, Javier, J. Fierrez-Aguilar, D. Simon, J. Gonzalez, M. Faundez-Zanuy, V. Espinosa, A. Satue, et al. 2003. “MCYT Baseline Corpus: A Bimodal Biometric Database.” IEE Proceedings-Vision, Image and Signal Processing 150 (6): 395–401.

CEDAR: Kalera, Meenakshi K., Sargur Srihari, and Aihua Xu. 2004. “Offline Signature Verification and Identification Using Distance Statistics.” International Journal     of Pattern Recognition and Artificial Intelligence 18 (7): 1339–60. doi:10.1142/S0218001404003630.
