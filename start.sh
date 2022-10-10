#!/bin/bash

export FLASK_APP=app
export FLASK_DEBUG=true
export SCHEDULER_API_ENABLED=true
export EACH_MINUTE=true
cd `dirname "$0"`
exec flask run