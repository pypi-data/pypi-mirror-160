# -*- coding:utf-8 -*-

import gdpy
import mock
import json

from gdpy.http import requests
from unittests.common import *
from gdpy import exceptions


def makeResponse200():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '"{success}"'
    return MockResponse_base(status, headers, response)


def makeResponse200_activatetask():
    status = 200
    headers = {},
    response = requests.Response
    response.text = u'{"task_id": "task_id", "task_name": "task_name"}'
    return MockResponse_base(status, headers, response)


def makeResponse202_activatetask():
    status = 202
    headers = {},
    response = requests.Response
    response.text = u'{"split": [], "splitting": [{"submit": true, "name": "test_account:/home/test_1.fq.gz", ' \
                    u'"enid": "5c2f068029d292001e07c4f0"}, ' \
                    u'{"submit": true, "name": "test_account:/home/中文/test_2.fq.gz", ' \
                    u'"enid": "5c2f064c29d292002407ca34"}]}'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_listtasks():
    status = 200
    headers = {}
    response = requests.Response
    response.text = '{"task_list": {}}'
    response.content = '{"task_list": {}}'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_listjobs():
    status = 200
    headers = {}
    response = requests.Response
    response.text = '{"jobs": {}}'
    response.content = '{"jobs": {}}'
    return MockResponse_base(status, headers, response)


def makeResponse504():
    status = 504
    headers = {},
    response = requests.Response
    response.text = 'xxx'
    return MockResponse_base(status, headers, response)


@mock.patch('gdpy.Session.do_request')
class TestTask(GDTestCase):
    # test get task
    def test_get_task(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = task().get_task('5715ab2a5d02d91829f57fb9')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test list tasks
    def test_list_task(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_listtasks())
        result = task().list_tasks()
        self.assertEquals(result.status, 200)

    # test_list_tasks_fail
    def test_list_tasks_fail(self, do_request):
        with self.assertRaises(exceptions.ServerError):
            mock_response(do_request, makeResponse504())
            r = task().list_tasks()
            exceptions.make_exception(r)

    # test active workflow
    def test_active_workflow_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200_activatetask())
        result = task().active_workflow('unittests/resources/cutfasta_v1_parameters.yml', 'cutfasta', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.task_id, 'task_id')

        req_info = mock_response(do_request, makeResponse202_activatetask())
        result = task().active_workflow('unittests/resources/cutfasta_v1_parameters.yml', 'cutfasta', 1)
        self.assertEquals(result.status, 202)
        self.assertEquals(result.split, [])

    # invalid workflow name
    def test_active_workflow_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(ValueError) as cm:
            result = task().active_workflow('unittests/resources/cutfasta_v1_parameters.yml', 1, 1)
        self.assertEquals(str(cm.exception),
                          'Invalid workflow name! Expect a string started with alphabet and under 128 characters, but got 1!')

        # invalid workflow version
        with self.assertRaises(ValueError) as cm:
            result = task().active_workflow('unittests/resources/cutfasta_v1_parameters.yml', 'cutfasta', None)
        self.assertEquals(str(cm.exception), 'Invalid workflow version! Expect interger greater than 0, but got None')

    # test delete task
    def test_delete_task(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = task().delete_task('5715ab2a5d02d91829f57fb9')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test get jobs
    def test_get_jobs(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_listjobs())
        result = task().get_jobs('5715ab2a5d02d91829f57fb9')
        self.assertEquals(result.status, 200)

    # test get job cmd
    def test_get_job_cmd(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = task().get_job_cmd('5715ab2a5d02d91829f57fb9_5913d4cd53468000202426a5_Fastqc_node1')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test stop task
    def test_stop_task(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = task().stop_task('5715ab2a5d02d91829f57fb9')
        self.assertEquals(do_request.call_args[0][0].data, None)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test start task
    def test_restart_task(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(NotImplementedError):
            task().restart_task('5715ab2a5d02d91829f57fb9')
        result = wdl_task().restart_task('5715ab2a5d02d91829f57fb9')
        self.assertEquals(do_request.call_args[0][0].url,
                          "https://cn-beijing-api.genedock.com/accounts/res_account_name/projects/project_name/wdl/tasks/5715ab2a5d02d91829f57fb9/restart/")
        self.assertEquals(do_request.call_args[0][0].data, json.dumps({"debug_params": []}))
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')
        debug_params = [
            {
                "job_name": "job_name_1",
                "runtime": {
                    "cpu": "4c",
                    "memory": "2G",
                    "disk": "100G"
                },
                "command": "echo 1"
            },
            {
                "job_name": "job_name_2",
                "runtime": {
                    "cpu": "4c",
                    "memory": "1G",
                    "disk": "50G"
                }
            }
        ]
        result = wdl_task().restart_task('5715ab2a5d02d91829f57fb9', debug_params=debug_params)
        self.assertEquals(do_request.call_args[0][0].data, json.dumps({"debug_params": debug_params}))
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test get job info
    def test_get_job_info(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = task().get_job_info('5715ab2a5d02d91829f57fb9_5913d4cd53468000202426a5_Fastqc_node1')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')


if __name__ == '__main__':
    unittest.main()
