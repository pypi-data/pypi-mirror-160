from dataclasses import dataclass

from elma.models.data import Data
from elma.models.util import DataSerializable, init_list, init_class, init_data


# StartProcess
@dataclass
class StartProcessRq(DataSerializable):
    Context: Data = None
    ProcessName: str = None
    ProcessToken: str = None
    ProcessHeaderId: int = None


@dataclass
class StartProcessRs(DataSerializable):
    @dataclass
    class CurrentOperationCls(DataSerializable):
        QueueElementName: str = None
        ExecutionStart: str = None
        NextExecuteDate: str = None

    Result: bool = None
    NextTaskId: int = None
    CurrentOperations: list = None

    def __post_init__(self):
        self.CurrentOperations = init_list(self.CurrentOperations, StartProcessRs.CurrentOperationCls)


# StartProcessAsync
@dataclass
class StartProcessAsyncRq(DataSerializable):
    Context: Data = None
    ProcessName: str = None
    ProcessToken: str = None
    ProcessHeaderId: int = None


@dataclass
class StartProcessAsyncRs(DataSerializable):
    @dataclass
    class CurrentOperationCls(DataSerializable):
        QueueElementName: str = None
        ExecutionStart: str = None
        NextExecuteDate: str = None

    Result: bool = None
    NextTaskId: int = None
    Status: str = None
    ExecutionToken: str = None
    CurrentOperations: list = None

    def __post_init__(self):
        self.CurrentOperations = init_list(self.CurrentOperations, StartProcessAsyncRs.CurrentOperationCls)


# StartProcessFrom
@dataclass
class StartProcessFormRq(DataSerializable):
    ProcessHeaderId: int = None


@dataclass
class StartProcessFormRs(DataSerializable):
    @dataclass
    class FormCls(DataSerializable):
        @dataclass
        class ItemCls(DataSerializable):
            Name: str = None
            DisplayName: str = None
            Description: str = None
            TypeUid: int = None
            SubTypeUid: int = None
            Required: bool = None
            ReadOnly: bool = None
            Visible: bool = None
            CustomView: bool = None
            FilterProviderUid: int = None
            FilterProviderData: str = None
            Items: list = None
            Settings: Data = None

            def __post_init__(self):
                self.Items = init_list(self.Items, TasksInfoRs.ItemCls.FormCls.ItemCls)

        Items: list = None

        def __post_init__(self):
            self.Items = init_list(self.Items, TasksInfoRs.ItemCls.FormCls.ItemCls)

    AskNameOnStart: bool = None
    Form: FormCls = None
    Context: Data = None

    def __post_init__(self):
        self.Form = init_class(self.Form, StartProcessFormRs.FormCls)


@dataclass
class StartableProcessesRs(DataSerializable):
    @dataclass
    class Group(DataSerializable):
        Id: int = None
        Name: str = None
        ParentId: int = None

    @dataclass
    class Process(DataSerializable):
        Id: int = None
        Name: str = None
        GroupId: int = None

    Groups: list = None
    Processes: list = None

    def __post_init__(self):
        self.Groups = init_list(self.Groups, StartableProcessesRs.Group)
        self.Processes = init_list(self.Processes, StartableProcessesRs.Process)


# ExecuteUserTask
@dataclass
class ExecuteUserTaskRq(DataSerializable):
    Id: int = None
    Context: Data = None
    SelectedConnectorUid: str = None


@dataclass
class ExecuteUserTaskRs(DataSerializable):
    @dataclass
    class CurrentOperationCls(DataSerializable):
        QueueElementName: str = None
        ExecutionStart: str = None
        NextExecuteDate: str = None

    Result: bool = None
    NextTaskId: int = None
    InstanceStatus: str = None
    EndTaskMessage: str = None
    CurrentOperations: list = None
    Information: Data = None

    def __post_init__(self):
        self.CurrentOperations = init_list(self.CurrentOperations, ExecuteUserTaskRs.CurrentOperationCls)


# ExecuteUserTaskAsync
@dataclass
class ExecuteUserTaskAsyncRq(DataSerializable):
    Id: int = None
    Context: Data = None
    SelectedConnectorUid: str = None


