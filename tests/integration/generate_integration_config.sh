#!/bin/sh
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

{
    echo "sn_host: '$SN_HOST'"
    echo "sn_username: '$SN_USERNAME'"
    echo "sn_password: '$SN_PASSWORD'"
    echo "collection_base_dir: '$SCRIPT_DIR/../..'"
} > "$SCRIPT_DIR/integration_config.yml"
