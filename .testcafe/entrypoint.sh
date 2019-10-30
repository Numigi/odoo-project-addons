#!/usr/bin/env bash
set -e

get_odoo_response_code(){
    echo $(curl -o /dev/null --silent --head --write-out '%{http_code}\n' odoo.localtest.me:8069/)
}

odoo_is_ready=$(get_odoo_response_code)
remaining_attempts=30

until [ $odoo_is_ready = '200' ]; do
    if [ $remaining_attempts = 0 ]; then
        echo "Failed to launch testcafe. The Odoo server is unreachable."
        exit 1
    fi
    odoo_is_ready=$(get_odoo_response_code)
    echo "$(date) - waiting for odoo to be ready - remaining attempts: $(( remaining_attempts-- ))"
    sleep 1
done

exec testcafe "$@"
