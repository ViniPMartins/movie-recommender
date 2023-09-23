#!/bin/bash

docker build -t ml-api --build-arg BASIC_AUTH_USERNAME_ARG=vinicius --build-arg BASIC_AUTH_PASSWORD_ARG=alura .
