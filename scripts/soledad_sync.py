import os
from ConfigParser import ConfigParser
from leap.soledad.client.api import Soledad
from twisted.internet import defer

# make sure the events server is running before instantiating soledad client
from leap.common.events import server
server.ensure_server()


# get configs from file
parser = ConfigParser()
parser.read('defaults.conf')

HOST = parser.get('server', 'host')

UUID = parser.get('client', 'uuid')
CLIENT_BASEDIR = parser.get('client', 'basedir')
PASSPHRASE = parser.get('client', 'passphrase')

NUM_DOCS = int(parser.get('sync', 'num_docs'))
PAYLOAD = parser.get('sync', 'payload')
AUTH_TOKEN = parser.get('sync', 'auth_token')

STATS_FILE = parser.get('test', 'stats_file')


DO_THESEUS = os.environ.get('THESEUS', False)


def _get_soledad_instance_from_uuid(uuid, passphrase, basedir, server_url,
                                    cert_file, token):
    secrets_path = os.path.join(basedir, '%s.secret' % uuid)
    local_db_path = os.path.join(basedir, '%s.db' % uuid)
    return Soledad(
        uuid,
        unicode(passphrase),
        secrets_path=secrets_path,
        local_db_path=local_db_path,
        server_url=server_url,
        cert_file=cert_file,
        auth_token=token,
        defer_encryption=True,
        syncable=True)


def _get_soledad_instance():
    return _get_soledad_instance_from_uuid(
        UUID, PASSPHRASE, CLIENT_BASEDIR, HOST, '', AUTH_TOKEN)

s = _get_soledad_instance()


def create_docs():
    global s
    # get content for docs
    payload = 'a' * 10
    if os.path.isfile(PAYLOAD):
        with open(PAYLOAD, 'r') as f:
            payload = f.read()
    # create docs
    cd = []
    for i in range(NUM_DOCS):
        cd.append(s.create_doc({'payload': payload}))
    d = defer.gatherResults(cd)
    d.addCallback(
        lambda _: s.get_all_docs())
    d.addCallback(
        lambda result: "%d docs created, %d docs on db"
                       % (NUM_DOCS, result[0]))
    return d


def start_sync():
    global s

    if DO_THESEUS:
        from theseus import Tracer
        t = Tracer()
        t.install()

    def stop_tracing(_):
        if DO_THESEUS:
            with open('callgrind.theseus', 'wb') as outfile:
                t.write_data(outfile)
            print "STOPPED TRACING, DUMPED IN CALLGRIND.THESEUS<<<<"

    d = s.sync()
    d.addCallback(stop_tracing)
    return d


def stats():
    global s
    return s.sync_stats()
