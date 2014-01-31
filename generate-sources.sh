#!/bin/bash

# Read svn release from spec file
svnrel=`grep "global svnrel" jspecview.spec|awk '{print $3}'`
echo "Using svn release $svnrel."

# Get the sources
svn checkout -r ${svnrel} http://svn.code.sf.net/p/jspecview/svn/dev2 jspecview
# Generate tarball
tar Jcf jspecview-${svnrel}svn.tar.xz --exclude=.svn --exclude=\*.class --exclude=\*.jar jspecview
