from typing import Sequence

from ..core.crypt import (
    upload_keys as crypt_upload_keys,
    search_pub_key,
    verify_key_length,
)
from ..core.error import UserError
from ..utils.config import Config
from ..utils.log import create_logger, log_runtime_info

logger = create_logger(__name__)


@log_runtime_info(logger)
def verify_keylengths_and_upload_keys(
    key_ids: Sequence[str], *, config: Config
) -> None:
    """Verify key lengths and upload keys"""
    keys = frozenset(search_pub_key(k, config.gpg_store, sigs=False) for k in key_ids)
    for key in keys:
        verify_key_length(key)
    upload_keys(key_ids=key_ids, config=config)


@log_runtime_info(logger)
def upload_keys(key_ids: Sequence[str], *, config: Config) -> None:
    """Upload one or more public PGP keys to the keyserver specified in the
    config.
    """
    if config.offline:
        raise UserError("Uploading keys is not possible in the offline mode.")
    if config.keyserver_url is None:
        raise UserError("Keyserver URL is undefined.")
    keys = frozenset(search_pub_key(k, config.gpg_store, sigs=False) for k in key_ids)
    if keys:
        logger.info("Uploading keys '%s'", ", ".join(k.key_id for k in keys))
        crypt_upload_keys(
            [k.fingerprint for k in keys],
            keyserver=config.keyserver_url,
            gpg_store=config.gpg_store,
        )
