#!/bin/sh
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

if [ -z "$SN_CLIENT_CERTIFICATE_FILE" ]; then
    SN_CLIENT_CERTIFICATE_FILE="/tmp/SN_CLIENT_CERTIFICATE_FILE"
fi

if [ -z "$SN_CLIENT_KEY_FILE" ]; then
    SN_CLIENT_KEY_FILE="/tmp/SN_CLIENT_KEY_FILE"
fi

yaml_literal_block() {
    key=$1
    value=$2
    printf '%s: |\n' "$key"
    printf '%s\n' "$value" | sed 's/^/  /'
}

{
    echo "sn_host: '$SN_HOST'"
    echo "sn_username: '$SN_USERNAME'"
    echo "sn_password: '$SN_PASSWORD'"
    echo "sn_client_id: '$SN_CLIENT_ID'"
    echo "sn_client_secret: '$SN_CLIENT_SECRET'"
    echo "sn_api_key: '$SN_API_KEY'"
    if [ -n "$SN_CLIENT_CERTIFICATE" ]; then
        yaml_literal_block sn_client_certificate "$SN_CLIENT_CERTIFICATE"
    fi
    if [ -n "$SN_CLIENT_KEY" ]; then
        yaml_literal_block sn_client_key "$SN_CLIENT_KEY"
    fi
    echo "sn_client_certificate_file: '$SN_CLIENT_CERTIFICATE_FILE'"
    echo "sn_client_key_file: '$SN_CLIENT_KEY_FILE'"
    echo "collection_base_dir: '$SCRIPT_DIR/../..'"
} > "$SCRIPT_DIR/integration_config.yml"
