# Netcdf Implementation
This module implements netcdf format access with DRB data model. It is able to navigates among the netcdf contents.

## Netcdf Factory and Netcdf Node
The module implements the basic factory model defined in DRB in its node resolver. Based on the python entry point mechanism, this module can be dynamically imported into applications.

The entry point group reference is `drb.impl`.<br/>
The implementation name is `netcdf`.<br/>
The factory class is decribed with implementation `drb_impl_netcdf.drb_impl_signature`.<br/>

The netCDF 4.0 data model is based on recusive structure of Groups each containing a set of Attributes, Dimensions and Variables. It also includes User-defined set of types.
The Drb structure implemented here, reproduces this representation.
Attributes are reported in node as node attributes whereas Dimensions and Values are reported as node children. The raw content is available in Variable node requesting array (xarray, or numpy ndarray types)

## limitations
The current version does not manage child modification and insertion. `DrbNetcdfNode` is currently read only.
The factory to build DrbNetcdfNode supports file directly opening it with path, for other implementation ByteIO or BufferedIOBase, they are manged with a local temporary file, removed when the node is closed..

## Using this module
To include this module into your project, the `drb-impl-netcdf` module shall be referenced into `requirements.txt` file, or the following pip line can be run:
```commandline
pip install drb-impl-netcdf
```
