import json
from datetime import datetime

import requests
from jproperties import Properties

from elma.exceptions import ElmaApiException
from elma.models.authorization import *
from elma.models.workflow import *

# BASE PATHS
API_PATH = "/API/REST"
AUTHORIZATION_PATH = API_PATH + "/Authorization"
WORKFLOW_PATH = API_PATH + "/Workflow"

# METHODS

# AUTHORIZATION
login_with_post_path = AUTHORIZATION_PATH + "/LoginWith?username={}"
login_with_basic = AUTHORIZATION_PATH + "/LoginWith?basic=1"
login_with_sspi_path = AUTHORIZATION_PATH + "/LoginWithSSPI"
api_version_path = AUTHORIZATION_PATH + "/ApiVersion"
version_path = AUTHORIZATION_PATH + "/Version"
check_permissions_path = AUTHORIZATION_PATH + "/CheckPermissions"
check_token_path = AUTHORIZATION_PATH + "/CheckToken?token={}"
server_time_path = AUTHORIZATION_PATH + "/ServerTime"
server_time_utc_path = AUTHORIZATION_PATH + "/ServerTimeUTC"
temporary_guid_path = AUTHORIZATION_PATH + "/TemporaryGuid"

# WORKFLOW
start_process_path = WORKFLOW_PATH + "/StartProcess"
startable_processes_path = WORKFLOW_PATH + "/StartableProcesses"
start_process_async_path = WORKFLOW_PATH + "/StartProcessAsync"
start_process_form_path = WORKFLOW_PATH + "/StartProcessForm"
execute_user_task_path = WORKFLOW_PATH + "/ExecuteUserTask"
execute_user_task_async_path = WORKFLOW_PATH + "/ExecuteUserTaskAsync"
execute_user_task_status_path = WORKFLOW_PATH + "/ExecuteUserTaskStatus"
has_dynamic_form_path = WORKFLOW_PATH + "/HasDynamicForm"
has_dynamic_forms_path = WORKFLOW_PATH + "/HasDynamicForms"
tasks_info_path = WORKFLOW_PATH + "/TasksInfo"
task_standard_output_flows_path = WORKFLOW_PATH + "/TaskStandardOutputFlows"

# WORKFLOW_INSTANCE_SERVICE
map_path = "/PublicAPI/REST/EleWise.ELMA.Workflow/WorkflowInstance/Map?id={}"

# HEADERS
CONTENT_TYPE_HEADER = "Content-Type"
APPLICATION_JSON = "application/json; charset=utf-8"


