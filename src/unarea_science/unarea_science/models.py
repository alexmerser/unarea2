from unarea_core.excaptions import NotFoundError
from unarea_science.data_objects import ScienceProjects

class ScienceProjectsModel(object):
    def __init__(self, science_data):
        self._projects_dao = science_data

    def create_project(self, project_spec):
        new_project = self._projects_dao.objects.create(
            theme=project_spec['theme'],
            abstract=project_spec['abstract'],
            is_thesis=project_spec['is_thesis'],
            year_of_start=project_spec['year_of_start'],
            supervisor_id=project_spec['supervisor_id'],
            performer_id=project_spec['performer_id']
        )
        return new_project

    def get_projects(self, project_ids, filters=None):
        if project_ids and not filters:
            res = self._projects_dao.objects(id__in=project_ids)
            return res
        res = self._projects_dao.objects(is_closed=False)
        return res

    def edit_project(self, project_id, values):
        res = self.get_projects([project_id])
        if not res:
            raise NotFoundError(self._projects_dao, project_id)
        res[0].modify(**values)
        return res[0]

    def delete_project(self, project_id):
        pass

SCIENCE_MODEL = ScienceProjectsModel(ScienceProjects)

        # # science/views.py
        #
        # from flask import Blueprint, render_template, flash, redirect, url_for, request, send_from_directory, g
        # from app.science.utils import write_script, export_themes, create_tmp_for_supervisor, list_supervisor, list_performer
        # from app.science.forms import AddThemeForm, EditThemeForm
        # from app.science.models import Boundthemes
        # from app.decorators import requires_wheel
        # from app import db, app
        # from flask.ext.login import current_user  # for autoGenerate the title page
        # import json
        # import locale
        # import subprocess
        # import shlex
        # import os
        # from models import *
        #
        # mod = Blueprint('science', __name__, url_prefix='/science', template_folder='templates')
        #
        #
        # @mod.route('/')
        # #@requires_wheel
        # def index():
        #     #write_script('actual', json_theme_list())
        #     return render_template('science_index.html')
        #
        #
        # @mod.route('/add_theme', methods=["GET", "POST"])
        # @requires_wheel
        # def add_theme():
        #     """Add new theme in to database."""
        #     form = AddThemeForm.new()
        #     if form.is_submitted():
        #         supervisor = form.supervisor.data  # this all get by ID, names only for presentation in dropdownLists
        #         sid = User.query.filter_by(email='empty@drs.systems').first().id
        #         performer = form.performer.data if form.performer.data != sid else None
        #         theme = form.theme.data
        #         diploma = form.diploma.data
        #         abstract = form.abstract.data
        #         theme = Boundthemes(supervisor, performer, theme, abstract, diploma)
        #         db.session.add(theme)
        #         db.session.commit()
        #         return redirect(url_for('science.theme_edit_list'))
        #     return render_template('theme_add.html', form=form)
        #
        #
        # @mod.route('/edit_list')
        # @requires_wheel
        # def theme_edit_list():
        #     themes = Boundthemes.query.filter_by(is_closed=False).all()
        #     themes_list = [{'id': item.id,
        #                    'supervisor': item.get_supervisor_name(),
        #                    'theme': item.theme,
        #                    'course': item.get_performer_course() if item.id_performer is not None else "none",
        #                    'diploma': item.diploma,
        #                    'performer': item.get_performer_name() if item.id_performer is not None else "none",
        #                    'abstract': item.abstract,
        #                    'year': item.year_of_start} for item in themes]
        #     return render_template('edit_list.html', themes=themes_list)
        #
        #
        # @mod.route('/edit/<theme_id>', methods=["GET", "POST"])
        # @requires_wheel
        # def edit_theme(theme_id):
        #     theme = Boundthemes.query.get_or_404(theme_id)
        #     form = EditThemeForm(request.form, obj=theme)
        #     form.supervisor.choices = [(supervisor['id'], supervisor['name']) for supervisor in list_supervisor()]
        #     form.performer.choices = [(performer['id'], performer['name']) for performer in list_performer()]
        #
        #     form.supervisor.data = theme.id_supervisor
        #     form.performer.data = theme.id_performer
        #
        #     if request.method == 'POST':
        #         form.populate_obj(theme)
        #         theme.id_supervisor = form.supervisor.data
        #         theme.id_performer = form.performer.data
        #         sid = User.query.filter_by(email='empty@drs.systems').first().id
        #         if theme.id_performer == sid:
        #             theme.id_performer = None
        #         db.session.commit()
        #         return redirect(url_for('science.theme_edit_list'))
        #     return render_template('theme_edit.html', form=form)
        #
        #
        # @mod.route('/delete/<theme_id>')
        # @requires_wheel
        # def delete_theme(theme_id):
        #     theme = Boundthemes.query.filter_by(id=theme_id).first()
        #     db.session.delete(theme)
        #     db.session.commit()
        #     return redirect(url_for('science.theme_edit_list'))
        #
        #
        # @mod.route('/export')
        # @requires_wheel
        # def export():
        #     export_themes()
        #     return redirect(url_for('science.theme_edit_list'))
        #
        #
        # @mod.route('/send_to_all')
        # @requires_wheel
        # def send_to_all():
        #     for teacher in list_supervisor():
        #         create_tmp_for_supervisor(teacher.user_id)
        #     return redirect(url_for('science.theme_edit_list'))
        #
        #
        # @mod.route('/archive')
        # def archive():
        #     write_script('archive', json_archive_list())
        #     return render_template('science_archive.html')
        #
        #
        # @mod.route('/one_theme/<int:theme_id>')
        # def one_theme(theme_id):
        #     one = Boundthemes.query.get_or_404(theme_id)
        #     theme = dict()
        #     theme['id'] = one.id
        #     theme['supervisor'] = one.get_supervisor_name()
        #     theme['theme'] = one.theme
        #     theme['course'] = one.get_performer_course() if one.id_performer is not None else "none"
        #     theme['performer'] = one.get_performer_name() if one.id_performer is not None else "none"
        #     theme['group'] = one.get_group_name() if one.id_performer is not None else "none"
        #     theme['diploma'] = "diploma" if one.diploma else ""
        #     theme['abstract'] = one.abstract
        #     theme['year'] = one.year_of_start
        #     return render_template('science_one_theme.html', theme=theme)
        #
        #
        # @mod.route('/storage')
        # @mod.route('/storage/<path:file_name>')
        # def storage(file_name):
        #     """
        #     Storage of text and source base of
        #     science (bachelor and master) works
        #     """
        #     return send_from_directory(app.config['STORAGE'], file_name)
        #
        #
        # @mod.route('/title_page', methods=["GET", "POST"])
        # def auto_title_page():
        #     """
        #     Create title page for course and diploma works
        #     Automatic mode
        #     """
        #     local_encode = locale.getdefaultlocale()
        #
        #     # path to files
        #     path = 'app/tmp/titles/'
        #
        #     # generating file name
        #     file_name = current_user.get_real_name().split()[0]
        #
        #     # get theme of this student
        #     theme = Boundthemes.query.filter_by(id_performer=current_user.id).filter_by(diploma=False).first()
        #
        #     # get pattern file
        #     with open('app/static/title_page.tex', 'r') as f:
        #         pattern = f.read()
        #
        #     print type(theme.theme)
        #
        #     # fill it with values
        #     content = pattern % {'theme': theme.theme.encode(local_encode[1]),
        #                          'performer': current_user.get_real_name().encode(local_encode[1]),
        #                          'supervisor': theme.get_supervisor_name().encode(local_encode[1])}
        #
        #     # write to .tex file
        #     with open(path + file_name + '.tex', 'w') as f:
        #         f.write(content)
        #
        #     # save current directory
        #     current_dir = os.getcwd()
        #     print current_dir
        #     # change work-directory
        #     os.chdir(current_dir + '/' + path)
        #     print os.getcwd()
        #     # convert to pdf
        #     proc = subprocess.Popen(shlex.split('pdflatex ' + file_name + '.tex'))
        #     proc.communicate()
        #
        #     # clean tmp files
        #     os.unlink(file_name + '.tex')
        #     os.unlink(file_name + '.log')
        #     os.unlink(file_name + '.aux')
        #
        #     # change dir back to project root dir
        #     os.chdir(current_dir)
        #
        #     return redirect(url_for('science.index'))
        #
        #
        # @mod.route('/json_theme_list')
        # def json_theme_list():
        #     themes = Boundthemes.query.filter_by(is_closed=False).all()
        #     themes_list = [{'id': item.id,
        #                    'supervisor': item.get_supervisor_name(),
        #                    'theme': item.theme,
        #                    'course': item.get_performer_course() if item.id_performer is not None else "none",
        #                    'group': item.get_group_name() if item.id_performer is not None else "none",
        #                    'diploma': item.diploma,
        #                    'performer': item.get_performer_name() if item.id_performer is not None else "none",
        #                    'abstract': item.abstract,
        #                    'year': item.year_of_start} for item in themes]
        #     return json.dumps(themes_list)
        #
        #
        # @mod.route('/json_archive_list')
        # def json_archive_list():
        #     # TODO: check this query. is it valide for all sets
        #     themes = Boundthemes.query.filter(is_closed=True).all()
        #     themes_list = [{'id': item.id,
        #                     'supervisor': item.get_supervisor_name(),
        #                     'theme': item.theme,
        #                     'performer': item.get_performer_name() if item.id_performer is not None else "none",
        #                     'abstract': item.abstract,
        #                     'year': item.year_of_start} for item in themes]
        #     return json.dumps(themes_list)
