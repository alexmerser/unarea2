from unarea_core.ext.restfull import ApiService
from unarea_science.handlers import ListActualProjects, ProjectHandler, CreateProjectHandler

SCIENCE_API = ApiService()

SCIENCE_API.add_resource(ProjectHandler, '/project/<string:project_id>')
SCIENCE_API.add_resource(CreateProjectHandler, '/project')
SCIENCE_API.add_resource(ListActualProjects, '/projects/actual')
