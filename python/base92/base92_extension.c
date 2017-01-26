// method "how to write a c-extension" copied in part from https://github.com/Blosc/python-blosc/blob/master/blosc/blosc_extension.c

#define PY_SSIZE_T_CLEAN   /* allows Py_ssize_t in s# format for parsing arguments */
#include "Python.h"

static PyObject *Base92Error;

static void
base92_error(int err, const char *msg)
{
    PyErr_Format(Base92Error, "Error %d %s", err, msg);
}

unsigned char ENCODE_MAPPING[256] = (unsigned char[]){
    33, 35, 36, 37, 38, 39, 40, 41, 42, 43,
    44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
    54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
    64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
    74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
    84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
    94, 95, 97, 98, 99, 100, 101, 102, 103, 104,
    105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
    115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
    125, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0
};
unsigned char DECODE_MAPPING[256] = (unsigned char[]){
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 0, 255, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
    26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
    36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
    46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
    56, 57, 58, 59, 60, 61, 255, 62, 63, 64,
    65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
    75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
    85, 86, 87, 88, 89, 90, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 255, 255, 255, 255, 255
};

unsigned char base92chr_encode(unsigned char byt) {
    return ENCODE_MAPPING[byt];
}

unsigned char base92chr_decode(unsigned char byt) {
    return DECODE_MAPPING[byt];
}

PyDoc_STRVAR(encode__doc__, "encode(input: bytes) -> str -- Return encoded string.\n");

static PyObject *
PyBase92_encode(PyObject *self, PyObject *args)
{
    Py_buffer view;
    PyObject *output;
    char *output_ptr;
    const uint8_t *input;
    const char *format;
    size_t nbytes, size;
    size_t i, j;       // i for raw, j for encoded
    unsigned long workspace; // bits holding bin
    unsigned short wssize;   // number of good bits in workspace
    int tmp;
    unsigned char c;

    /* Accept some kind of input followed by
     * typesize, clevel, shuffle and cname */
#if PY_MAJOR_VERSION <= 2
    /* s* : bytes like object including unicode and anything that supports
     * the buffer interface */
    format = "s*:encode";
#elif PY_MAJOR_VERSION >= 3
    /* y* :bytes like object EXCLUDING unicode and anything that supports
     * the buffer interface. This is the recommended way to accept binary
     * data in Python 3. */
    format = "y*:encode";
#endif
    if (!PyArg_ParseTuple(args, format, &view))
        return NULL;

    nbytes = view.len;
    input = (const uint8_t*)view.buf;

    if (nbytes == 0) {
        PyBuffer_Release(&view);
        /* Alloc memory for encoding */
        if (!(output = PyBytes_FromStringAndSize("~", 1)))
            return NULL;
        return output;
    }

    // precalculate how much space we need to malloc
    size = (nbytes * 8) % 13;
    if (size == 0) {
        size = 2 * ((nbytes * 8) / 13);
    } else if (size < 7) {
        size = 2 * ((nbytes * 8) / 13) + 1;
    } else {
        size = 2 * ((nbytes * 8) / 13) + 2;
    }

    /* Alloc memory for encoding */
    if (!(output = PyBytes_FromStringAndSize(NULL, size))) {
        PyBuffer_Release(&view);
        return NULL;
    }

    output_ptr = PyBytes_AS_STRING(output);

    workspace = 0;
    wssize = 0;
    j = 0;
    for (i = 0; i < nbytes; i++) {
        workspace = workspace << 8 | input[i];
        wssize += 8;
        if (wssize >= 13) {
            tmp = (workspace >> (wssize - 13)) & 8191;
            c = base92chr_encode(tmp / 91);
            if (c == 0) {
                // do something, illegal character
                PyBuffer_Release(&view);
                Py_DECREF(output);
                base92_error(0, "while encoding byte 1");
                return NULL;
            }
            output_ptr[j++] = c;
            c = base92chr_encode(tmp % 91);
            if (c == 0) {
                // do something, illegal character
                PyBuffer_Release(&view);
                Py_DECREF(output);
                base92_error(0, "while encoding byte 2");
                return NULL;
            }
            output_ptr[j++] = c;
            wssize -= 13;
        }
    }
    // encode a last byte
    if (0 < wssize && wssize < 7) {
        tmp = (workspace << (6 - wssize)) & 63;  // pad the right side
        c = base92chr_encode(tmp);
        if (c == 0) {
            // do something, illegal character
            PyBuffer_Release(&view);
            Py_DECREF(output);
            base92_error(0, "while encoding last byte 0");
            return NULL;
        }
        output_ptr[j] = c;
    } else if (7 <= wssize) {
        tmp = (workspace << (13 - wssize)) & 8191; // pad the right side
        c = base92chr_encode(tmp / 91);
        if (c == 0) {
            // do something, illegal character
            PyBuffer_Release(&view);
            Py_DECREF(output);
            base92_error(0, "while encoding last byte 1");
            return NULL;
        }
        output_ptr[j++] = c;
        c = base92chr_encode(tmp % 91);
        if (c == 0) {
            // do something, illegal character
            PyBuffer_Release(&view);
            Py_DECREF(output);
            base92_error(0, "while encoding last byte 2");
            return NULL;
        }
        output_ptr[j] = c;
    }

    PyBuffer_Release(&view);
    return output;
}



