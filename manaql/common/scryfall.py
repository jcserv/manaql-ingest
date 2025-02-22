from enum import Enum


class AllowedLayout(str, Enum):
    Normal = "normal"
    ModalDFC = "modal_dfc"
    Saga = "saga"
    Split = "split"
    Transform = "transform"
