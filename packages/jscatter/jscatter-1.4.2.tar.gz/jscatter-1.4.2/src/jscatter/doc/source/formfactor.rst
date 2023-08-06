formfactor (ff)
===============

.. automodule:: jscatter.formfactor
    :noindex:
   
Form Factors
------------

**General**

.. autosummary::
    guinier
    genGuinier
    ornsteinZernike
    DAB
    guinierPorod
    guinierPorod3d
    powerLaw
    beaucage

----

**Polymer models**

.. autosummary::
    gaussianChain
    polymerCorLength
    ringPolymer
    wormlikeChain
    alternatingCoPolymer

----

**Sphere, Ellipsoid, Cylinder, Cube, CoreShell,..**

.. autosummary::
    sphere
    ellipsoid
    cylinder
    disc
    cuboid
    prism
    superball
    sphereCoreShell
    sphereFuzzySurface
    sphereGaussianCorona
    sphereCoreShellGaussianCorona
    inhomogeneousSphere
    inhomogeneousCylinder
    fuzzyCylinder

----

**Multi shell models**

Multi shell models with may be used to approximate any shell distribution. See examples multiShellSphere.

.. autosummary::
    multilayer
    multiShellSphere
    multiShellEllipsoid
    multiShellDisc
    multiShellCylinder
    multilamellarVesicles

----

**Other**

.. autosummary::
    idealHelix
    pearlNecklace
    linearPearls
    teubnerStrey
    ellipsoidFilledCylinder
    decoratedCoreShell


Cloud of scatterers
-------------------
.. automodule:: jscatter.cloudscattering
    :noindex:

.. autosummary::
    ~jscatter.cloudscattering.cloudScattering
    ~jscatter.cloudscattering.orientedCloudScattering
    ~jscatter.cloudscattering.orientedCloudScattering3Dff

3D formfactor amplitudes (or use orientedCloudScattering) for above 3Dff

.. autosummary::
    ~jscatter.cloudscattering.fa_cuboid
    ~jscatter.cloudscattering.fa_disc
    ~jscatter.cloudscattering.fa_ellipsoid


------

.. automodule:: jscatter.formfactor
    :members:
    :undoc-members:
    :show-inheritance:
   

.. automodule:: jscatter.cloudscattering
    :members:


   
   