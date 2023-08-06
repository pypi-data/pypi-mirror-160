|License|


siibra neuroimaging toolbox
=============================

Copyright 2020-2021, Forschungszentrum Jülich GmbH

*Authors: Big Data Analytics Group, Institute of Neuroscience and
Medicine (INM-1), Forschungszentrum Jülich GmbH*


This repository provides a toolbox for `siibra <https://siibra-python.readthedocs.io>`__ which provides functionalities to assign (typically thresholded) whole brain activation maps, as obtained from functional neuroimaging, to brain regions. Given an input volume in the form of a NIfTI file, the toolbox will segregate the input signal into connectec components, and then analyze overlap and correlation of each component with regions defined in an atlas. Per default, the Julich-Brain probabilistic cytoarchitectonic maps [AmuntsEtAl2020]_ defined in MNI152 space are used, and the input volume is assumed in the same physical space. The functionality is strongly inspired by similar functionalities of the popular `SPM anatomy toolbox <https://github.com/inm7/jubrain-anatomy-toolbox>`__ [EickhoffEtAl2005]_.

In the current implementation, the toolbox provides a Python library as well as an extension to the `siibra-cli <https://github.com/FZJ-INM1-BDA/siibra-cli>`__ commandline client. We release installation packages on pypi, so you typically can just run ``pip install siibra-toolbox-neuroimaging`` to install the Python package and commandline extension. 

  **Note** that ``siibra-toolbox-neuroimaging`` is still in early development. Get in touch with us to discuss, and feel free to post issues here on github.


A typical workflow will look like this::

   from siibra_toolbox_neuroimaging import AnatomicalAssignment
   my_input_file = "<filename>.nii.gz"
   analysis = AnatomicalAssignment()
   assignments, component_mask = analysis.analyze(my_input_file)
   analysis.create_report(assignments, my_input_file, component_mask)

The main result is a table listing for each detected component significantly overlapping brain regions and their properties, returned as a pandas DataFrame (``assignments`` in the above example). 
From this, the library can generate a nicely formatted pdf report which also adds structural connectivity profiles for the regions. 
The same report can also be produced using the commandline interface, by the simple call ``siibra assign nifti <filename>.nii.gz``. Future versions will provide an interactive plugin to `siibra-explorer <https://github.com/FZJ-INM1-BDA/siibra-explorer>`__, the interactive web browser hosted at <https://atlases.ebrains.eu/viewer/go/human>. 

This repository contains an example notebook, which you can run in your browser using `mybinder <https://mybinder.org>`__  by clicking the following link:

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/FZJ-INM1-BDA/siibra-toolbox-neuroimaging/HEAD?labpath=example.ipynb


The toolbox relies on the functionalities of ``siibra-python``, documented at https://siibra-python.readthedocs.io. It includes a catalogue of well
documented code examples that walk you through the different concepts
and functionalities. As a new user, it is recommended to go through
these examples - they are easy and will quickly provide you with the
right code snippets that get you started. 

References
----------

.. [EickhoffEtAl2005] Eickhoff S, Stephan KE, Mohlberg H, Grefkes C, Fink GR, Amunts K, Zilles K: A new SPM toolbox for combining probabilistic cytoarchitectonic maps and functional imaging data. NeuroImage 25(4), 1325-1335, 2005
.. [AmuntsEtAl2020] Amunts K, Mohlberg H, Bludau S, Zilles K.: Julich-Brain: A 3D probabilistic atlas of the human brain’s cytoarchitecture. Science. 2020;369(6506):988-992. doi:10.1126/science.abb4588



Acknowledgements
----------------

This software code is funded from the European Union’s Horizon 2020
Framework Programme for Research and Innovation under the Specific Grant
Agreement No. 945539 (Human Brain Project SGA3).

.. acknowledgments-end

.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
