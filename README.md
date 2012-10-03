py-lightstreamer-lite
=====================

A minimal python lightstreamer client, NOT YET SUITABLE FOR ANY PURPOSE because:
- it doesn't reconnect when lightstreamer finishes a connection or ends a session: this is fairly fundamental since lightstreamer can only keep a connection open as long as the content-length allows (and may or may not close connections for other reasons)
- it's not fully-featured
- it prints to stdout whenever it feels like it
- it hasn't been tested very much and doesn't have unit tests
- it's really just a demonstration

On the plus side:
- it is fairly minimal, e.g. LS_* parameters are simply passed through
- it doesn't impose a concurrency model on clients: see examples for running multiple sessions with gevent, multiprocessing or threading

To get started:
- please see the (/examples) directory
- create a session, create subscriptions in a callback (so lightstreamerlite doesn't attempt to subscribe before it has a session id)
- run session.run_forever() if all you need is a single session and all your processing can be event-driven
- look at the concurrency options (I recommend gevent) if you need more than one session, or for any processing which isn't entirely event-driven

The lightstreamer "text mode protocol" which is (partially) implemented is described here: (http://www.lightstreamer.com/distros/Lightstreamer_Allegro-Presto-Vivace_4_1_Duomo_20120809/Lightstreamer/DOCS-SDKs/sdk_client_generic/doc/Network%20Protocol%20Tutorial.pdf)