@dataclass
class ExecuteUserTaskAsyncRs(DataSerializable):
    @dataclass
    class CurrentOperationCls(DataSerializable):
        QueueElementName: str = None
        ExecutionStart: str = None
        NextExecuteDate: str = None

    Result: bool
    Status: str
    Error: str
    ExecutionToken: str
    NextTaskId: int
    InstanceStatus: str
    EndTaskMessage: str
    CurrentOperations: list = None
    Information: Data = None

    def __post_init__(self):
        self.CurrentOperations = init_list(self.CurrentOperations, ExecuteUserTaskRs.CurrentOperationCls)


# ExecuteUserTaskStatus
@dataclass
class ExecuteUserTaskStatusRq(DataSerializable):
    ExecutionToken: str = None


@dataclass
class ExecuteUserTaskStatusRs(DataSerializable):
    ExecutionToken: str = None


# HasDynamicForm
@dataclass
class HasDynamicFormRq(DataSerializable):
    TaskId: int = None


@dataclass
class HasDynamicFormRs(DataSerializable):
    Result: bool = None


# HasDynamicForms
@dataclass
class HasDynamicFormsRq(DataSerializable):
    TaskIds: list = None


@dataclass
class HasDynamicFormsRs(DataSerializable):
    Result: list = None


# TaskStandardOutputFlows
@dataclass
class TaskStandardOutputFlowsRq(DataSerializable):
    TaskId: int = None


@dataclass
class TaskStandardOutputFlowsRs(DataSerializable):
    @dataclass
    class FlowCls(DataSerializable):
        Uid: int = None
        Status: str = None
        Name: str = None

    Result: bool = None
    Flows: list = None

    def __post_init__(self):
        self.Flows = init_list(self.Flows, TaskStandardOutputFlowsRs.FlowCls)


# TasksInfo
@dataclass
class TasksInfoRq(DataSerializable):
    Ids: list = None

    def __init__(self, ids: []) -> None:
        ids_objs: list = []
        for int_id in ids:
            ids_objs.append(TasksInfoRq.Id(int_id))
        self.Ids = ids_objs
        super().__init__()

    @dataclass
    class Id(DataSerializable):
        Id: int = None


@dataclass
class TasksInfoRs(DataSerializable):
    Items: list = None

    @dataclass
    class ItemCls(DataSerializable):
        @dataclass
        class FormCls(DataSerializable):
            @dataclass
            class ItemCls(DataSerializable):
                Name: str = None
                DisplayName: str = None
                Description: str = None
                TypeUid: int = None
                SubTypeUid: int = None
                Required: bool = None
                ReadOnly: bool = None
                Visible: bool = None
                CustomView: bool = None
                FilterProviderUid: int = None
                FilterProviderData: str = None
                Items: list = None
                Settings: Data = None

                def __post_init__(self):
                    self.Items = init_list(self.Items, TasksInfoRs.ItemCls.FormCls.ItemCls)

            Items: list = None

            def __post_init__(self):
                self.Items = init_list(self.Items, TasksInfoRs.ItemCls.FormCls.ItemCls)

        @dataclass
        class ProcessInfoCls(DataSerializable):
            ProcessName: str = None
            ProcessVersionNumber: int = None
            InstanceName: str = None
            InstanceId: int = None
            StartDate: str = None
            Initiator: int = None
            Responsible: int = None

        @dataclass
        class FlowCls(DataSerializable):
            Uid: int = None
            Name: str = None
            Description: str = None
            Status: str = None
            Color: str = None
            OutputCancel: bool = None
            ValidateContextVariables: bool = None
            UseConfirmConnector: bool = None
            ConfirmConnectorText: str = None
            EnableComment: bool = None
            SignType: str = None

        Id: int = None
        TypeUid: int = None
        IsAvailable: bool = None
        TaskDescription: str = None
        DenyReassign: bool = None
        Flows: list = None
        ProcessInfo: ProcessInfoCls = None
        DocumentHelp: Data = None
        Context: str = None
        Form: FormCls = None

        def __post_init__(self):
            self.Flows = init_list(self.Flows, TasksInfoRs.ItemCls.FlowCls)
            self.Form = init_class(self.Form, TasksInfoRs.ItemCls.FormCls)
            self.ProcessInfo = init_class(self.ProcessInfo, TasksInfoRs.ItemCls.ProcessInfoCls)
            self.DocumentHelp = init_data(self.DocumentHelp)

    def __post_init__(self):
        self.Items = init_list(self.Items, TasksInfoRs.ItemCls)
