Python Plugin
-------------

The dripline-python library is specifically designed to be extendable using a plugin system.
New classes implemented as plugins are added to the dripline namespace and are available to the provided command line applications in an integrated fashion.
This system should make it easier for projects to develop custom code additions following good programming designs in a way which was not available under dripline version 2 implementations.
It also provides an improved means for dealing with optional features with extra dependencies (both are bundled in the plugin package).

This walkthrough goes through the process of setting up and implementing a very simple plugin to extend the KeyValueStore class with more features.
It is focused on organization, desgin, and installation steps rather than adding complex logic for a particular use case.
The source for a working example plugin is provided in the `dripline-python-extension-example repo <https://github.com/driplineorg/dripline-python-extension-example>`_.
