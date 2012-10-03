from lightstreamerlite import Session

def subscribe(session):
    print "about to subscribe"
    session.subscribe(
        update,
        LS_id='my_id',
        LS_mode='MERGE',
        LS_schema='one two three',
        LS_data_adapter='my_data_adapter',
        LS_snapshot=True
    )

def update(item_id, values):
    print "for item_id: %d, received %s" % (item_id, values)

if __name__ == '__main__':
    session = Session(
        host='https://example.com/lightstreamer',
        callback = subscribe,
        LS_user='my_user',
        LS_password='my_password',
        LS_adapter_set='my_adapter_set',
    )
    print "Started Session"
    session.run_forever()