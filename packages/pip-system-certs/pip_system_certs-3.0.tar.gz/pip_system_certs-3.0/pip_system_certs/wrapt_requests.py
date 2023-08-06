from __future__ import absolute_import
import wrapt

## Enable the import to enable type hinting / code navigation below
# import pip._vendor.requests.adapters


# pip master has most commands moved into _internal folder


@wrapt.when_imported('requests')
@wrapt.when_imported('pip._vendor.requests')
@wrapt.when_imported('pipenv.patched.notpip._vendor.requests')
def apply_patches(requests):
    override_ssl_handler(requests.adapters.HTTPAdapter)


def override_ssl_handler(adapter):
    # type: (pip._vendor.requests.adapters.HTTPAdapter) -> None
    
    def init_poolmanager(wrapped, _instance, args, kwargs):
        # type: (pip._vendor.requests.adapters.HTTPAdapter.init_poolmanager, None, list, dict) -> None
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.load_default_certs()
        kwargs['ssl_context'] = ssl_context
        wrapped(*args, **kwargs)

    def cert_verify(wrapped, _instance, args, kwargs):
        # type: (pip._vendor.requests.adapters.HTTPAdapter.cert_verify, None, list, dict) -> None
        wrapped(*args, **kwargs)

        # By default Python requests uses the ca_certs from the certifi module
        # But we want to use the certificate store instead.
        # By clearing the ca_certs variable we force it to fall back on that behaviour (handled in urllib3)
        if "conn" in kwargs:
            conn = kwargs["conn"]
        else:
            conn = args[0]

        conn.ca_certs = None

    wrapt.wrap_function_wrapper(adapter, 'init_poolmanager', init_poolmanager)
    wrapt.wrap_function_wrapper(adapter, 'cert_verify', cert_verify)
