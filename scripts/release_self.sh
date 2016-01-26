#!/bin/bash

function find_version_number ()
{
  echo "------------------------------------"
  echo "Extracting Git Revision Number"
  echo "------------------------------------"

  SEMANTIC=`cat symantic.version`

  function trim() { echo $1; }

  if [ -z $GIT_HOME ]; then
    if [ -f "/usr/local/bin/git" ]; then
      export GIT_HOME=/usr/local/bin/git
    elif [ -f "/usr/bin/git" ]; then
      export GIT_HOME=/usr/bin/git
    elif [ -f "/bin/git" ]; then
      export GIT_HOME=/bin/git
    else
      ${FRED}GIT Could not be located${RS}
      EXIT_CODE=55
      failed_exit
    fi
  fi

  export GIT_REV_COUNT_RAW=`$GIT_HOME log --pretty=oneline | wc -l`
  export GIT_REV_COUNT=`trim $GIT_REV_COUNT_RAW`
  export GIT_REV=`$GIT_HOME rev-parse HEAD`

  VERSION=$SEMANTIC.$TAG$GIT_REV_COUNT
  echo "Version: $VERSION"
  echo "# THIS IS A GENERATED FILE " > version.properties
  echo "version='$VERSION'" >> version.properties
  echo "revision='$GIT_REV'" >> version.properties
  echo "Git Revision Number is $GIT_REV_COUNT"
  cp version.properties src/VERSION.py
  echo ""
}

find_version_number

python src/github_release.py -u jtownley -o jtownley -v $VERSION -r github_release -n "{tag release}" -k -t token.txt -f one.txt -f two.fork -f *.tho