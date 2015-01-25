AC_INIT(Makefile.in)
AC_PREFIX_DEFAULT(/usr/local)

AC_SUBST(TRANSMISSION)
AC_ARG_WITH(transmission,
    AC_HELP_STRING([--with-transmission=ans],[transmission style (file,syslog) [[file]]]),
    TRANSMISSION="$withval"
    AC_MSG_RESULT([TRANSMISSION=$with_transmission])
    AC_DEFINE_UNQUOTED(TRANSMISSION, "$with_transmission")dnl
    ,
    withval="file"
    AC_MSG_RESULT([TRANSMISSION=$withval])
    TRANSMISSION="$withval"
    AC_DEFINE_UNQUOTED(TRANSMISSION, "$withval"))dnl

AC_SUBST(ETC_DIR)
AC_ARG_WITH(etcDir,
    AC_HELP_STRING([--with-etcDir=ans],[Directory where xalt_db.conf and reverseMapD can be found [[.]]]),
    ETC_DIR="$withval"
    AC_MSG_RESULT([ETC_DIR=$with_etcDir])
    AC_DEFINE_UNQUOTED(ETC_DIR, "$with_etcDir")dnl
    ,
    withval="."
    AC_MSG_RESULT([ETC_DIR=$withval])
    ETC_DIR="$withval"
    AC_DEFINE_UNQUOTED(ETC_DIR, "$withval"))dnl


AC_SUBST(PATH_TO_AS)
AC_SUBST(PATH_TO_HEAD)
AC_SUBST(PATH_TO_BASENAME)
AC_SUBST(PATH_TO_READLINK)
AC_SUBST(PATH_TO_DIRNAME)
AC_SUBST(PATH_TO_GREP)
AC_SUBST(PATH_TO_CAT)
AC_SUBST(PATH_TO_RM)
AC_SUBST(PATH_TO_MKDIR)
AC_SUBST(PATH_TO_AS)
AC_SUBST(PATH_TO_UUIDGEN)
AC_SUBST(USE_CONTRIB_ARGPARSE)

AC_PATH_PROG(PATH_TO_PYTHON, python, "")
AC_PATH_PROG(PATH_TO_GIT, git, "")
AC_PATH_PROG(PATH_TO_AS,as, [])
AC_PATH_PROG(PATH_TO_BASENAME, basename, [])
AC_PATH_PROG(PATH_TO_READLINK, readlink, [])
AC_PATH_PROG(PATH_TO_DIRNAME, dirname, [])
AC_PATH_PROG(PATH_TO_MKDIR,mkdir, [])
AC_PATH_PROG(PATH_TO_HEAD, head, [])
AC_PATH_PROG(PATH_TO_GREP, grep, [])
AC_PATH_PROG(PATH_TO_CAT, cat, [])
AC_PATH_PROG(PATH_TO_RM, rm, [])
AC_PATH_PROG(PATH_TO_UUIDGEN,uuidgen, [])


printf "Use contrib argparse"
USE_CONTRIB_ARGPARSE=no
versionStr=$(python --version 2>&1 | head -1)
major_version=`expr "$versionStr" : 'Python \+\([[0-9]]\+\)\.'`
minor_version=`expr "$versionStr" : 'Python \+[[0-9]]\+\.\([[0-9]]\+\)'`
version=`expr $major_version \* 100000 + $minor_version`
contrib_version=200007
if test $version -lt $contrib_version ; then
  USE_CONTRIB_ARGPARSE=yes
fi
echo "... $USE_CONTRIB_ARGPARSE"



AC_OUTPUT(makefile:Makefile.in)
