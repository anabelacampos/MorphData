# MorphData Plugin

## Overview
**MorphData** is an open-source ImageJ plugin that automatizes the data extraction process of morphological features of single microglial cells, which can then be used to characterize microglia behavior in the brain of human patients or of animal models of neurological and psychiatric diseases.

Sample data (`MorphData - Input Data Sample.zip` and `MorphData - Output Data Sample.zip`) are provided to the public strictly for educational and academic research purposes.

## Installation
To install **MorphData**, you must first download ImageJ and associated-bundles with preinstalled plugins, such as Fiji (version 1.52t, or later):

```
https://imagej.net/Fiji/Downloads
``` 

To add MorphData as a new plugin to ImageJ you must: 

1. Download the Morph_Data.ijm file; 
2. Put the file in the plugins folder of ImageJ/Fiji itself; 
3. Start ImageJ and the MorphData plugin will be available at the Plugins tab.
 
In addition, the MorphData plugin is reliant on the following ImageJ plugins:

* AnalyzeSkeleton (2D/3D) (version 3.4.2, or later);
* FracLac (version 2015Sep090313a9330, or later).

A detailed description on how to install ImageJ plugins can be found online at:

```
https://imagej.net/plugins
``` 

MorphData also comes with a post-processing script, which you can run if necessary. 
To use this script, you are required to have a Python environment installed (version 3.7.10, or later). 
The easiest way to have such an environment is to download and install Anaconda, a popular open-source Python distribution platform, available at:

```
https://www.anaconda.com/products/individual
``` 

MorphData post-processing script is reliant on the following modules:

* pandas (version 1.2.3, or later);
* tkinter (version 8.6, or later).

To run the post-processing script just open the Python console/prompt and execute it as `python MorphData_PostProcessing.py`.

## File system structure
It is important to clearly structure the single cell images in the file system. 
Ideally, you should create a structure such as the one available on `MorphData - Input Data Sample.zip`. 
To comply with MorphData, while the name of the folders at the first two levels is irrelevant, it is important to guarantee that the last two levels are entitled as _Slice i_, where _i_ identifies different slices, and _Image j_, where _j_ identifies different photomicrographs. 
Single cells should be placed inside the corresponding image folder, being entitled as _Microgliak.tif_, where _k_ identifies each cell within the image folder.

## Operating system
MorphData runs in any operating system compatible with ImageJ, which is available, as a downloadable application, for Windows, macOS, and Linux.

## Contribution
New contributors, of all experience levels, are welcome. Contributions can be proposed using the pull request feature of GitHub or by opening a new issue. These contributions can, among others, focus on the data extraction process, on MorphData performance over different cell types other than microglial cells, improve the documentation, or be made of constructive feedback and suggestions. 

## Citation
You can cite this plugin/code as:

```
Campos, AB., Duarte-Silva, S., Ambrósio, AF., Maciel, P. & Fernandes, B., MorphData: Automating the data extraction process of morphological features of microglial cells in ImageJ. BioRxiv, 2021.08.05.455282, 2021. DOI: 10.1101/2021.08.05.455282
``` 

or alternatively:

```
@article{Campos2021bioRxiv,
  author = {Campos, Ana Bela and Duarte-Silva, Sara and Ambr{\'o}sio, Ant{\'o}nio Francisco and Maciel, Patr{\'\i}cia and Fernandes, Bruno}, 
  title = {MorphData: Automating the data extraction process of morphological features of microglial cells in ImageJ}, 
  journal = {bioRxiv}, 
  year = {2021}, 
  doi = {10.1101/2021.08.05.455282}, 
  publisher = {Cold Spring Harbor Laboratory},
  URL = {https://www.biorxiv.org/content/early/2021/08/06/2021.08.05.455282}
}
``` 

## License
Software made available under a MIT License.

Copyright (c) 2021 anabelacampos.
