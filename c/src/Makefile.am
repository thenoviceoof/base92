include_HEADERS = base92.h

lib_LIBRARIES = libbase92.a
libbase92_a_SOURCES = base92.c

check_PROGRAMS = test
TESTS = $(check_PROGRAMS)
test_SOURCES = test.c
test_LDFLAGS = -L$(top_srcdir)/src
test_LDADD = -lbase92
