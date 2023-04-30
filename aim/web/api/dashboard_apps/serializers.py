import json
from aim.web.api.dashboard_apps.models import ExploreState


def explore_state_response_serializer(es_object):
    return (
        {
            'id': es_object.uuid,
            'type': es_object.type,
            'updated_at': es_object.updated_at,
            'created_at': es_object.created_at,
            'state': json.loads(es_object.state),
        }
        if isinstance(es_object, ExploreState)
        else None
    )
