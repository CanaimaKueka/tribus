#!/usr/bin/env bash

for j in ${START_SERVICES}; do
	service ${j} restart
done

if ! id -u ${HOST_USER} >/dev/null 2>&1; then
	useradd -o -u ${HOST_USER_ID} ${HOST_USER}
	echo "${HOST_USER}:tribus" | chpasswd
fi

bash