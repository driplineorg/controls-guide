.. _python-plugin:

=============
Python Plugin
=============

The dripline-python library is specifically designed to be extendable using a plugin system.
New classes implemented in a plugin are automatically added to the dripline namespace using the namespace package system.
The are available to the provided command line applications in an integrated fashion.
This system should make it easier for projects to develop custom code additions following good programming designs in a way which was not available under dripline version 2 implementations of dripline-python.
It also provides an improved means of dealing with optional features with extra dependencies (both the dripline components and dependencies are bundled in the plugin package).

This walkthrough goes through the process of setting up and implementing a very simple plugin to extend the KeyValueStore class with more features.
It is focused on organization, desgin, and installation steps rather than adding complex logic for a particular use case.
The source for a working example plugin is provided in the `github repo for this document <https://github.com/driplineorg/controls-guide/tree/master/examples/dripline-python-plugin>`_.

It is assumed that you've completed the :ref:`first-mesh-walkthrough` and are already comfortable with building and running dripline services in containers in a mesh.
If not you should go review that guide before proceeding.

Writing a plugin
----------------

Starting with dripline-python v4.0.0, dripline-python supports using namespace packages to add classes to the dripline namespace for use in applications.
This model will allow individual projects to more naturally add their own customized components, including installing any extra dependencies and allowing implementations to span multiple source files in a reasonable way, while still using the common command line tools including ``dl-serve``.
The trade-off is that there is an amount of boilerplate required.

The boilerplate
^^^^^^^^^^^^^^^

In order to add your own components, you can start with this repo as an example. The steps are:

1. Create a new python package (directory with a setup.py file). You can copy the setup.py file and the dripline directory structure from this repo into your own repo for this purpose, be sure to update the name and version.
2. Add the namespace package directory structure, it requires that the ``dripline`` directory be empty except for its subdirectory ``extensions`` and that ``extensions`` have exactly the ``__init__.py`` file as is here.
3. Add the directory for your actual plugin content, here  it is ``dripline/extensions/jitter`` but your plugin should have a different directory name of your choice (probably matching the name of your distribution package in setup.py).
4. Within your plugin's folder (here ``dripline/extensions/jitter``), the ``__init__.py`` file must:
   1. import the classes you've imlemented as part of the plugin
   2. define an ``__all__`` list of the objects you want to add to the ``dripline.extensions`` namespace
   2. define a ``version`` data member which is a scarab.VersionSemantic() instance, here we extract the version from the python package but you can populate that object in whatever method works best for you.
5. Optionally, copy the Dockerfile, make sure that the copy and working directory location used are unique to your plugin and confirm that the base image tag is current (or at least that you're happy with the version being used).
6. Implement your custom classes and run your service in the usual way, ``dl-serve`` will be able to find them at runtime.

Adding implementations
^^^^^^^^^^^^^^^^^^^^^^

This part is entirely dependent on your particular application.
In the case of the jitter plugin, there is one source file (``jitter_endpoints.py``), which implements a single class (``JitterEntity``).
It inherits from KeyValueStore, but overrides the ``on_get`` method to behave somewhat differently; it adds a bit of random offset to the stored value whenever measured.
This shows a method being overridden to support a custom get.
You can also add arbitrary other functions, here ``update_seed`` will set the random seed used by the pseudo-random number generator.

In many cases, you may find that while the provided classes don't do everything you need, they provide close to the desired behavior.
If you inherit from them, you should be able to replace only that functionality that you need to expand, without recreating the rest of the source code (and allowing your class to inherit any bug fixes or feature extensions the may come in future versions).
