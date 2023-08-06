from pydantic.dataclasses import dataclass

from common_inspection_py.types.tasks import TaskType, TaskConfigs
from common_inspection_py.config.datamodels import ScanTaskBaseConfig, ScanTaskRuntimeConfig, ScanTaskMetaData
from common_inspection_py.interfaces.datarequests import ScanTaskData
from typing import Dict, Any, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod


class ReadTaskConfigData(BaseModel):
    data: Optional[Dict] = None


@dataclass
class Task(ABC):
    taskType: TaskType
    taskConfig: TaskConfigs
    ScanTaskBaseConfig: Optional[Any] = None

    @abstractmethod
    def readTaskStaticConfigData(self) -> ReadTaskConfigData:
        raise NotImplementedError


@dataclass
class TaskRunTime(ABC):
    task: Task

    @abstractmethod
    def readTaskStaticConfigData(self, dataReadTaskConfig: Any) -> ReadTaskConfigData:
        raise NotImplementedError

    @abstractmethod
    def readTaskData(self, dataReadTask: Any) -> ScanTaskData:
        raise NotImplementedError

    @abstractmethod
    def writeTaskData(self, dataWriteTask: Any) -> ScanTaskData:
        raise NotImplementedError

    @abstractmethod
    def runTask(self, dataTask: Any) -> ScanTaskMetaData:
        raise NotImplementedError
