%global pkg_name objectweb-asm5
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        5.0.3
Release:        1.4%{?dist}
Summary:        Java bytecode manipulation and analysis framework
License:        BSD
URL:            http://asm.ow2.org/
BuildArch:      noarch

Source0:        http://download.forge.ow2.org/asm/asm-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix_maven}aqute-bnd
BuildRequires:  %{?scl_prefix}maven-local

%description
ASM is an all purpose Java bytecode manipulation and analysis
framework.  It can be used to modify existing classes or dynamically
generate classes, directly in binary form.  Provided common
transformations and analysis algorithms allow to easily assemble
custom complex transformations and code analysis tools.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
This package provides %{summary}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%setup -q -n asm-%{version}
find -name *.jar -delete

sed -i /Class-Path/d archive/*.bnd
sed -i "s/Import-Package:/&org.objectweb.asm,org.objectweb.asm.util,/" archive/asm-xml.bnd
sed -i "s|\${config}/biz.aQute.bnd.jar|`build-classpath aqute-bnd`|" archive/*.xml
sed -i -e '/kind="lib"/d' -e 's|output/eclipse|output/build|' .classpath

%mvn_compat_version : 5 5.0.3
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%ant -Dobjectweb.ant.tasks.path= jar jdoc
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# missing dep org.ow2:ow2 (nothing interesting in there anyway)
%pom_remove_parent output/dist/lib/asm-parent-%{version}.pom

%mvn_artifact output/dist/lib/asm-parent-%{version}.pom
for m in asm asm-analysis asm-commons asm-tree asm-util asm-xml all/asm-all all/asm-debug-all; do
    %mvn_artifact output/dist/lib/${m}-%{version}.pom \
                  output/dist/lib/${m}-%{version}.jar
done
%mvn_install -J output/dist/doc/javadoc/user
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Wed Jan 14 2015 Michal Srb <msrb@redhat.com> - 5.0.3-1.4
- Fix directory ownership

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 5.0.3-1.3
- Mass rebuild 2015-01-13

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 5.0.3-1.2
- Mass rebuild 2015-01-09

* Tue Jan 06 2015 Michal Srb <msrb@redhat.com> - 5.0.3-1.1
- SCL-ize spec file
- Remove dependency on unavailable parent POM
- Drop jpackage_script
- Make it a compat package

* Sun Jul 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.3-1
- Update to upstream version 5.0.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.2-1
- Update to upstream version 5.0.2

* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 5.0.1-2
- SCL-ize package.
- Fix bogus dates in changelog.

* Mon Mar 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.1-1
- Update to upstream version 5.0.1

* Wed Mar 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0-0.3.beta
- Enable asm-debug-all module

* Mon Jan 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0-0.2.beta
- Remove Eclipse Orbit alias

* Tue Dec  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0-0.1.beta
- Update to 5.0 beta

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-7
- Make jetty orbit depmap point to asm-all jar
- Resolves: rhbz#917625

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-6
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#917625

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 0:3.3.1-2
- Use poms produced by the build not foreign ones.
- Adpat to current guidelines.

* Mon Apr 04 2011 Chris Aniszczyk <zx@redhat.com> 0:3.3.1
- Upgrade to 3.3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com>  0:3.2.1-2
- Change depmap parent id to asm (bug #606659)

* Thu Apr 15 2010 Fernando Nasser <fnasser@redhat.com> 0:3.2.1
- Upgrade to 3.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5.1
- build for Fedora

* Thu Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5
- add OSGi manifest (Alexander Kurtakov)

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:3.1-4
- remove Class-Path from MANIFEST.MF
- add unversioned javadoc symlink
- remove javadoc scriptlets
- fix directory ownership
- remove build requirement on dos2unix

* Fri Feb 08 2008 Ralph Apel <r.apel@r-apel.de> - 0:3.1-3jpp
- Add poms and depmap frags with groupId of org.objectweb.asm !
- Add asm-all.jar 
- Add -javadoc Requires post and postun
- Restore Vendor, Distribution

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-2jpp
- Fix EOL of txt files
- Add dependency on jaxp 

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-1jpp
- Upgrade to 3.1

* Wed Aug 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.0-1jpp
- Upgrade to 3.0
- Rename to include objectweb- prefix as requested by ObjectWeb

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.1-2jpp
- First JPP 1.7 build

* Thu Oct 06 2005 Ralph Apel <r.apel at r-apel.de> 0:2.1-1jpp
- Upgrade to 2.1

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:2.0.RC1-1jpp
- First release of the 2.0 line.
