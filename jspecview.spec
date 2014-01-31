%{?_javapackages_macros:%_javapackages_macros}
%global svnrel 1464

Name:           jspecview
Version:        2
Release:        6.%{svnrel}svn.0%{?dist}
Summary:        JAVA applets for the display of JCAMP-DX and AnIML/CML spectral files


License:        LGPLv2
URL:            http://jspecview.sourceforge.net/
# Upstream does not release stable source tarballs. Tarball created with attached script.
Source0:        jspecview-%{svnrel}svn.tar.xz
Source1:        generate-sources.sh
# Fedora patches: no JMol bindings, no signing
Patch0:         jspecview-fedora.patch
BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:  itext
BuildRequires:  icedtea-web
# Upstream has hardcoded stuff for eclipse setup
BuildRequires:  eclipse

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
%patch0 -p1 -b .fedora

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

# Get app version
ver=`ls JSpecView/build/jspecview.app.*.jar| sed "s|JSpecView/build/jspecview.app.||g;s|.jar||g"`
install -D -p -m 644 JSpecView/build/jspecview.app.${ver}.jar %{buildroot}%{_javadir}/jspecview.app.jar
install -D -p -m 644 JSpecView/build/jspecview.applet.${ver}.jar %{buildroot}%{_javadir}/jspecview.applet.jar

# Install symlinks
pushd %{buildroot}%{_javadir}
ln -s jspecview.app.jar jspecview.app.${ver}.jar 
ln -s jspecview.applet.jar jspecview.applet.${ver}.jar 
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
* Wed Jan 01 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-6.1464svn
- Update to revision 1464.

* Tue Oct 22 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2-6.1171svn
- Real .jar is unversioned (BZ #1022126).

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
