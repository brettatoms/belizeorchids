#!/bin/bash

#curl --data 'name=master&server=prod.master.example.com' http://localhost:27080/_connect
BASEPATH=`dirname $0`
MONGOOSE_PATH=$BASEPATH/sleepy.mongoose

if ! [ -d $MONGOOSE_PATH ] ; then
    git clone git@github.com:10gen-labs/sleepy.mongoose.git $BASEPATH/sleepy.mongoose
fi

if [ "`pidof mongod`" == "" ] ; then
    echo "starting mongod..."
    mongod &
    sleep 1
else
    echo "mongod already running."
fi

python $MONGOOSE_PATH/httpd.py -x -m "localhost:27017" &
# sleep 5
# curl  --data "server=localhost:27017" http://localhost:27080/_connect 



