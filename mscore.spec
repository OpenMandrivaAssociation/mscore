%define srcname MuseScore
%define shortname mscore

Summary:    Linux MusE Score Typesetter
Name:       mscore
Version:    1.0
Release:    %mkrel 1
# (Fedora) rtf2html is LGPLv2+
# paper4.png paper5.png are LGPLv3
# the rest is GPLv2
License:    GPLv2 and LGPLv2+ and LGPLv3
Url:        https://musescore.org
Group:      Publishing
Source0:    http://downloads.sourceforge.net/project/mscore/mscore/%{srcname}-%{version}/%{srcname}-%{version}.tar.bz2
# (Fedora) For building the jazz font
Source1:    mscore-ConvertFont.ff
# (Fedora) For mime types
Source2:    mscore.xml
Patch0:     mscore-1.0-awl-fix-underlink.patch
Patch1:     mscore-1.0-disable-uitools.patch
# (Fedora) use the system default soundfont instead of the deleted, non-free, one
Patch2:     mscore-use-default-soundfont.patch
# (Fedora) don't build the common files (font files, wallpapers, demo song,
# instrument list) into the binary executable to reduce its size. This is also
# useful to inform the users about the existence of different choices for common
# files. The font files need to be separated due to the font packaging guidelines.
Patch3:     mscore-separate-commonfiles.patch
# (Fedora) Split the large documentation into a separate package
Patch4:     mscore-split-doc.patch
# (Fedora) Fix DSO linking.
Patch5:     mscore-dso-linking.patch
# (Fedora) Fix some gcc warnings
Patch6:     mscore-fix-gcc-warnings.patch
# (Mandriva) Fix constant cast (gcc-4.6)
Patch7:     mscore-1.0-fix_const_cast.patch
BuildRequires:  cmake
BuildRequires:  libalsa-devel
BuildRequires:  jackit-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  portaudio-devel
BuildRequires:  qt4-devel > 4:4.4
BuildRequires:  qt4-linguist
Requires:   qtscriptbindings
Requires:   %{name}-fonts = %{version}-%{release}
Requires:   soundfont2-default
Provides:   musescore

%description
MuseScore stands for Linux MusE Score Typesetter.

Features:
      - WYSIWYG design, notes are entered on a "virtual notepaper"
      - TrueType font(s) for printing & display allows for high quality
        scaling to all sizes
      - easy & fast note entry
      - many editing functions
      - MusicXML import/export
      - Midi (SMF) import/export
      - MuseData import
      - Midi input for note entry
      - integrated sequencer and software synthesizer to
        play the score
      - print or create pdf files

%package doc
Summary:       MuseScore documentation
Group:         Development/Other
License:       CC-BY
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch
Obsoletes:     mscore-doc

%description doc
MuseScore is a free cross platform WYSIWYG music notation program.

This package contains the user manual of MuseScore in different languages.

%package fonts
Summary:       MuseScore fonts
Group:         Publishing
License:       GPL+ with exceptions and OFL
BuildArch:     noarch
BuildRequires: fontforge
BuildRequires: tetex
BuildRequires: t1utils
Obsoletes:     mscore-fonts

%description fonts
MuseScore is a free cross platform WYSIWYG music notation program.

This package contains the musical notation fonts for use of MuseScore.

%prep
%setup -q -n %{shortname}-%{version}/%{name}
%patch0 -p2 -b .underlink
%patch1 -p0 -b .disable-uitools

%patch2 -p2 -b .default-soundfont
%patch3 -p2 -b .separate-commonfiles
%patch4 -p2 -b .split-doc
%patch5 -p2 -b .dso-linking
%patch6 -p2 -b .gcc-warnings
%patch7 -p1 -b .const-cast

# only install .qm files
perl -pi -e 's,.*.ts\n,,g' share/locale/CMakeLists.txt

# (Fedora) Remove the precompiled binary
rm rtf2html/rtf2html

# (Fedora) Do not build the bundled qt scripting interface:
sed -i 's|scriptgen||' CMakeLists.txt

# (Fedora) Fix EOL encoding
sed 's|\r||' rtf2html/README > tmpfile
touch -r rtf2html/README tmpfile
mv -f tmpfile rtf2html/README

