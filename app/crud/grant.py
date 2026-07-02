from app.crud.base import CRUDBase
from app.models.grant import Grant
from app.schema.grant import GrantCreate, GrantUpdate


class CRUDGrant(
    CRUDBase[
        Grant,
        GrantCreate,
        GrantUpdate,
    ]
):
    pass


grant_crud = CRUDGrant(Grant)