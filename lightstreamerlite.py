import requests

connect_mandatory_keys = ["LS_user", "LS_adapter_set"]
connect_allowed_keys = connect_mandatory_keys[:] + ["LS_password", "LS_requested_max_bandwidth", "LS_content_length", "LS_keepalive_millis"]

subscribe_mandatory_keys = ["LS_id","LS_mode","LS_schema"]
subscribe_allowed_keys = subscribe_mandatory_keys[:] + ["LS_snapshot", "LS_selector", "LS_data_adapter", "LS_requested_buffer_size", "LS_requested_max_frequency"]

class Session(object):
    _table = 0
    _table_callbacks = {}
    _session_id = None

    def __init__(self, host, callback, **kwargs):
        self._host = host
        self._on_create = callback
        self._validate_params(kwargs, connect_mandatory_keys, connect_allowed_keys)
        self._create(**kwargs)

    def _validate_params(self, params, mandatory_keys, allowed_keys):
        for key in mandatory_keys:
            if not params.has_key(key):
                raise Exception("%s is mandatory" % key)
        for key in params.keys():
            if key not in allowed_keys:
                raise Exception("%s is not allowed" % key)

    def _create(self, **kwargs):
        create_params = kwargs
        create_params['LS_polling'] = True
        create_params['LS_polling_millis'] = 5000
        r = requests.post('%s/create_session.txt' % self._host, data=create_params, prefetch=False)
        line_number = 0
        for line in r.iter_lines(chunk_size=1):
            if line:
                line_number += 1
                #print "Debug: line %d is: %s" % (line_number, line)
                if line_number == 1:
                    if not line.startswith('OK'):
                        raise Exception("Not OK: failed to create session")
                    print "Got OK"
                    continue
                if line_number == 2:
                    if not line.startswith("SessionId"):
                        raise Exception("Need SessionId")
                    new_session_id = line.strip().split(":")[1]
                    print "Got SessionId: %s" % new_session_id
                    self._session_id = new_session_id
                    self._on_create(self)
                    continue
                print "Got: %s" % line

    def _bind(self):
        bind_params = {}
        bind_params['LS_session'] = self._session_id
        r = requests.post('%s/bind_session.txt' % self._host, data=bind_params, prefetch=False)
        line_number = 0
        for line in r.iter_lines(chunk_size=1):
            if line:
                line_number += 1
                #print "Debug: line %d is: %s" % (line_number, line)
                if line_number == 1:
                    if not line.startswith('OK'):
                        raise Exception("Not OK: failed to create session")
                    print "Got OK"
                    continue
                if line.startswith("PROBE"):
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
        self._bind()