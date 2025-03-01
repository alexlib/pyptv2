# cython: language_level=3
# Mimimal vec_utils.pxd with vec3d definition
cdef extern from "optv/vec_utils.h":
    ctypedef struct vec3d:
        double x
        double y
        double z

    ctypedef struct vec2d:
        double x
        double y
