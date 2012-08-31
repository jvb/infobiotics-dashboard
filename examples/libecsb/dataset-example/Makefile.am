AM_CPPFLAGS = -I$(top_builddir) -I$(top_srcdir)

noinst_PROGRAMS = read-dataset-example write-dataset-example

read_dataset_example_SOURCES = read-dataset-example.cpp ExampleDataset.cpp ExampleDataset.h
read_dataset_example_LDADD = $(top_builddir)/ecsb/libecsb.la

write_dataset_example_SOURCES = write-dataset-example.cpp ExampleDataset.cpp ExampleDataset.h
write_dataset_example_LDADD = $(top_builddir)/ecsb/libecsb.la
