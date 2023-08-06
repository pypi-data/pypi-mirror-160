from typing import Dict, Any, Optional, List
from pydantic import validate_arguments, BaseModel
from pydantic.dataclasses import dataclass
from common_inspection_py.interfaces.requests import IInspectionConfig, IRequestParameters


class ScanTaskBaseConfig(BaseModel):
    taskConfiguration: Optional[Any] = None
    taskIOConfiguration: Optional[Any] = None


class ScanTaskRuntimeConfig(BaseModel):
    runTaskID: str
    runTaskTracker: Dict
    runTaskDetails: Dict


class Data(BaseModel):
    file: str
    basic: Optional[List[str]]
    advanced: Optional[List[str]]


class Resp_Data(BaseModel):
    snapshot: Optional[str]
    detailed: Optional[str]
    error: Optional[str]


class Response(BaseModel):
    data: Optional[Resp_Data] = None
    success: bool


class ScanTaskReqDet(BaseModel):
    inspectionConfig: IInspectionConfig
    data: Data
    query: IRequestParameters
    response: Response


class ScanTaskMetaData(BaseModel):
    scanTaskID: str
    scanTaskRequestDetails: ScanTaskReqDet
