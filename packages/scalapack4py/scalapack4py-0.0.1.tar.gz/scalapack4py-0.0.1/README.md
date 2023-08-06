# Dynamics ScaLAPACK wrapper for Python

Python wrapper for dynamically loaded ScaLAPACK and BLACS libraries

```
from scalapack4py import ScaLAPACK4py, parprint, ordprint
from ctypes import cast, py_object, CDLL, RTLD_GLOBAL

scalapack_lib = CDLL('libscalapack-openmpi.so.2.0', mode=RTLD_GLOBAL)
sl = ScaLAPACK4py(scalapack_lib)

...

descr = sl.wrap_blacs_desc(descr)
locshape = (descr.locrow, descr.loccol)
data = np.ctypeslib.as_array(data, shape=locshape)
sl.scatter(data_src, descr, data)

```