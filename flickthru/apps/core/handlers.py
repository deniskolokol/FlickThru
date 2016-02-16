import predictionio
from datetime import datetime
from dateutil import parser

from django.conf import settings


PIO_TZ = predictionio.pytz.timezone(settings.TIME_ZONE)


def ensure_event_time(event_time):
    if event_time is None:
        return datetime.now(PIO_TZ)
    try:
        event_time = parser.parse(event_time)
    except ValueError:
        return datetime.now(PIO_TZ)
    if event_time.tzinfo is None:
        event_time = event_time.replace(tzinfo=PIO_TZ)
    return event_time


class EventHandler(object):
    def __init__(self, access_key=None, event_server_uri=None):
        if any([access_key is None, event_server_uri is None]):
            access_key = settings.PIO_APP_ACCESS_KEY
            event_server_uri = settings.PIO_EVENT_SERVER
        self.client = predictionio.EventClient(access_key, event_server_uri)
        self.exporter = None
        self.filename = None

    def delete_events(self):
        try:
            for event in self.client.get_events():
                self.client.adelete_event(event['eventId'])
        except predictionio.NotFoundError:
            return

    def _do_create_event(self, func, event, entity_type, entity_id,
                         target_entity_type, target_entity_id,
                         properties, event_time):
        return func(event=event,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    target_entity_type=target_entity_type,
                    target_entity_id=target_entity_id,
                    properties=properties,
                    event_time=event_time)

    def create_event(self, event, entity_type, entity_id,
                     target_entity_type=None, target_entity_id=None,
                     properties=None, event_time=None, **kwargs):
        async = kwargs.get('async',  False)
        if async:
            func = self.client.acreate_event
        else:
            func = self.client.create_event
        event_time = ensure_event_time(event_time)
        return self._do_create_event(func, event, entity_type, entity_id,
                                     target_entity_type, target_entity_id,
                                     properties, event_time)

    def _lazy_get_exporter_func(self, **kwargs):
        """kwargs must contain filename"""
        if self.exporter is None:
            self.filename = kwargs['filename']
            self.exporter = predictionio.FileExporter(file_name=self.filename)
        return self.exporter.create_event
        
    def export_event(self, event, entity_type, entity_id,
                     target_entity_type=None, target_entity_id=None,
                     properties=None, event_time=None, **kwargs):
        func = self._lazy_get_exporter_func(**kwargs)
        event_time = ensure_event_time(event_time)
        return self._do_create_event(func, event, entity_type, entity_id,
                                     target_entity_type, target_entity_id,
                                     properties, event_time)

    def close(self):
        if self.exporter is not None:
            subprocess.Popen(['pio', 'import',
                              '--appid', '2', #XXX: how to get app id?
                              '--input', self.filename])
            self.exporter.close()
            print >> sys.stdout, '--\nExported to %s, waiting in queue' % \
                     os.path.abspath(handler.filename)
