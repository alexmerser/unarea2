import json
from unarea_core.build import create_app as app_factory
from flask_testing import TestCase
from unarea_science.data_objects import ScienceProjects


class UnareaScienceApiSpec(TestCase):
    def create_app(self):
        app = app_factory()
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        ScienceProjects.objects.all().delete()

    def test_create_minimal_science_project(self):
        resp = self.app.post('/api/science/project', data=json.dumps({'theme': 'TestTheme'}))
        assert resp.status_code, 201

    def test_get_project_handler(self):
        tmp = self.app.post('/api/science/project', data=json.dumps({'theme': 'TestTheme1'}))
        assert tmp.status_code, 201

        p_dict = json.loads(tmp.data)
        resp = self.app.get('/api/science/project/%s' % p_dict['id'])
        self.assert200(resp)

        data = json.loads(resp.data)

        self.assertIn('theme', data)
        self.assertIn('id', data)

    def test_put_project_return_404_on_not_existing_id(self):
        resp = self.app.put('/api/science/project/%s' % '55a45131b382052e987b0d51')
        ex_message = json.loads(resp.data)
        self.assert404(resp)
        self.assertEqual(resp.status, "404 NOT FOUND")
        self.assertEqual(ex_message['message'], u'ScienceProjects with id 55a45131b382052e987b0d51 not exists!')

    def test_put_project_success_flow(self):
        new = self.app.post('/api/science/project', data=json.dumps({'theme': 'TestTheme1'}))
        p_dict = json.loads(new.data)
        resp = self.app.put('/api/science/project/%s' % p_dict['id'],
                            data=json.dumps({'theme': 'UPDAGETTheme',
                                             'is_thesis': True,
                                             'abstract': 'YOLOYOBA ABSTRACTTHEN'}))
        updated = json.loads(resp.data)
        self.assertEqual(updated['theme'], u"UPDAGETTheme")
        self.assertTrue(updated['is_thesis'])
        self.assertEqual(updated['abstract'], u'YOLOYOBA ABSTRACTTHEN')

    def test_list_actual_projects(self):
        self.app.post('/api/science/project', data=json.dumps({'theme': 'TestTheme1'}))
        resp = self.app.get('/api/science/projects/actual')
        self.assert200(resp)
        data = json.loads(resp.data)
        self.assertIn('total', data)
        self.assertIn('projects', data)
        self.assertEqual(data['total'], 1)


