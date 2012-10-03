from lightstreamerlite import Session
import multiprocessing

def subscribe1(session):
    print "about to subscribe1"
    session.subscribe(
        update1,
        LS_id='my_id1',
        LS_mode='MERGE',
        LS_schema='one two three',
        LS_data_adapter='my_data_adapter',
        LS_snapshot=True
    )

def subscribe2(session):
    print "about to subscribe2"
    session.subscribe(
        update2,
        LS_id='my_id2',
        LS_mode='MERGE',
        LS_schema='one two three',
        LS_data_adapter='my_data_adapter',
        LS_snapshot=True
    )

def update1(item_id, values):
    print "1:for item_id: %d, received %s" % (item_id, values)

def update2(item_id, values):
    print "2:for item_id: %d, received %s" % (item_id, values)

if __name__ == '__main__':
    session1 = Session(
        host='https://example.com/lightstreamer',
        callback = subscribe1,
        LS_user='my_user',
        LS_password='my_password',
        LS_adapter_set='my_adapter_set',
    )
    session2 = Session(
        host='https://example.com/lightstreamer',
        callback = subscribe2,
        LS_user='my_user',
        LS_password='my_password',
        LS_adapter_set='my_adapter_set',
    )
    multiprocessing.Process(target=session1.run_forever).start()
    multiprocessing.Process(target=session2.run_forever).start()