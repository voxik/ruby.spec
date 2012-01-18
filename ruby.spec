%global major_version 1
%global minor_version 9
%global teeny_version 3
%global patch_level 0

%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_version_patch_level %{major_minor_version}.%{teeny_version}.%{patch_level}
%global ruby_abi %{major_minor_version}.1

%global ruby_archive %{name}-%{ruby_version}-p%{patch_level}

%global ruby_libdir %{_datadir}/%{name}
%global ruby_libarchdir %{_libdir}/%{name}

# This is the local lib/arch and should not be used for packaging.
%global ruby_sitedir site_ruby
%global ruby_sitelibdir %{_prefix}/local/share/ruby/%{ruby_sitedir}
%global ruby_sitearchdir %{_prefix}/local/%{_lib}/ruby/%{ruby_sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the Fedora repositories.
%global ruby_vendordir vendor_ruby
%global ruby_vendorlibdir %{_datadir}/ruby/%{ruby_vendordir}
%global ruby_vendorarchdir %{_libdir}/ruby/%{ruby_vendordir}

%global rubygems_version 1.8.11

# The RubyGems library has to stay out of Ruby directory three, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/rubygems

# Specify custom RubyGems root.
%global gem_dir %{_datadir}/gems
# TODO: Should we create arch specific rubygems-filesystem?
%global gem_extdir %{_exec_prefix}/lib{,64}/gems

%global rake_version 0.9.2.2
# TODO: The IRB has strange versioning. Keep the Ruby's versioning ATM.
# http://redmine.ruby-lang.org/issues/5313
%global irb_version %{ruby_version_patch_level}
%global rdoc_version 3.9.4
%global bigdecimal_version 1.1.0
%global io_console_version 0.3
%global json_version 1.5.4
%global minitest_version 2.5.1

%global	_normalized_cpu	%(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/;s/armv.*/arm/')

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: %{ruby_version_patch_level}
Release: 4%{?dist}
Group: Development/Languages
License: Ruby or BSD
URL: http://ruby-lang.org/
Source0: ftp://ftp.ruby-lang.org/pub/%{name}/%{major_minor_version}/%{ruby_archive}.tar.gz
Source1: operating_system.rb

# http://redmine.ruby-lang.org/issues/5231
Patch0: ruby-1.9.3-disable-versioned-paths.patch
# TODO: Should be submitted upstream?
Patch1: ruby-1.9.3-arch-specific-dir.patch
# http://redmine.ruby-lang.org/issues/5281
Patch2: ruby-1.9.3-added-site-and-vendor-arch-flags.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
Patch3: ruby-1.9.3-always-use-i386.patch
# http://redmine.ruby-lang.org/issues/5465
Patch4: ruby-1.9.3-fix-s390x-build.patch
# Fix the uninstaller, so that it doesn't say that gem doesn't exist
# when it exists outside of the GEM_HOME (already fixed in the upstream)
Patch5: ruby-1.9.3-rubygems-1.8.11-uninstaller.patch
# http://redmine.ruby-lang.org/issues/5135 - see comment 29
Patch6: ruby-1.9.3-webrick-test-fix.patch
# Already fixed upstream:
# https://github.com/ruby/ruby/commit/f212df564a4e1025f9fb019ce727022a97bfff53
Patch7: ruby-1.9.3-bignum-test-fix.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://redmine.ruby-lang.org/issues/5617
Patch8: ruby-1.9.3-custom-rubygems-location.patch
# Add support for installing binary extensions according to FHS.
# https://github.com/rubygems/rubygems/issues/210
Patch9: rubygems-1.8.11-binary-extensions.patch
# Fixes segfaults when build with GCC 4.7.
# http://bugs.ruby-lang.org/issues/5851
Patch10: ruby-1.9.3-prevent-optimizing-sp.patch
# Fixes json encoding failures when build with GCC 4.7.
# http://bugs.ruby-lang.org/issues/5888
Patch11: ruby-1.9.3-fix-json-parser.patch

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ruby(rubygems) >= %{rubygems_version}

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
BuildRequires: db4-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: tk-devel
# Needed to pass test_set_program_name(TestRubyOptions)
BuildRequires: procps

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package devel
Summary:    A Ruby development environment
Group:      Development/Languages
# Requires:   %{name}-libs = %{version}-%{release}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package libs
Summary:    Libraries necessary to run Ruby
Group:      Development/Libraries
License:    Ruby or BSD
Provides:   ruby(abi) = %{ruby_abi}

%description libs
This package includes the libruby, necessary to run Ruby.

# TODO: Rename or not rename to ruby-rubygems?
%package -n rubygems
Summary:    The Ruby standard for packaging ruby libraries
Version:    %{rubygems_version}
Group:      Development/Libraries
License:    Ruby or MIT
Requires:   ruby(abi) = %{ruby_abi}
Requires:   rubygem(rdoc) = %{rdoc_version}
Requires:   rubygem(io-console) = %{io_console_version}
Provides:   gem = %{version}-%{release}
Provides:   ruby(rubygems) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.


%package -n rubygems-devel
Summary:    Macros and development tools for packagin RubyGems
Version:    %{rubygems_version}
Group:      Development/Libraries
License:    Ruby or MIT
Requires:   ruby(rubygems) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygems-devel
Macros and development tools for packagin RubyGems.


%package -n rubygem-rake
Summary:    Ruby based make-like utility
Version:    %{rake_version}
Group:      Development/Libraries
License:    Ruby or MIT
Requires:   ruby(abi) = %{ruby_abi}
Requires:   ruby(rubygems) = %{rubygems_version}
Provides:   rake = %{version}-%{release}
Provides:   rubygem(rake) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.


%package irb
Summary:    The Interactive Ruby
Version:    %{irb_version}
Group:      Development/Libraries
Requires:   %{name}-libs = %{ruby_version_patch_level}
Provides:   irb = %{version}-%{release}
Provides:   ruby(irb) = %{version}-%{release}
BuildArch:  noarch

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package -n rubygem-rdoc
Summary:    A tool to generate HTML and command-line documentation for Ruby projects
Version:    %{rdoc_version}
Group:      Development/Libraries
License:    GPLv2 and Ruby and MIT
Requires:   ruby(abi) = %{ruby_abi}
Requires:   ruby(rubygems) = %{rubygems_version}
Requires:   ruby(irb) = %{irb_version}
Provides:   rdoc = %{version}-%{release}
Provides:   ri = %{version}-%{release}
Provides:   rubygem(rdoc) = %{version}-%{release}
Obsoletes:  ruby-rdoc < %{version}
Obsoletes:  ruby-ri < %{version}
# TODO: It seems that ri documentation differs from platform to platform due to
# some encoding bugs, therefore the documentation should be split out of this gem
# or kept platform specific.
# https://github.com/rdoc/rdoc/issues/71
# BuildArch:  noarch

%description -n rubygem-rdoc
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.


%package -n rubygem-bigdecimal
Summary:    BigDecimal provides arbitrary-precision floating point decimal arithmetic
Version:    %{bigdecimal_version}
Group:      Development/Libraries
License:    GPL+ or Artistic
Requires:   ruby(abi) = %{ruby_abi}
Requires:   ruby(rubygems) = %{rubygems_version}
Provides:   rubygem(bigdecimal) = %{version}-%{release}

%description -n rubygem-bigdecimal
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect–whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.


%package -n rubygem-io-console
Summary:    IO/Console is a simple console utilizing library
Version:    %{io_console_version}
Group:      Development/Libraries
Requires:   ruby(abi) = %{ruby_abi}
Requires:   ruby(rubygems) = %{rubygems_version}
Provides:   rubygem(io-console) = %{version}-%{release}

%description -n rubygem-io-console
IO/Console provides very simple and portable access to console. It doesn’t
provide higher layer features, such like curses and readline.


%package -n rubygem-json
Summary:    This is a JSON implementation as a Ruby extension in C
Version:    %{json_version}
Group:      Development/Libraries
License:    Ruby or GPLv2
Requires:   ruby(abi) = %{ruby_abi}
Requires:   ruby(rubygems) = %{rubygems_version}
Provides:   rubygem(json) = %{version}-%{release}

%description -n rubygem-json
This is a implementation of the JSON specification according to RFC 4627.
You can think of it as a low fat alternative to XML, if you want to store
data to disk or transmit it over a network rather than use a verbose
markup language.


%package -n rubygem-minitest
Summary:    Minitest provides a complete suite of testing facilities.
Version:    %{minitest_version}
Group:      Development/Libraries
License:    MIT
Requires:   ruby(abi) = %{ruby_abi}
Requires:   ruby(rubygems) = %{rubygems_version}
Provides:   rubygem(minitest) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.


%package tcltk
Summary:    Tcl/Tk interface for scripting language Ruby
Group:      Development/Languages
Requires:   %{name}-libs%{?_isa} = %{ruby_version_patch_level}
Provides:   ruby(tcltk) = %{ruby_version_patch_level}-%{release}

%description tcltk
Tcl/Tk interface for the object-oriented scripting language Ruby.

%prep
%setup -q -n %{ruby_archive}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10
%patch11 -p1

%build
autoconf

%configure \
        --with-rubylibprefix='%{ruby_libdir}' \
        --with-archdir='%{ruby_libarchdir}' \
        --with-sitedir='%{ruby_sitelibdir}' \
        --with-sitearchdir='%{ruby_sitearchdir}' \
        --with-vendordir='%{ruby_vendorlibdir}' \
        --with-vendorarchdir='%{ruby_vendorarchdir}' \
        --with-rubyhdrdir='%{_includedir}' \
        --with-rubygemsdir='%{rubygems_dir}' \
        --disable-rpath \
        --enable-shared \
        --disable-versioned-paths

# Q= makes the build output more verbose and allows to check Fedora
# compiler options.
make %{?_smp_mflags} COPY="cp -p" Q=


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Dump the macros into macro.ruby to use them to build other Ruby libraries.
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.ruby << \EOF
%%ruby_libdir %{_datadir}/%{name}
%%ruby_libarchdir %{_libdir}/%{name}

# This is the local lib/arch and should not be used for packaging.
%%ruby_sitedir site_ruby
%%ruby_sitelibdir %{_prefix}/local/share/ruby/%{ruby_sitedir}
%%ruby_sitearchdir %{_prefix}/local/%{_lib}/ruby/%{ruby_sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the Fedora repositories.
%%ruby_vendordir vendor_ruby
%%ruby_vendorlibdir %{_datadir}/ruby/%{ruby_vendordir}
%%ruby_vendorarchdir %{_libdir}/ruby/%{ruby_vendordir}
EOF

cat >> %{buildroot}%{_sysconfdir}/rpm/macros.rubygems << \EOF
# The RubyGems root folder.
%%gem_dir %{gem_dir}

# Common gem locations and files.
%%gem_instdir %%{gem_dir}/gems/%%{gem_name}-%%{version}
%%gem_extdir %%{_libdir}/gems/exts/%%{gem_name}-%%{version}
%%gem_libdir %%{gem_instdir}/lib
%%gem_cache %%{gem_dir}/cache/%%{gem_name}-%%{version}.gem
%%gem_spec %%{gem_dir}/specifications/%%{gem_name}-%%{version}.gemspec
%%gem_docdir %%{gem_dir}/doc/%%{gem_name}-%%{version}
EOF

# Install custom operating_system.rb.
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
cp %{SOURCE1} %{buildroot}%{rubygems_dir}/rubygems/defaults

# Move gems root into common direcotry, out of Ruby directory structure.
mv %{buildroot}%{ruby_libdir}/gems/%{ruby_abi} %{buildroot}%{gem_dir}

# Create folders for gem binary extensions.
mkdir -p %{buildroot}%{gem_extdir}/exts

# Move bundled rubygems to %%gem_dir and %%gem_extdir
mkdir -p %{buildroot}%{gem_dir}/gems/rake-%{rake_version}/lib
mv %{buildroot}%{ruby_libdir}/rake* %{buildroot}%{gem_dir}/gems/rake-%{rake_version}/lib

mkdir -p %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib
mv %{buildroot}%{ruby_libdir}/rdoc* %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib

mkdir -p %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/exts/bigdecimal-%{bigdecimal_version}/lib
mv %{buildroot}%{ruby_libdir}/bigdecimal %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mv %{buildroot}%{ruby_libarchdir}/bigdecimal.so %{buildroot}%{_libdir}/gems/exts/bigdecimal-%{bigdecimal_version}/lib

mkdir -p %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/exts/io-console-%{io_console_version}/lib/io
mv %{buildroot}%{ruby_libdir}/io %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mv %{buildroot}%{ruby_libarchdir}/io/console.so %{buildroot}%{_libdir}/gems/exts/io-console-%{io_console_version}/lib/io

mkdir -p %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/exts/json-%{json_version}/lib
mv %{buildroot}%{ruby_libdir}/json* %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mv %{buildroot}%{ruby_libarchdir}/json/ %{buildroot}%{_libdir}/gems/exts/json-%{json_version}/lib/

mkdir -p %{buildroot}%{gem_dir}/gems/minitest-%{minitest_version}/lib
mv %{buildroot}%{ruby_libdir}/minitest %{buildroot}%{gem_dir}/gems/minitest-%{minitest_version}/lib

# Adjust the gemspec files so that the gems will load properly
sed -i '2 a\
  s.require_paths = ["lib"]' %{buildroot}/%{gem_dir}/specifications/rake-%{rake_version}.gemspec

sed -i '2 a\
  s.require_paths = ["lib"]' %{buildroot}/%{gem_dir}/specifications/rdoc-%{rdoc_version}.gemspec

sed -i -e '2 a\
  s.require_paths = ["lib"]' -e '3 a\
  s.extensions = ["bigdecimal.so"]' %{buildroot}/%{gem_dir}/specifications/bigdecimal-%{bigdecimal_version}.gemspec

sed -i -e '2 a\
  s.require_paths = ["lib"]' -e '3 a\
  s.extensions = ["io/console.so"]' %{buildroot}/%{gem_dir}/specifications/io-console-%{io_console_version}.gemspec

sed -i -e '2 a\
  s.require_paths = ["lib"]' -e '3 a\
  s.extensions = ["json/ext/parser.so", "json/ext/generator.so"]' %{buildroot}/%{gem_dir}/specifications/json-%{json_version}.gemspec

sed -i '2 a\
  s.require_paths = ["lib"]' %{buildroot}/%{gem_dir}/specifications/minitest-%{minitest_version}.gemspec

%check
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc ChangeLog
%doc GPL
%doc LEGAL
%doc NEWS
%doc README
%lang(ja) %doc README.ja
%doc ToDo
%doc doc/ChangeLog-*
%doc doc/NEWS-*
%{_bindir}/erb
%{_bindir}/ruby
%{_bindir}/testrb
%{_mandir}/man1/erb*
%{_mandir}/man1/ruby*

# http://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Static_Libraries
%exclude %{_libdir}/libruby-static.a

%files devel
%doc COPYING*
%doc GPL
%doc LEGAL
%doc README.EXT
%lang(ja) %doc README.EXT.ja

%config(noreplace) %{_sysconfdir}/rpm/macros.ruby

%{_includedir}/ruby.h
%{_includedir}/ruby
%dir %{_includedir}/%{_normalized_cpu}-%{_target_os}
%{_includedir}/%{_normalized_cpu}-%{_target_os}/ruby

%{_libdir}/libruby.so
%{_libdir}/pkgconfig/ruby-1.9.pc

%files libs
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc GPL
%doc LEGAL
%doc README
%lang(ja) %doc README.ja
# Exclude /usr/local directory since it is supposed to be managed by
# local system administrator.
%exclude %{ruby_sitelibdir}
%exclude %{ruby_sitearchdir}
%{ruby_vendorlibdir}
%{ruby_vendorarchdir}

# List all these files explicitly to prevent surprises
# Platform independent libraries.
%dir %{ruby_libdir}
%{ruby_libdir}/*.rb
%exclude %{ruby_libdir}/*-tk.rb
%exclude %{ruby_libdir}/irb.rb
%exclude %{ruby_libdir}/tcltk.rb
%exclude %{ruby_libdir}/tk*.rb
%{ruby_libdir}/cgi
%{ruby_libdir}/date
%{ruby_libdir}/digest
%{ruby_libdir}/dl
%{ruby_libdir}/drb
%{ruby_libdir}/fiddle
%exclude %{ruby_libdir}/gems
%exclude %{ruby_libdir}/irb
%{ruby_libdir}/matrix
%{ruby_libdir}/net
%{ruby_libdir}/openssl
%{ruby_libdir}/optparse
%{ruby_libdir}/psych
%{ruby_libdir}/racc
%{ruby_libdir}/rbconfig
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper
%{ruby_libdir}/rss
%{ruby_libdir}/shell
%{ruby_libdir}/syck
%{ruby_libdir}/test
%exclude %{ruby_libdir}/tk
%exclude %{ruby_libdir}/tkextlib
%{ruby_libdir}/uri
%{ruby_libdir}/webrick
%{ruby_libdir}/xmlrpc
%{ruby_libdir}/yaml

# Platform specific libraries.
%{_libdir}/libruby.so.*
%dir %{ruby_libarchdir}
%{ruby_libarchdir}/continuation.so
%{ruby_libarchdir}/coverage.so
%{ruby_libarchdir}/curses.so
%{ruby_libarchdir}/date_core.so
%{ruby_libarchdir}/dbm.so
%dir %{ruby_libarchdir}/digest
%{ruby_libarchdir}/digest.so
%{ruby_libarchdir}/digest/bubblebabble.so
%{ruby_libarchdir}/digest/md5.so
%{ruby_libarchdir}/digest/rmd160.so
%{ruby_libarchdir}/digest/sha1.so
%{ruby_libarchdir}/digest/sha2.so
%dir %{ruby_libarchdir}/dl
%{ruby_libarchdir}/dl.so
%{ruby_libarchdir}/dl/callback.so
%dir %{ruby_libarchdir}/enc
%{ruby_libarchdir}/enc/big5.so
%{ruby_libarchdir}/enc/cp949.so
%{ruby_libarchdir}/enc/emacs_mule.so
%{ruby_libarchdir}/enc/encdb.so
%{ruby_libarchdir}/enc/euc_jp.so
%{ruby_libarchdir}/enc/euc_kr.so
%{ruby_libarchdir}/enc/euc_tw.so
%{ruby_libarchdir}/enc/gb18030.so
%{ruby_libarchdir}/enc/gb2312.so
%{ruby_libarchdir}/enc/gbk.so
%{ruby_libarchdir}/enc/iso_8859_1.so
%{ruby_libarchdir}/enc/iso_8859_10.so
%{ruby_libarchdir}/enc/iso_8859_11.so
%{ruby_libarchdir}/enc/iso_8859_13.so
%{ruby_libarchdir}/enc/iso_8859_14.so
%{ruby_libarchdir}/enc/iso_8859_15.so
%{ruby_libarchdir}/enc/iso_8859_16.so
%{ruby_libarchdir}/enc/iso_8859_2.so
%{ruby_libarchdir}/enc/iso_8859_3.so
%{ruby_libarchdir}/enc/iso_8859_4.so
%{ruby_libarchdir}/enc/iso_8859_5.so
%{ruby_libarchdir}/enc/iso_8859_6.so
%{ruby_libarchdir}/enc/iso_8859_7.so
%{ruby_libarchdir}/enc/iso_8859_8.so
%{ruby_libarchdir}/enc/iso_8859_9.so
%{ruby_libarchdir}/enc/koi8_r.so
%{ruby_libarchdir}/enc/koi8_u.so
%{ruby_libarchdir}/enc/shift_jis.so
%dir %{ruby_libarchdir}/enc/trans
%{ruby_libarchdir}/enc/trans/big5.so
%{ruby_libarchdir}/enc/trans/chinese.so
%{ruby_libarchdir}/enc/trans/emoji.so
%{ruby_libarchdir}/enc/trans/emoji_iso2022_kddi.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_docomo.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_kddi.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_softbank.so
%{ruby_libarchdir}/enc/trans/escape.so
%{ruby_libarchdir}/enc/trans/gb18030.so
%{ruby_libarchdir}/enc/trans/gbk.so
%{ruby_libarchdir}/enc/trans/iso2022.so
%{ruby_libarchdir}/enc/trans/japanese.so
%{ruby_libarchdir}/enc/trans/japanese_euc.so
%{ruby_libarchdir}/enc/trans/japanese_sjis.so
%{ruby_libarchdir}/enc/trans/korean.so
%{ruby_libarchdir}/enc/trans/single_byte.so
%{ruby_libarchdir}/enc/trans/transdb.so
%{ruby_libarchdir}/enc/trans/utf8_mac.so
%{ruby_libarchdir}/enc/trans/utf_16_32.so
%{ruby_libarchdir}/enc/utf_16be.so
%{ruby_libarchdir}/enc/utf_16le.so
%{ruby_libarchdir}/enc/utf_32be.so
%{ruby_libarchdir}/enc/utf_32le.so
%{ruby_libarchdir}/enc/windows_1251.so
%{ruby_libarchdir}/etc.so
%{ruby_libarchdir}/fcntl.so
%{ruby_libarchdir}/fiber.so
%{ruby_libarchdir}/fiddle.so
%{ruby_libarchdir}/gdbm.so
%{ruby_libarchdir}/iconv.so
%dir %{ruby_libarchdir}/io
%{ruby_libarchdir}/io/nonblock.so
%{ruby_libarchdir}/io/wait.so
%dir %{ruby_libarchdir}/mathn
%{ruby_libarchdir}/mathn/complex.so
%{ruby_libarchdir}/mathn/rational.so
%{ruby_libarchdir}/nkf.so
%{ruby_libarchdir}/objspace.so
%{ruby_libarchdir}/openssl.so
%{ruby_libarchdir}/pathname.so
%{ruby_libarchdir}/psych.so
%{ruby_libarchdir}/pty.so
%dir %{ruby_libarchdir}/racc
%{ruby_libarchdir}/racc/cparse.so
%{ruby_libarchdir}/rbconfig.rb
%{ruby_libarchdir}/readline.so
%{ruby_libarchdir}/ripper.so
%{ruby_libarchdir}/sdbm.so
%{ruby_libarchdir}/socket.so
%{ruby_libarchdir}/stringio.so
%{ruby_libarchdir}/strscan.so
%{ruby_libarchdir}/syck.so
%{ruby_libarchdir}/syslog.so
%exclude %{ruby_libarchdir}/tcltklib.so
%exclude %{ruby_libarchdir}/tkutil.so
%{ruby_libarchdir}/zlib.so

%files -n rubygems
%{_bindir}/gem
%{rubygems_dir}
%{gem_dir}
%exclude %{gem_dir}/gems/*
%{_exec_prefix}/lib*/gems
%exclude %{_exec_prefix}/lib*/gems/exts/bigdecimal-%{bigdecimal_version}
%exclude %{_exec_prefix}/lib*/gems/exts/io-console-%{io_console_version}
%exclude %{_exec_prefix}/lib*/gems/exts/json-%{json_version}
%exclude %{gem_dir}/gems/rake-%{rake_version}
%exclude %{gem_dir}/gems/rdoc-%{rdoc_version}
%exclude %{gem_dir}/specifications/bigdecimal-%{bigdecimal_version}.gemspec
%exclude %{gem_dir}/specifications/io-console-%{io_console_version}.gemspec
%exclude %{gem_dir}/specifications/json-%{json_version}.gemspec
%exclude %{gem_dir}/specifications/minitest-%{minitest_version}.gemspec
%exclude %{gem_dir}/specifications/rake-%{rake_version}.gemspec
%exclude %{gem_dir}/specifications/rdoc-%{rdoc_version}.gemspec

%files -n rubygems-devel
%config(noreplace) %{_sysconfdir}/rpm/macros.rubygems

%files -n rubygem-rake
%{_bindir}/rake
%{gem_dir}/gems/rake-%{rake_version}
%{gem_dir}/specifications/rake-%{rake_version}.gemspec
%{_mandir}/man1/rake.1*

%files irb
%{_bindir}/irb
%{ruby_libdir}/irb.rb
%{ruby_libdir}/irb
%{_mandir}/man1/irb.1*

%files -n rubygem-rdoc
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_dir}/gems/rdoc-%{rdoc_version}
%{gem_dir}/specifications/rdoc-%{rdoc_version}.gemspec
%{_mandir}/man1/ri*
%{_datadir}/ri

%files -n rubygem-bigdecimal
%{_libdir}/gems/exts/bigdecimal-%{bigdecimal_version}
%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}
%{gem_dir}/specifications/bigdecimal-%{bigdecimal_version}.gemspec

%files -n rubygem-io-console
%{_libdir}/gems/exts/io-console-%{io_console_version}
%{gem_dir}/gems/io-console-%{io_console_version}
%{gem_dir}/specifications/io-console-%{io_console_version}.gemspec

%files -n rubygem-json
%{_libdir}/gems/exts/json-%{json_version}
%{gem_dir}/gems/json-%{json_version}
%{gem_dir}/specifications/json-%{json_version}.gemspec

%files -n rubygem-minitest
%{gem_dir}/gems/minitest-%{minitest_version}
%{gem_dir}/specifications/minitest-%{minitest_version}.gemspec

%files tcltk
%{ruby_libdir}/*-tk.rb
%{ruby_libdir}/tcltk.rb
%{ruby_libdir}/tk*.rb
%{ruby_libarchdir}/tcltklib.so
%{ruby_libarchdir}/tkutil.so
%{ruby_libdir}/tk
%{ruby_libdir}/tkextlib

%changelog
* Tue Jan 17 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-4
- Bundled gems moved into dedicated directories and subpackages.
- Create and own RubyGems directories for binary extensions.
- Fix build with GCC 4.7.

* Wed Jan 04 2012 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-3
- Fix RHEL build.
- Fixed directory ownership.
- Verose build output.

* Wed Dec 14 2011 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-2
- Install RubyGems outside of Ruby directory structure.
- RubyGems has not its own -devel subpackage.
- Enhanced macros.ruby and macros.rubygems.
- All tests are green now (bkabrda).

* Tue Sep 23 2011 Vít Ondruch <vondruch@redhat.com> - 1.9.3.0-1
- Initial package
