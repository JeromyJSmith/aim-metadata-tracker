from fastapi import Depends, HTTPException
from aim.web.api.utils import APIRouter  # wrapper for fastapi.APIRouter
from sqlalchemy.orm import Session
from typing import List
from aim.web.api.dashboards.models import Dashboard
from aim.web.api.dashboard_apps.models import ExploreState
from aim.web.api.dashboards.serializers import dashboard_response_serializer
from aim.web.api.db import get_session
from aim.web.api.dashboards.pydantic_models import (
    DashboardOut,
    DashboardCreateIn,
    DashboardUpdateIn
)

dashboards_router = APIRouter()


@dashboards_router.get('/', response_model=List[DashboardOut])
async def dashboards_list_api(session: Session = Depends(get_session)):
    dashboards_query = session.query(Dashboard) \
        .filter(Dashboard.is_archived == False) \
        .order_by(Dashboard.updated_at)  # noqa
    return [
        dashboard_response_serializer(dashboard, session)
        for dashboard in dashboards_query
    ]


@dashboards_router.post('/', status_code=201, response_model=DashboardOut)
async def dashboards_post_api(request_data: DashboardCreateIn, session: Session = Depends(get_session)):
    # create the dashboard object
    dashboard_name = request_data.name
    dashboard_description = request_data.description
    dashboard = Dashboard(dashboard_name, dashboard_description)
    session.add(dashboard)

    # update the app object's foreign key relation
    app_id = str(request_data.app_id)
    if (
        app := session.query(ExploreState)
        .filter(ExploreState.uuid == app_id)
        .first()
    ):
        app.dashboard_id = dashboard.uuid

    # commit db session
    session.commit()

    return dashboard_response_serializer(dashboard, session)


@dashboards_router.get('/{dashboard_id}/', response_model=DashboardOut)
async def dashboards_get_api(dashboard_id: str, session: Session = Depends(get_session)):
    if (
        dashboard := session.query(Dashboard)
        .filter(Dashboard.uuid == dashboard_id, Dashboard.is_archived == False)
        .first()
    ):
        return dashboard_response_serializer(dashboard, session)
    else:
        raise HTTPException(status_code=404)


@dashboards_router.put('/{dashboard_id}/', response_model=DashboardOut)
async def dashboards_put_api(dashboard_id: str, request_data: DashboardUpdateIn,
                             session: Session = Depends(get_session)):
    dashboard = session.query(Dashboard) \
        .filter(Dashboard.uuid == dashboard_id, Dashboard.is_archived == False) \
        .first()  # noqa
    if not dashboard:
        raise HTTPException(status_code=404)
    if dashboard_name := request_data.name:
        dashboard.name = dashboard_name
    if dashboard_description := request_data.description:
        dashboard.description = dashboard_description
    session.commit()

    return dashboard_response_serializer(dashboard, session)


@dashboards_router.delete('/{dashboard_id}/')
async def dashboards_delete_api(dashboard_id: str, session: Session = Depends(get_session)):
    dashboard = session.query(Dashboard) \
        .filter(Dashboard.uuid == dashboard_id, Dashboard.is_archived == False) \
        .first()  # noqa
    if not dashboard:
        raise HTTPException(status_code=404)

    dashboard.is_archived = True
    session.commit()
