AM_CPPFLAGS = -I$(top_builddir) -I$(top_srcdir)

EXTRA_DIST = README mcss-cmaes-01.cmaes.params mcss-cmaes-01.mcss.params mcss-cmaes-01.sbml mcss-cmaes-01.target.data mcss-cmaes-01.build.sh

noinst_libdir=$(abs_top_builddir)/examples/mcss-cmaes

noinst_lib_LTLIBRARIES = mcss-cmaes-01.la

mcss_cmaes_01_la_SOURCES = mcss-cmaes-01.cpp
mcss_cmaes_01_la_LDFLAGS = -module -avoid-version
mcss_cmaes_01_la_LIBADD = $(top_builddir)/mcss/libmcss.la

#if !STATIC_ONLY_BUILD
#all-local: mcss-cmaes-01.la
#	cp $(CURDIR)/.libs/*.so $(CURDIR)
#endif

clean-local:
	rm -f *.so
