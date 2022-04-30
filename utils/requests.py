from pydantic import BaseModel


class BaseHeadmanRequest(BaseModel):
    stream_group: str
    day: str
    parity: str


class ChangeSchedule(BaseHeadmanRequest):
    pair_number: int
    changes: str


class ChangeScheduleHeadman(ChangeSchedule):
    ...


class ChangeSchedulePersonal(ChangeSchedule):
    id: int


class AddAnnotationHeadman(BaseHeadmanRequest):
    annotation: str


class AddAnnotationPersonal(BaseHeadmanRequest):
    id: int
    annotation: str


class RemovePairHeadman(BaseHeadmanRequest):
    pair_number: int


class RemovePairPersonal(BaseHeadmanRequest):
    id: int
    pair_number: int


class ResetScheduleHeadman(BaseHeadmanRequest):
    ...


class ResetSchedulePersonal(BaseHeadmanRequest):
    id: int


class RemoveAnnotationHeadman(BaseHeadmanRequest):
    ...


class RemoveAnnotationPersonal(BaseHeadmanRequest):
    id: int
