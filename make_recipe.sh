#!/bin/bash

# This script creates a recipe git repo on the following server

USER=agoetz
HOSTNAME=droplet.andygoetz.org
SERVER=$USER@$HOSTNAME
REPODIR=/var/www/cookbook.andygoetz.org/public_html/repos
RECIPEREPO="$1"
REMOTEDIR=$REPODIR/$RECIPEREPO
REMOTENAME='droplet'

if [ -z "$RECIPEREPO" ] ; then
    echo "Usage: $0  reponame"
    exit 1
fi



if [ -e "$RECIPEREPO" ] ; then
    echo "repo '$RECIPEREPO' already exists locally"
    exit 1
fi

echo "testing if $RECIPEREPO already exists remotely..."

if ssh $SERVER test -e $REMOTEDIR ; then
    echo "repo '$RECIPEREPO' already exists remotely"
    exit 1
fi


echo 'making remote repo...'

ssh $SERVER git init --bare $REMOTEDIR
ssh $SERVER mv $REMOTEDIR/hooks/post-update.sample $REMOTEDIR/hooks/post-update

echo making local repo...

mkdir $RECIPEREPO
pushd $RECIPEREPO
git init
git remote add $REMOTENAME $SERVER:$REMOTEDIR
popd