class ElmaApiWebClient:
    __AuthTokenMaxMinutesAlive = 15
    __UserLogin: str
    __UserPassword: str
    __AuthToken: str
    __AuthTokenLiveTimestamp: float
    __SessionToken: str
    __AppToken: str
    authorization: 'Authorization'
    workflow: 'Workflow'
    workflow_instance_service: 'WorkflowInstanceService'

    def __init__(self, host_name: str = "http://localhost", port: int = 8080, debug_mode=False) -> None:
        super().__init__()
        self.host_name = host_name
        self.port = port
        self.debug_mode = debug_mode
        self.authorization = self.init_authorization()
        self.workflow = self.init_workflow()
        self.workflow_instance_service = self.init_workflow_instance_service()

    def init_authorization(self):
        return ElmaApiWebClient.Authorization(self)

    def init_workflow(self):
        return ElmaApiWebClient.Workflow(self)

    def init_workflow_instance_service(self):
        return ElmaApiWebClient.WorkflowInstanceService(self)

    # Создание инстанса веб-клиента с автоматической авторизацией запросов
    @staticmethod
    def init_with_auth(host_name: str, port: int, debug_mode=False,
                       user_login: str = None, user_password: str = None, app_token: str = None):
        instance = ElmaApiWebClient(host_name=host_name, port=port, debug_mode=debug_mode)
        auth_result = instance.authorization.login_with_user_name(user_login=user_login,
                                                                  user_password=user_password,
                                                                  app_token=app_token)
        instance.set_auth_token(auth_result.AuthToken)
        instance.set_session_token(auth_result.SessionToken)
        instance.set_app_token(app_token)
        instance.__UserLogin = user_login
        instance.__UserPassword = user_password
        return instance

    # Создание инстанса веб-клиента с автоматической авторизацией запросов через конфигурационный файл .properties
    # *заполнять только один из аргументов*
    @staticmethod
    def init_with_auth_from_properties(config_file_path: str, properties: dict = None):
        if properties is None:
            properties = {}
            configs = Properties()
            with open(config_file_path, 'rb') as config_file:
                configs.load(config_file)
                for prop in configs.items():
                    properties[prop[0]] = prop[1].data

        debug_mode: bool = properties.get("debug_mode", False) == "true"
        return ElmaApiWebClient.init_with_auth(
            host_name=properties["host"],
            port=properties["port"],
            debug_mode=debug_mode,
            user_login=properties["user_login"],
            user_password=properties["user_password"],
            app_token=properties["application_token"]
        )

    def set_auth_token_live_timestamp(self, timestamp):
        self.__AuthTokenLiveTimestamp = timestamp

    def get_auth_token_live_timestamp(self):
        return self.__AuthTokenLiveTimestamp

    def get_auth_token_max_minutes_alive(self):
        return self.__AuthTokenMaxMinutesAlive

    def get_auth_token(self):
        return self.__AuthToken

    def get_session_token(self):
        return self.__SessionToken

    def get_app_token(self):
        return self.__AppToken

    def get_user_login(self):
        return self.__UserLogin

    def set_auth_token(self, auth_token):
        self.__AuthToken = auth_token

    def set_session_token(self, session_token):
        self.__SessionToken = session_token

    def set_app_token(self, app_token):
        self.__AppToken = app_token

    def set_debug_mode(self, mode: bool):
        self.debug_mode = mode

    # Получить токен из кэша. Если токен уже просрочен, то получить новый и закэшировать
    def get_cached_auth_token(self):
        date_now = datetime.now()
        date_of_token_creation = datetime.fromtimestamp(self.get_auth_token_live_timestamp())
        tdelta = date_now - date_of_token_creation
        max_minutes_alive = (self.__AuthTokenMaxMinutesAlive - 1) * 60
        if tdelta.seconds >= max_minutes_alive:
            auth_result = self.authorization.login_with_user_name(user_login=self.__UserLogin,
                                                                  user_password=self.__UserPassword,
                                                                  app_token=self.__AppToken)
            self.__AuthToken = auth_result.AuthToken
        return self.__AuthToken

    # базовый запрос в elma
    def base_request(self, path="", headers=None, body=None, request_func=lambda u, h, b: requests.post(u, h, b)):
        if headers is None:
            headers = {}
        if body is None:
            body = {}
        headers[CONTENT_TYPE_HEADER] = APPLICATION_JSON
        url = f"{self.host_name}:{self.port}{path}"
        if self.debug_mode:
            print("\n")
            print(f"request url: {url}")
            print(f"request headers: {headers}")
            print(f"request body: {body}")
        r = request_func(url, headers, body)
        if self.debug_mode:
            print(f"response code: {r.status_code}")
            print(f"response status: {r.reason}")
            print(f"response body: {r.text}")
        if len(r.text) == 0 or r.status_code > 300:
            raise ElmaApiException(f"code: {r.status_code}; status: {r.reason}; content: {r.text}")
        return json.loads(r.text)

    def authorized_request(self, path: str = None, headers=None, body=None,
                           auth_token=None, session_token=None,
                           request_func=lambda u, h, b: requests.post(u, h, b)):
        if headers is None:
            headers = {}
        cached_auth_token = self.get_cached_auth_token()
        if auth_token is None and cached_auth_token is not None:
            auth_token = cached_auth_token
        if auth_token is not None:
            self.__AuthToken = auth_token
        else:
            raise ElmaApiException("auth_token is missing")

        if session_token is None and self.__SessionToken is not None:
            session_token = self.__SessionToken
        elif session_token is not None:
            self.__SessionToken = session_token

        headers["AuthToken"] = auth_token
        if session_token is not None:
            headers["SessionToken"] = session_token
        return self.base_request(path, headers, body, request_func)

        # POST-запрос в elma

    def base_post_request(self, path: str = "", headers=None, body=None):
        return self.base_request(path, headers, body,
                                 lambda u, h, b: requests.post(url=u, headers=h, data=b))

    # GET-запрос в elma
    def base_get_request(self, path: str = "", headers=None):
        return self.base_request(path, headers, {},
                                 lambda u, h, b: requests.get(url=u, headers=h))

    # POST-запрос в elma с авторизацией
    def authorized_post_request(self, path: str = None, headers=None, body=None,
                                auth_token=None, session_token=None):
        return self.authorized_request(path, headers, body,
                                       auth_token, session_token,
                                       lambda u, h, b: requests.post(url=u, headers=h, data=b))

    # GET-запрос в elma с авторизацией
    def authorized_get_request(self, path: str = None, headers=None,
                               auth_token=None, session_token=None):
        return self.authorized_request(path, headers, {},
                                       auth_token, session_token,
                                       lambda u, h, b: requests.get(url=u, headers=h))

    # API Methods:

    class ApiModule:
        def __init__(self, elma: 'ElmaApiWebClient') -> None:
            super().__init__()
            self.elma_client = elma

    class Authorization(ApiModule):

        # метод авторизации
        def login_with_user_name(self, user_login: str = None, user_password: str = None,
                                 app_token: str = None) -> AuthResponse:
            path = login_with_post_path.format(user_login)
            headers = {
                "ApplicationToken": app_token
            }
            if self.__dict__.keys().__contains__("__SessionToken") and self.elma_client.get_session_token() is not None:
                headers["SessionToken"] = self.elma_client.get_session_token()
            body = f'"{user_password}"'
            json_dict = self.elma_client.base_post_request(path=path, headers=headers, body=body)
            self.elma_client.set_auth_token_live_timestamp(datetime.timestamp(datetime.now()))
            return AuthResponse.from_json(json_dict)

        def login_with_basic(self) -> AuthResponse:
            return AuthResponse.from_json(self.elma_client.base_get_request(path=login_with_basic))

        def login_with_sspi(self) -> AuthResponse:
            return AuthResponse.from_json(self.elma_client.base_get_request(path=login_with_sspi_path))

        def api_version(self) -> ApiVersionResponse:
            return ApiVersionResponse.from_json(self.elma_client.base_get_request(path=api_version_path))

        def version(self) -> str:
            return self.elma_client.base_get_request(path=version_path)

        def check_permissions(self, check_permissions_rq: list,
                              auth_token: str = None, session_token: str = None):
            json_body = []
            for cp in check_permissions_rq:
                if isinstance(cp, CheckPermissionsRequest.CheckPermission):
                    json_body.append(cp.to_json())
                else:
                    json_body.append(cp)
            return self.elma_client.authorized_post_request(path=check_permissions_path,
                                                            body=json.dumps(json_body),
                                                            auth_token=auth_token, session_token=session_token)

        def check_token(self, token) -> AuthResponse:
            return AuthResponse.from_json(self.elma_client.base_get_request(path=check_token_path.format(token)))

        def server_time(self, auth_token: str = None, session_token: str = None) -> str:
            return self.elma_client.authorized_get_request(path=server_time_path,
                                                           auth_token=auth_token, session_token=session_token)

        def server_time_utc(self, auth_token: str = None, session_token: str = None) -> str:
            return self.elma_client.authorized_get_request(path=server_time_utc_path,
                                                           auth_token=auth_token, session_token=session_token)

        def temporary_guid(self, auth_token: str = None, session_token: str = None) -> str:
            return self.elma_client.authorized_get_request(path=temporary_guid_path,
                                                           auth_token=auth_token, session_token=session_token)

    class Workflow(ApiModule):
        def __workflow_post_request(self, path: str, rsp_cls, rq: DataSerializable = None,
                                    auth_token: str = None, session_token: str = None):
            body = None
            if rq is not None:
                body = str(rq.to_Data())
            json_result = self.elma_client.authorized_post_request(path=path, headers={}, body=body,
                                                                   auth_token=auth_token, session_token=session_token)
            data = Data.from_json(json_result)
            dtobj = data.to_obj()
            return rsp_cls(**dtobj)

        # метод запуска процесса
        def start_process(self, start_process_rq: StartProcessRq = None,
                          context_vars: Data = Data(), process_name=None,
                          process_token: str = None, process_header_id: int = None,
                          auth_token: str = None, session_token: str = None) -> StartProcessRs:
            if start_process_rq is None:
                start_process_rq = StartProcessRq(context_vars, process_name, process_token, process_header_id)
            return self.__workflow_post_request(path=start_process_path, rq=start_process_rq, rsp_cls=StartProcessRs,
                                                auth_token=auth_token, session_token=session_token)

        # получить все запущенные процессы
        def get_startable_processes(self, auth_token: str = None, session_token: str = None) -> StartableProcessesRs:
            return self.__workflow_post_request(path=startable_processes_path, rsp_cls=StartableProcessesRs,
                                                auth_token=auth_token, session_token=session_token)

        def start_process_async(self, start_process_async_rq: StartProcessAsyncRq = None,
                                context_vars: Data = Data(),
                                process_name=None, process_token: str = None, process_header_id: int = None,
                                auth_token: str = None, session_token: str = None) -> StartProcessAsyncRs:

            if start_process_async_rq is None:
                start_process_async_rq = StartProcessAsyncRq(context_vars, process_name, process_token,
                                                             process_header_id)
            return self.__workflow_post_request(path=start_process_async_path, rq=start_process_async_rq,
                                                rsp_cls=StartProcessAsyncRs,
                                                auth_token=auth_token, session_token=session_token)

        def start_process_form(self, start_process_from_rq: StartProcessFormRq = None,
                               process_header_id: int = None,
                               auth_token: str = None, session_token: str = None) -> StartProcessFormRs:
            if start_process_from_rq is None:
                start_process_from_rq = StartProcessFormRq(process_header_id)
            return self.__workflow_post_request(path=start_process_form_path, rq=start_process_from_rq,
                                                rsp_cls=StartProcessFormRs,
                                                auth_token=auth_token, session_token=session_token)

        def execute_user_task(self, execute_user_task_rq: ExecuteUserTaskRq = None,
                              _id=None, context=None, selected_connector_uid=None,
                              auth_token: str = None, session_token: str = None) -> ExecuteUserTaskRs:
            if execute_user_task_rq is None:
                execute_user_task_rq = ExecuteUserTaskRq(_id, context, selected_connector_uid)
            return self.__workflow_post_request(path=execute_user_task_path, rq=execute_user_task_rq,
                                                rsp_cls=ExecuteUserTaskRs,
                                                auth_token=auth_token, session_token=session_token)

        def execute_user_task_async(self, execute_user_task_async_rq: ExecuteUserTaskAsyncRq = None,
                                    _id=None, context=None, selected_connector_uid=None,
                                    auth_token: str = None, session_token: str = None) -> ExecuteUserTaskAsyncRs:

            if execute_user_task_async_rq is None:
                execute_user_task_async_rq = ExecuteUserTaskAsyncRq(_id, context, selected_connector_uid)
            return self.__workflow_post_request(path=execute_user_task_async_path, rq=execute_user_task_async_rq,
                                                rsp_cls=ExecuteUserTaskAsyncRs,
                                                auth_token=auth_token, session_token=session_token)

        def execute_user_task_status(self, execute_user_task_status_rq: ExecuteUserTaskStatusRq = None,
                                     execution_token=None,
                                     auth_token: str = None, session_token: str = None) -> ExecuteUserTaskStatusRs:
            if execute_user_task_status_rq is None:
                execute_user_task_status_rq = ExecuteUserTaskStatusRq(execution_token)
            return self.__workflow_post_request(path=execute_user_task_status_path, rq=execute_user_task_status_rq,
                                                rsp_cls=ExecuteUserTaskStatusRs,
                                                auth_token=auth_token, session_token=session_token)

        def has_dynamic_form(self, has_dynamic_form_rq: HasDynamicFormRq = None,
                             task_id=None,
                             auth_token: str = None, session_token: str = None) -> HasDynamicFormRs:
            if has_dynamic_form_rq is None:
                has_dynamic_form_rq = HasDynamicFormRq(task_id)
            return self.__workflow_post_request(path=has_dynamic_form_path, rq=has_dynamic_form_rq,
                                                rsp_cls=HasDynamicFormRs,
                                                auth_token=auth_token, session_token=session_token)

        def has_dynamic_forms(self, has_dynamic_forms_rq: HasDynamicFormsRq = None,
                              task_ids=None,
                              auth_token: str = None, session_token: str = None) -> HasDynamicFormsRs:
            if task_ids is None:
                task_ids = []
            if has_dynamic_forms_rq is None:
                has_dynamic_forms_rq = HasDynamicFormsRq(task_ids)
            return self.__workflow_post_request(path=has_dynamic_forms_path, rq=has_dynamic_forms_rq,
                                                rsp_cls=HasDynamicFormsRs,
                                                auth_token=auth_token, session_token=session_token)

        def tasks_info(self, task_info_rq: TasksInfoRq = None,
                       ids=None,
                       auth_token: str = None, session_token: str = None) -> TasksInfoRs:
            if ids is None:
                ids = []
            if task_info_rq is None:
                task_info_rq = TasksInfoRq(ids)
            return self.__workflow_post_request(path=tasks_info_path, rq=task_info_rq,
                                                rsp_cls=TasksInfoRs,
                                                auth_token=auth_token, session_token=session_token)

        def task_standard_output_flows(self, task_standard_output_flows_rq: TaskStandardOutputFlowsRq = None,
                                       task_id=None,
                                       auth_token: str = None, session_token: str = None) -> TaskStandardOutputFlowsRs:
            if task_standard_output_flows_rq is None:
                task_standard_output_flows_rq = TaskStandardOutputFlowsRq(task_id)
            return self.__workflow_post_request(path=task_standard_output_flows_path, rq=task_standard_output_flows_rq,
                                                rsp_cls=TaskStandardOutputFlowsRs,
                                                auth_token=auth_token, session_token=session_token)

    class WorkflowInstanceService(ApiModule):
        def get_map(self, process_id: str, auth_token: str = None, session_token: str = None) -> str:
            url = f"{self.elma_client.host_name}:{self.elma_client.port}"
            path = self.elma_client.authorized_get_request(path=map_path.format(process_id),
                                                           auth_token=auth_token, session_token=session_token)
            return url + path
