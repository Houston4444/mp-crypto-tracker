#!/bin/bash

export FLASK_APP=app
export FLASK_DEBUG=true
export SCHEDULER_API_ENABLED=true
exec flask run