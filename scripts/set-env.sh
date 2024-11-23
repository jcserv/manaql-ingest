#!/bin/bash
export $(grep -v '^#' .env | xargs) > /dev/null 2>&1
