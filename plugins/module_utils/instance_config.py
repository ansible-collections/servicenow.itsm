import os


def get_combined_instance_config(config_from_params: dict = None):
    if config_from_params is None:
        config_from_params = {}

    instance_env = get_instance_config_from_env()
    return _merge_instance_configs(config_from_params, instance_env)


def get_instance_config_from_env():
    return dict(
        host=os.getenv("SN_HOST"),
        username=os.getenv("SN_USERNAME"),
        password=os.getenv("SN_PASSWORD"),
        client_id=os.getenv("SN_CLIENT_ID"),
        client_secret=_get_secret_from_env(),
        refresh_token=os.getenv("SN_REFRESH_TOKEN"),
        grant_type=os.getenv("SN_GRANT_TYPE"),
        timeout=float(os.getenv("SN_TIMEOUT", 120)),
        client_certificate_file=os.getenv("SN_CLIENT_CERTIFICATE_FILE"),
        client_key_file=os.getenv("SN_CLIENT_KEY_FILE"),
    )


def _get_secret_from_env():
    # can remove this method and simplify in release 3.0.0
    for arg in ("SN_CLIENT_SECRET", "SN_SECRET_ID"):
        value = os.getenv(arg)
        if value is not None:
            return value
    return None


def _merge_instance_configs(instance_config, instance_env):
    instance = {}
    for k, v in instance_env.copy().items():
        if v is not None:
            instance[k] = v

    for k, v in instance_config.items():
        instance[k] = v

    return instance
