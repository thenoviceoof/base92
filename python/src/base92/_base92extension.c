#define PY_SSIZE_T_CLEAN
#include <Python.h>

// Lookup table for encoding base92 bits to characters.
static char BASE92_CHARS[91] = (char[]){
        33, 35, 36, 37, 38, 39, 40, 41, 42, 43,
        44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
        54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
        64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
        74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
        84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
        94, 95, 97, 98, 99, 100, 101, 102, 103, 104,
        105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
        115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
        125
};

// Lookup table for decoding base92 characters to bits.
static char BASE92_VALUES[256] = (char[]){
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, 0, -1, 1, 2, 3, 4, 5,
        6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
        26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
        36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
        56, 57, 58, 59, 60, 61, -1, 62, 63, 64,
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
        75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
        85, 86, 87, 88, 89, 90, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1
};

// Encode bytes to base92 string
static PyObject *base92_encode(PyObject *self, PyObject *args) {
    const char *bytstr;
    Py_ssize_t len;
    
    if (!PyArg_ParseTuple(args, "y#", &bytstr, &len)) {
        return NULL;
    }
    
    if (len == 0) {
        return PyUnicode_FromString("~");
    }
    
    // Estimate output size (worst case: each byte becomes ~1.4 characters)
    Py_ssize_t max_output_len = 2 * ((len * 8) / 13);
    char remainder = (len * 8) % 13;
    if (remainder > 0 && remainder < 7) {
            max_output_len += 1;
    } else if (remainder >= 7) {
            max_output_len += 2;
    }
    // +1 for terminating \0.
    char *result = PyMem_Malloc(max_output_len + 1);
    if (!result) {
        return PyErr_NoMemory();
    }
    
    unsigned long long bit_buffer = 0;
    int bit_count = 0;
    Py_ssize_t output_pos = 0;
    
    // Process input bytes
    for (Py_ssize_t i = 0; i < len; i++) {
        // Previously (unsigned char) was left out, and caused crashes.
        bit_buffer = (bit_buffer << 8) | (unsigned char) bytstr[i];
        bit_count += 8;
        
        // Process 13-bit chunks
        while (bit_count >= 13) {
            unsigned long long chunk = bit_buffer >> (bit_count - 13);
            bit_buffer &= (1ULL << (bit_count - 13)) - 1;
            bit_count -= 13;
            
            // Encode as two base92 characters
            // No bounds check necessary: 2**13 = 8192, 8192 / 91 =
            // 90.02. All results fall into [0, 91).
            result[output_pos++] = BASE92_CHARS[chunk / 91];
            result[output_pos++] = BASE92_CHARS[chunk % 91];
        }
    }
    
    // Handle remaining bits
    if (bit_count > 0) {
        if (bit_count < 7) {
            // Pad to 6 bits and encode as single character
            unsigned long long chunk = bit_buffer << (6 - bit_count);
            result[output_pos++] = BASE92_CHARS[chunk];
        } else {
            // Pad to 13 bits and encode as two characters
            unsigned long long chunk = bit_buffer << (13 - bit_count);
            result[output_pos++] = BASE92_CHARS[chunk / 91];
            result[output_pos++] = BASE92_CHARS[chunk % 91];
        }
    }
    
    result[output_pos] = '\0';
    PyObject *py_result = PyUnicode_FromStringAndSize(result, output_pos);
    PyMem_Free(result);
    
    return py_result;
}

// Decode base92 string to bytes
static PyObject *base92_decode(PyObject *self, PyObject *args) {
    const char *bstr;
    Py_ssize_t len;
    
    if (!PyArg_ParseTuple(args, "s#", &bstr, &len)) {
        return NULL;
    }
    
    if (len == 1 && bstr[0] == '~') {
        return PyBytes_FromStringAndSize("", 0);
    }

    if (len == 1) {
            PyErr_SetString(PyExc_ValueError, "1 character is not a valid base92 encoding");
            return NULL;
    }
    
    // Estimate output size
    Py_ssize_t max_output_len = ((len / 2 * 13) + (len % 2 * 6)) / 8;
    char *result = PyMem_Malloc(max_output_len);
    if (!result) {
        return PyErr_NoMemory();
    }
    
    unsigned long long bit_buffer = 0;
    int bit_count = 0;
    Py_ssize_t output_pos = 0;
    
    // Process pairs of characters
    Py_ssize_t i = 0;
    while (i < len - 1) {
        // Decode pair to 13-bit value
        char val1 = BASE92_VALUES[(unsigned char) bstr[i]];
        char val2 = BASE92_VALUES[(unsigned char) bstr[i + 1]];
        
        if (val1 == -1 || val2 == -1) {
            PyMem_Free(result);
            PyErr_SetString(PyExc_ValueError, "Invalid base92 character");
            return NULL;
        }
        
        unsigned long long chunk = val1 * 91 + val2;
        bit_buffer = (bit_buffer << 13) | chunk;
        bit_count += 13;
        
        // Extract complete bytes
        while (bit_count >= 8) {
            char byte_val = bit_buffer >> (bit_count - 8);
            result[output_pos++] = byte_val;
            bit_buffer &= (1ULL << (bit_count - 8)) - 1;
            bit_count -= 8;
        }
        
        i += 2;
    }
    
    // Handle single remaining character
    if (i < len) {
        char val = BASE92_VALUES[(unsigned char)bstr[i]];
        if (val == -1) {
            PyMem_Free(result);
            PyErr_SetString(PyExc_ValueError, "Invalid base92 character");
            return NULL;
        }
        
        bit_buffer = (bit_buffer << 6) | val;
        bit_count += 6;
        
        // Extract any complete bytes
        // We pad the encoding, and each encoded character is smaller
        // than a byte, so any leftover bits are safe to throw away.
        while (bit_count >= 8) {
            char byte_val = bit_buffer >> (bit_count - 8);
            result[output_pos++] = byte_val;
            bit_buffer &= (1ULL << (bit_count - 8)) - 1;
            bit_count -= 8;
        }
    }
    
    PyObject *py_result = PyBytes_FromStringAndSize(result, output_pos);
    PyMem_Free(result);
    
    return py_result;
}

// Module method definitions
static PyMethodDef Base92Methods[] = {
    {"base92_encode", base92_encode, METH_VARARGS, "Encode bytes to base92 string"},
    {"base92_decode", base92_decode, METH_VARARGS, "Decode base92 string to bytes"},
    /* Sentinel */
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef base92module = {
    PyModuleDef_HEAD_INIT,
    "_base92compiled",
    "base92 encoding/decoding module",
    /* The module has no state to track. */
    /* m_size= */ -1,
    Base92Methods
};

// Module initialization
PyMODINIT_FUNC PyInit__base92compiled(void) {
    return PyModule_Create(&base92module);
}
