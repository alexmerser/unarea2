from flask import request

from unarea_core.ext.restfull import ResouceHandler
from unarea_core.excaptions import NotFoundError
from unarea_core.lib.api import NotFoundResponse, CreatedApiResponse, SuccessApiResponse, UpdatedApiResponse
from unarea_science.models import SCIENCE_MODEL
from unarea_science.validators import new_project_validator, update_project_validator


class ListActualProjects(ResouceHandler):
    def get(self):
        act = SCIENCE_MODEL.get_projects(None)
        total = len(act)
        return {'total': total, 'projects': [p.json_dict for p in act]}


class CreateProjectHandler(ResouceHandler):
    def post(self):
        new_project_spec = new_project_validator.parse(request.data)
        created = SCIENCE_MODEL.create_project(new_project_spec)
        return CreatedApiResponse(created, created.json_fields())


class ProjectHandler(ResouceHandler):
    def get(self, project_id):
        res = SCIENCE_MODEL.get_projects([project_id])[0]
        return SuccessApiResponse(res, res.json_fields())

    def put(self, project_id):
        diff = update_project_validator.parse(request.data)
        try:
            updated = SCIENCE_MODEL.edit_project(project_id, diff)
            return UpdatedApiResponse(updated, updated.json_fields())
        except NotFoundError as ex:
            NotFoundResponse(ex.message)

    def delete(self, project_id):
        pass
