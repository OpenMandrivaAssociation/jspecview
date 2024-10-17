%{?_javapackages_macros:%_javapackages_macros}
%global svnrel 1171

%if 0%{?fedora}
%else
Epoch:          1
%endif
Name:           jspecview
Version:        2
Release:        5.%{svnrel}svn.0%{?dist}
Summary:        JAVA applets for the display of JCAMP-DX and AnIML/CML spectral files


License:        LGPLv2
URL:            https://jspecview.sourceforge.net/
# Upstream does not release stable source tarballs. Tarball created with attached script.
Source0:        jspecview-%{svnrel}svn.tar.xz
Source1:        generate-sources.sh
# Include missing resources in jar
Patch0:	  	jspecview-resources.patch
# Use system libraries
Patch1:		jspecview-fedorabuild.patch
BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:	itext
BuildRequires:	icedtea-web
# Upstream has hardcoded stuff for eclipse setup
BuildRequires:	eclipse

Requires:       jpackage-utils
Requires:       java

%description
The JSpecView Project provides JAVA applets for the display of
JCAMP-DX and AnIML/CML spectral files.

%package javadoc
Summary:        Javadocs for %{name}

Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n jspecview
%patch0 -p1 -b .resources
%patch1 -p1 -b .fedora

# Fix EOL encodings
for f in JSpecView/extras/{COPYRIGHT,LICENSE,README}.txt; do
 sed 's/\r//' $f > $f.new && \
 touch -r $f $f.new && \
 mv $f.new $f
done

# Remove pre-existing binaries
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# Install netscape.jar
cp -a %{_datadir}/icedtea-web/plugin.jar JSpecView/libs/netscape.jar

%build
# Build library
cd JSpecViewLib
ant
cd ..

cd JSpecView
ant make-application-jar make-applet-jar
cd ..

%install
mkdir -p %{buildroot}%{_javadir}
install -D -p -m 644 -t %{buildroot}%{_javadir}/ JSpecView/build/jspecview.app.*.jar
install -D -p -m 644 -t %{buildroot}%{_javadir}/ JSpecView/build/jspecview.applet.*.jar

# Install symlinks
pushd %{buildroot}%{_javadir}
ln -s jspecview.app.*.jar jspecview.app.jar
ln -s jspecview.applet.*.jar jspecview.applet.jar
popd

# Javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp JSpecView/doc/ %{buildroot}%{_javadocdir}/%{name}

%files
%doc JSpecView/extras/README.txt JSpecView/extras/LICENSE.txt JSpecView/extras/COPYRIGHT.txt
%{_javadir}/jspecview.*.jar

%files javadoc
%{_javadocdir}/%{name}/

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-5.1171svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-4.1171svn
- Compress tarballs with xz (BZ #979821).
- Update to revision 1171.

* Tue May 14 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-4.1169svn
- Dropped classpaths from manifests.
- Update to revision 1169.
- Added missing resources.
- Fixed EOL encodings.

* Tue May 07 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-3.1166svn
- Include license files as well.

* Mon Apr 29 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-2.1166svn
- Include javadoc.

* Fri Apr 05 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-1.1166svn
- Fixed the broken build system, patch sent upstream.
- Update to 1166svn.

* Mon Mar 25 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-1.1158svn
- First release.