PyDoc_STRVAR(decode__doc__, "decode(input: str) -> bytes -- Return decoded data.\n");

static PyObject *
PyBase92_decode(PyObject *self, PyObject *args)
{
    Py_buffer view;
    PyObject *output;
    char *output_ptr;
    const uint8_t *input;
    const char *format;
    size_t nbytes, size, i, j;
    int b1, b2;
    unsigned long workspace;
    unsigned short wssize;

    /* Accept some kind of input followed by
     * typesize, clevel, shuffle and cname */
#if PY_MAJOR_VERSION <= 2
    /* s* : bytes like object including unicode and anything that supports
     * the buffer interface */
    format = "s*:decode";
#elif PY_MAJOR_VERSION >= 3
    /* y* :bytes like object EXCLUDING unicode and anything that supports
     * the buffer interface. This is the recommended way to accept binary
     * data in Python 3. */
    format = "y*:decode";
#endif
    if (!PyArg_ParseTuple(args, format, &view))
        return NULL;

    nbytes = view.len;
    input = (const uint8_t*)view.buf;

    if (nbytes == 0 || (nbytes == 1 && input[0] == 126)) {  // "~"
        PyBuffer_Release(&view);
        /* Alloc memory for decoding */
        if (!(output = PyBytes_FromStringAndSize(NULL, 0)))
            return NULL;
        return output;
    }

    // calculate size
    size = ((nbytes / 2 * 13) + (nbytes % 2 * 6)) / 8;

    /* Alloc memory for decoding */
    if (!(output = PyBytes_FromStringAndSize(NULL, size))) {
        PyBuffer_Release(&view);
        return NULL;
    }

    output_ptr = PyBytes_AS_STRING(output);

    // handle pairs of chars
    workspace = 0;
    wssize = 0;
    j = 0;
    for (i = 0; i + 1 < nbytes; i += 2) {
        b1 = base92chr_decode(input[i]);
        b2 = base92chr_decode(input[i+1]);
        workspace = (workspace << 13) | (b1 * 91 + b2);
        wssize += 13;
        while (wssize >= 8) {
            output_ptr[j++] = (workspace >> (wssize - 8)) & 255;
            wssize -= 8;
        }
    }
    // handle single char
    if (nbytes % 2 == 1) {
        workspace = (workspace << 6) | base92chr_decode(input[nbytes - 1]);
        wssize += 6;
        while (wssize >= 8) {
            output_ptr[j++] = (workspace >> (wssize - 8)) & 255;
            wssize -= 8;
        }
    }

    PyBuffer_Release(&view);
    return output;
}


static PyMethodDef base92_methods[] =
{
    {"encode", (PyCFunction)PyBase92_encode, METH_VARARGS, encode__doc__},
    {"decode", (PyCFunction)PyBase92_decode, METH_VARARGS, decode__doc__},
};


#if PY_MAJOR_VERSION < 3
/* Python 2 module initialization */
PyMODINIT_FUNC
initbase92_extension(void)
{
    PyObject *m;
    m = Py_InitModule("base92_extension", base92_methods);
    if (m == NULL)
        return;

    Base92Error = PyErr_NewException("base92_extension.error", NULL, NULL);
    if (Base92Error != NULL) {
        Py_INCREF(Base92Error);
        PyModule_AddObject(m, "error", Base92Error);
    }
}
# else
/* Python 3 module initialization */
static struct PyModuleDef base92_def = {
    PyModuleDef_HEAD_INIT,
    "base92_extension",
    NULL,
    -1,
    base92_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit_base92_extension(void) {
    PyObject *m = PyModule_Create(&base92_def);

    return m;
}
#endif
