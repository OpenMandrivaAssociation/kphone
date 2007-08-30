%define iconname kphone.png 

Summary:	KPhone - SIP user agent
Name:		kphone
Version:	4.2
Release:	%mkrel 8
License:	GPL
Group:		Communications
URL:		http://www.wirlab.net/kphone/index.html
BuildRequires:	autoconf2.1
BuildRequires:	kdelibs-devel >= 3.1.1
BuildRequires:	openssl-devel >= 0.9.6j
Obsoletes:	libkphone3
Obsoletes:	libkphone3-devel
Provides:	libkphone3 libkphone3-devel
BuildRoot:	%_tmppath/%{name}-%{version}-root-%(id -u -n)

Source:		%{name}-%{version}.tar.bz2
Source1:	kphone.menu
Patch1:		kphone-3.0.5-fix-lib64.patch
Patch2:		kphone-4.0.2-mdkmenu.patch
Patch3:		kphone-4.0.2-destdir.patch
Patch4:		kphone-4.1.0-fix-install-po-file.patch
Patch5:		kphone-4.2.0-fix-compile-po.patch
Patch6:		kphone-varargs.patch
Patch7:		kphone-packed.patch
Patch8:		kphone-fix-help.patch
Patch9:		kphone-pt_BR-trans.patch
#(nl) Fix Build with gcc 4.1.1
Patch10:	kphone-4.2-fix-build.patch
Patch11:	kphone-4.2-CVE-2006-2442.patch


# LJB: Don't really know how to deal with this best
%define _pixmapsdir %{_prefix}/share/icons

# Deal with --tag
%define __libtoolize /bin/true

# Taken from arts package
# QTDIR is always /usr/lib/qt3, whether that's a lib64 architecture or
# not (sublibdirs are correctly qualified in the latter case however).
%define qtdir	%{_prefix}/lib/qt3

%description
KPhone is a SIP (Session Initiation Protocol) user agent for Linux,
with which you can initiate VoIP (Voice over IP) connections over the
Internet. It also supports Presence and Instant Messaging.

%prep 
%setup -q -n %{name} 
#%patch1 -p1 -b .lib64
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1 -b .fix_install_po_file
%patch5 -p1 -b .fix_compile_po
%patch6 -p1 -b .varargs
%patch7 -p1 -b .packed
%patch8 -p1 -b .fix_help
%patch9 -p1 -b .pt_BR
%patch10 -p1 -b .fix_build_with_gcc_4.1.1
%patch11 -p1 -b .cve-2006-2442
autoconf

%build
# This will be outside the build root and thus ignored.
# We don't want the .desktop file anyway
kde_appsdir="%{_applnkdir}"; export kde_appsdir
kde_icondir="%{_pixmapsdir}"; export kde_icondir

QTDIR=%qtdir
export LD_LIBRARY_PATH=$QTLIB:$LD_LIBRARY_PATH

# Update config.{sub,guess} to recognize amd64-*
%{?__cputoolize: %{__cputoolize}}

%configure \
        --enable-shared \
        --with-gnu-ld \
        --with-pic \
        --enable-mt \
        --disable-rpath

# crashes build - from copied spec file, not verified: LJB
#	--enable-final \
%make

%install
export PATH=$QTLIB/bin:$PATH
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_menudir}

%makeinstall_std

# Don't want to patch the Makefile
install -m 0644 %SOURCE1 %buildroot/%_menudir/kphone
mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
cp icons/large-kphone.png %{buildroot}%{_liconsdir}/%{iconname}
cp icons/lo-kphone.png %{buildroot}%{_iconsdir}/%{iconname}
cp icons/mini-kphone.png %{buildroot}%{_miconsdir}/%{iconname}

install -d -m 755 $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}):\
    command="%{_bindir}/%{name}"\
    title="Kphone"\
    longtitle="Kphone SIP user agent"\
    needs="x11"\
    section="Internet/Video Conference"\
    icon="%{name}.png"\
    xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Kphone
Comment=Kphone SIP user agent
Exec=kphone
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-VideoConference;
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /usr/bin/update-menus
%postun -p /usr/bin/update-menus

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kphone
%{_menudir}/kphone
%{_datadir}/apps/kphone/icons/*.png
%_iconsdir/%iconname
%_liconsdir/%iconname
%_miconsdir/%iconname  
%_datadir/applications/*

%dir %_datadir/kphone/translations/
%_datadir/kphone/translations/*.qm
		 

%doc CHANGES COPYING INSTALL README


