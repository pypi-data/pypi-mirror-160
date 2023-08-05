**Pyseistr**
======

## Description

**Pyseistr** is a python package for the denoising and structural filtering of multi-channel seismic data. 

## Reference
Chen et al., 2022, Pyseistr, In preparation. 

BibTeX:

	@article{pyseistr,
	  title={TBD},
	  author={Authors},
	  journal={TBD},
	  volume={1},
	  number={1},
	  pages={1-10},
	  year={2022}
	}

-----------
## Copyright
    Initial version: Yangkang Chen (chenyk2016@gmail.com), 2021-2022
	Later version: pyseistr developing team, 2022-present
-----------

## License
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)   

-----------

## Install
Using the latest version

    git clone https://github.com/chenyk1990/pyseistr
    cd pyseistr
    pip install -v -e .
or using Pypi

    pip install pyseistr

-----------
## Examples
    The "demo" directory contains all runable scripts to demonstrate different applications of pyseistr. 

-----------
## Dependence Packages
* scipy 
* numpy 
* matplotlib

-----------
## Development
    The development team welcomes voluntary contributions from any open-source enthusiast. 
    If you want to make contribution to this project, feel free to contact the development team. 

-----------
## Contact
    Regarding any questions, bugs, developments, collaborations, please contact  
    Yangkang Chen
    chenyk2016@gmail.com

-----------
## Modules
    somean2d.py -> 2D structure-oriented mean filter
    dip2d.py  -> 2D local slope estimation
    dip3d.py  -> 3D local slope estimation
    divne.py  -> element-wise division constrained by shaping regularization
    somean2d.py -> 2D structure-oriented mean filter 
    somean3d.py -> 3D structure-oriented mean filter 
    somf2d.py -> 2D structure-oriented median filter 
    somf3d.py -> 3D structure-oriented median filter 
-----------
## Counting lines
Counting lines of the Package:

    port install cloc

Using the following comman in src/Pyseistr/ or in the main directory to get a report

    cloc ./

-----------

