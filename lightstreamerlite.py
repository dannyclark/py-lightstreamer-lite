import requests

connect_mandatory_keys = ["LS_user", "LS_adapter_set"]
connect_allowed_keys = connect_mandatory_keys[:] + ["LS_password", "LS_requested_max_bandwidth", "LS_content_length", "LS_keepalive_millis"]

subscribe_mandatory_keys = ["LS_id","LS_mode","LS_schema"]
subscribe_allowed_keys = subscribe_mandatory_keys[:] + ["LS_snapshot", "LS_selector", "LS_data_adapter", "LS_requested_buffer_size", "LS_requested_max_frequency","LS_snapshot_length"]

class Session(object):
    def __init__(self, host, callback, **kwargs):
        self._table = 0
        self._table_callbacks = {}
        self._session_id = None
        self._connect_args = kwargs

        self._host = host
        self._on_connect = callback
        self._validate_params(kwargs, connect_mandatory_keys, connect_allowed_keys)

    def _validate_params(self, params, mandatory_keys, allowed_keys):
        for key in mandatory_keys:
            if not params.has_key(key):
                raise Exception("%s is mandatory" % key)
        for key in params.keys():
            if key not in allowed_keys:
                raise Exception("%s is not allowed" % key)

    def _connect(self, **kwargs):
        create_params = kwargs
        r = requests.post('%s/create_session.txt' % self._host, data=create_params, prefetch=False)
        if r.status_code != 200:
            raise Exception("Received status code: %d when attempting to connect" % r.status_code)
        line_number = 0
        for line in r.iter_lines(chunk_size=1):
            if line:
                line_number += 1
                #print "Debug: line %d is: %s" % (line_number, line)
                if line_number == 1:
                    if not line.startswith('OK'):
                        raise Exception("Not OK: failed to create session - %s " % line)
                    print "Got OK"
                    continue
                if line_number == 2:
                    if not line.startswith("SessionId"):
                        raise Exception("Need SessionId")
                    new_session_id = line.strip().split(":")[1]
                    print "Got SessionId: %s" % new_session_id
                    self._session_id = new_session_id
                    self._on_connect(self)
                    continue
                if line.startswith("PROBE"):
                    continue
                if "EOS" in line:
                    print "Got EOS: %s" % line
                    continue
                if ":" not in line: # not a header line
                    values = line.split('|')
                    table_id, item_id = [int(x) for x in values[0].split(',')]
                    self._table_callbacks[table_id](item_id, values[1:])
                print "Got: %s" % line

    def subscribe(self, callback, **kwargs):
        self._validate_params(kwargs, subscribe_mandatory_keys, subscribe_allowed_keys)
        params = kwargs
        self._table += 1
        table_id = self._table
        params.update(
            {"LS_table" : table_id,
             "LS_op" : "add",
             "LS_session" : self._session_id}
        )
        r = requests.post('%s/control.txt' % self._host, data=params)
        print "sent control for table_id %d" % (table_id)
        if r.status_code != 200:
             raise Exception("Received status code: %d when attempting to subscribe for table_id: %d" % (r.status_code, table_id))
        self._table_callbacks[table_id] = callback
        for line in r.iter_lines():
            print "reply from control: %s" % line

    def run_forever(self):
        self._connect(**self._connect_args)
