from typing import List, Literal, Optional

from pydantic import BaseModel

DetectionSensitivity = Literal['high', 'low']


class IInfoTypeMeta(BaseModel):
    domains: Optional[List[str]] = None


class IInfoType(BaseModel):
    name: str
    meta: Optional[IInfoTypeMeta] = None


class IScanForLongTexts(BaseModel):
    columnNumbers: Optional[List[int]] = None
    columnNames: Optional[List[str]] = None


class IGetInfoTypeRequestParameters(BaseModel):
    type: Literal['allGeneric', 'allCountry', 'all']


class IRequestParameters(BaseModel):
    snapshot: Optional[bool] = None
    detailed: Optional[bool] = None
    detectionSensitivity: Optional[DetectionSensitivity] = None
    getConfidenceDetailed: Optional[bool] = None
    predictNullColumns: Optional[bool] = None
    allExcept: Optional[str] = None  ## json string (legacy)
    scanRegexOnly: Optional[bool] = None
    scanWithoutRegexBoundaries: Optional[bool] = None
    showNeighbourMatch: Optional[bool] = None
    showNeighbourhood: Optional[int] = None
    maskDetails: Optional[bool] = None
    sample: Optional[bool] = None
    sampleSize: Optional[str] = None
    interruptIfTooLong: Optional[bool] = None
    interruptTimeBudgetPerMB: Optional[int] = None


class INonCountrySpecificConfig(BaseModel):
    toScan: bool
    nonCountrySpecificExcept: Optional[List[str]] = None  # which generic infotypes to not include
    countrySpecificInclude: Optional[List[str]] = None  # which country-specific infotypes to include


suffixForConfidenceType = Literal['defaultsOnly', 'all', 'none']


class IConfidenceThresholdForSomeParams(BaseModel):
    confidenceThreshold: int
    infoTypes: List[str]


class IConfidenceConfig(BaseModel):
    useDefaultPossibles: bool
    confidenceThreshold: Optional[int] = None  # replaces the default confidence threshold
    confidenceThresholdForSomeInfoTypes: Optional[IConfidenceThresholdForSomeParams] = None
    suffixForConfidence: Optional[suffixForConfidenceType] = None


class IInspectionConfig(BaseModel):
    infoTypes: List[IInfoType]
    neighbourRequirePII: Optional[List[str]] = None
    infoTypesWithoutMasking: Optional[List[str]] = None
    confidenceConfig: Optional[IConfidenceConfig] = None
    allNonCountrySpecific: Optional[INonCountrySpecificConfig] = None
    allExcept: Optional[List[str]] = None
    exclusions: Optional[List[str]] = None
    scanForLongTexts: Optional[IScanForLongTexts] = None


class IExclusionConfigKeyedByInfotype(BaseModel):
    infoType: List[str]


class mimeDict(BaseModel):
    headers: Optional[str] = None
    delimiter: Optional[str] = None
    quoteChar: Optional[str] = None
    excludeColumns: Optional[List[int]] = None


class IMeta(BaseModel):
    mimetype: Optional[str] = None
    mimetypeMeta: Optional[mimeDict] = None
    fileName: Optional[str] = None
    entityName: Optional[str] = None
