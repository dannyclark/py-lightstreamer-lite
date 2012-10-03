py-lightstreamer-lite
=====================

A minimal python lightstreamer client, NOT YET SUITABLE FOR ANY PURPOSE because:
- it doesn't reconnect when lightstreamer finishes a connection or ends a session: this is fairly fundamental since lightstreamer can only keep a connection open as long as the content-length allows (and may or may not close connections for other reasons)
- it's not fully-featured
- it hasn't been tested very much and doesn't have unit tests

On the plus side:
- it is fairly minimal, e.g. LS_* parameters are simply passed through
- it doesn't impose a concurrency model on clients: see examples for running multiple sessions with gevent, multiprocessing or threading