# (Fedora) Remove preshipped fonts. We will build them from source
rm -f %{shortname}/%{shortname}/fonts/*.ttf

# (Fedora) Disable rpath
sed -i '/rpath/d' %{shortname}/CMakeLists.txt

# (Fedora) this is non-free soundfont "Gort's Minipiano"
rm -f mscore/data/piano1.sf2

# (Fedora) Force specific compile flags:
find . -name CMakeLists.txt -exec sed -i 's|-O3|%{optflags}|' {} \;

%build
%cmake_qt4 -DUSE_GLOBAL_FLUID=ON -DBUILD_SCRIPT_INTERFACE=OFF
%make
make lupdate
make lrelease

# (Fedora) Build fonts from source:
pushd ../%{shortname}/fonts
   # adapt genFont script to mandriva's cmake build dir
   sed -i 's,../../../build/mscore/genft,../../build/mscore/genft,' genFont
   ./genFont
   fontforge %{SOURCE1} MuseJazz.sfd
popd

%install
rm -rf %{buildroot}
%{makeinstall_std} -C build

# Install fonts
mkdir -p %{buildroot}/%{_datadir}/fonts/%{shortname}
install -pm 644 %{shortname}/fonts/%{shortname}*.ttf %{buildroot}/%{_datadir}/fonts/%{shortname}

# Install Manpage
install -D -pm 644 packaging/%{shortname}.1 %{buildroot}/%{_mandir}/man1/%{shortname}.1

# Install mimetype file
install -D -pm 644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/packages/%{shortname}.xml

# (Fedora) gather the doc files in one location
   cp -p rtf2html/ChangeLog        ChangeLog.rtf2html
   cp -p rtf2html/COPYING.LESSER   COPYING.LESSER.rtf2html
   cp -p rtf2html/README           README.rtf2html
   cp -p rtf2html/README.mscore    README.mscore.rtf2html
   cp -p rtf2html/README.ru        README.ru.rtf2html
   cp -p osdabzip/README           README.osdabzip
   cp -p osdabzip/README.mscore    README.mscore.osdabzip
   cp -p share/wallpaper/COPYRIGHT COPYING.wallpaper


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog* NEWS README* COPYING*
%{_bindir}/%{shortname}
%{_datadir}/%{shortname}*
%{_datadir}/applications/%{shortname}.desktop
%{_datadir}/pixmaps/%{shortname}.*
%{_datadir}/mime/packages/%{shortname}.xml
%{_datadir}/soundfonts/TimGM6mb.sf2
%{_mandir}/man1/*
%{qt4plugins}/designer/libawlplugin.so
%exclude %{_datadir}/%{shortname}-1.0/man/

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/%{shortname}-1.0/man/

%files fonts
%{_datadir}/fonts/%{shortname}


%changelog
* Thu Apr 21 2011 Frank Kober <emuse@mandriva.org> 1.0-1mdv2011.0
+ Revision: 656537
- new version 1.0
  o made patch to fix gcc 4.6 compile error (upstream is informed)

* Sat Oct 02 2010 Thomas Spuhler <tspuhler@mandriva.org> 0.9.6.3-1mdv2011.0
+ Revision: 582451
- added 0.9.6.3
- added 0.9.6.3

* Thu Aug 26 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-9mdv2011.0
+ Revision: 573419
- fix typo to make sure all fonts are installed

* Wed Aug 25 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-8mdv2011.0
+ Revision: 573323
+ rebuild (emptylog)

* Wed Aug 25 2010 Olivier Blin <oblin@mandriva.com> 0.9.6.2-7mdv2011.0
+ Revision: 573083
+ rebuild (emptylog)

* Tue Aug 24 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-6mdv2011.0
+ Revision: 572998
+ rebuild (emptylog)

* Tue Aug 24 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-5mdv2011.0
+ Revision: 572929
+ rebuild (emptylog)

* Tue Aug 24 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-4mdv2011.0
+ Revision: 572920
- drop useless requires (slipped by when syncing the spec with Fedora's)

* Wed Aug 18 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-3mdv2011.0
+ Revision: 571245
+ rebuild (emptylog)

* Wed Aug 18 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-2mdv2011.0
+ Revision: 571125
+ rebuild (emptylog)

* Tue Aug 17 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.2-1mdv2011.0
+ Revision: 571071
- update to 0.9.6.2

* Mon Aug 09 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.1-3mdv2011.0
+ Revision: 567805
+ rebuild (emptylog)

* Sun Aug 08 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.1-2mdv2011.0
+ Revision: 567790
+ rebuild (emptylog)

* Sun Aug 08 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.6.1-1mdv2011.0
+ Revision: 567693
- update to 0.9.6.1
- update url
- fix license
- add requires on soundfont2-default
- rediff patch0 (only the awl part is needed, scriptgen build is disabled)
- add various patches and extra sources from Fedora
- split the manual pdf's in a separate package
- split the fonts in a separate package

  + Frank Kober <emuse@mandriva.org>
    - add musescore to Provides for user convenience

* Sun Apr 11 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.5-2mdv2010.1
+ Revision: 533571
- clean spec
- drop patch2, and use a perl command instead

* Fri Dec 25 2009 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.5-1mdv2010.1
+ Revision: 482211
- new version 0.9.5
- rediff patches 0,1,2

* Tue Oct 06 2009 Funda Wang <fwang@mandriva.org> 0.9.3-3mdv2010.0
+ Revision: 454472
- requires qtscriptbinding
- do not build script interface due to conflicts with main package

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 0.9.3-2mdv2010.0
+ Revision: 440161
- rebuild

* Sat Oct 11 2008 Funda Wang <fwang@mandriva.org> 0.9.3-1mdv2009.1
+ Revision: 292266
- new version 0.9.3

* Wed Aug 13 2008 Funda Wang <fwang@mandriva.org> 0.9.2-2mdv2009.0
+ Revision: 271321
- add patch fixing underlink

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat May 10 2008 Funda Wang <fwang@mandriva.org> 0.9.2-1mdv2009.0
+ Revision: 205385
- fix building
- BR qt4-linguist
- New version 0.9.2

* Sat Jan 26 2008 Funda Wang <fwang@mandriva.org> 0.9.1d-1mdv2008.1
+ Revision: 158191
- fix desktop file install
- br portaudio
- 0.9.1d
- New version 0.9.1
- New version 0.9.0

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 21 2007 Funda Wang <fwang@mandriva.org> 0.8.0-1mdv2008.1
+ Revision: 136363
- New version 0.8.0

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 25 2007 Funda Wang <fwang@mandriva.org> 0.7.0.1-2mdv2008.1
+ Revision: 111852
- BR context
- BR texlive
- import mscore


