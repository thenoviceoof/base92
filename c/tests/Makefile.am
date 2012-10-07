INCLUDES = -I$(top_srcdir)/src

check_PROGRAMS = test_empty chr_encode chr_decode simple_test onechar_test hello_world binary_string lengths

TESTS = $(check_PROGRAMS)

test_empty_SOURCES = test_empty.c
test_empty_LDFLAGS = -L$(top_srcdir)/src
test_empty_LDADD = -lbase92

chr_encode_SOURCES = chr_encode.c
chr_encode_LDFLAGS = -L$(top_srcdir)/src
chr_encode_LDADD = -lbase92

chr_decode_SOURCES = chr_decode.c
chr_decode_LDFLAGS = -L$(top_srcdir)/src
chr_decode_LDADD = -lbase92

simple_test_SOURCES = simple_test.c
simple_test_LDFLAGS = -L$(top_srcdir)/src
simple_test_LDADD = -lbase92

onechar_test_SOURCES = onechar_test.c
onechar_test_LDFLAGS = -L$(top_srcdir)/src
onechar_test_LDADD = -lbase92

hello_world_SOURCES = hello_world.c
hello_world_LDFLAGS = -L$(top_srcdir)/src
hello_world_LDADD = -lbase92

binary_string_SOURCES = binary_string.c
binary_string_LDFLAGS = -L$(top_srcdir)/src
binary_string_LDADD = -lbase92

lengths_SOURCES = lengths.c
lengths_LDFLAGS = -L$(top_srcdir)/src
lengths_LDADD = -lbase92
