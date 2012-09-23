INCLUDES = -I$(top_srcdir)/src

check_PROGRAMS = test_empty hello_world binary_string lengths

TESTS = $(check_PROGRAMS)

test_empty_SOURCES = test_empty.c
test_empty_LDFLAGS = -L$(top_srcdir)/src
test_empty_LDADD = -lbase92

hello_world_SOURCES = hello_world.c
hello_world_LDFLAGS = -L$(top_srcdir)/src
hello_world_LDADD = -lbase92

binary_string_SOURCES = binary_string.c
binary_string_LDFLAGS = -L$(top_srcdir)/src
binary_string_LDADD = -lbase92

lengths_SOURCES = lengths.c
lengths_LDFLAGS = -L$(top_srcdir)/src
lengths_LDADD = -lbase92
