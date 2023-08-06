from tonclient.types import ParamsOfParse, ParamsOfQueryCollection, ResultOfQueryCollection

from tvmbase.client import Client
from tvmbase.models.data import AccountData
from tvmbase.models.tvm.base import BaseTvm


class Account(BaseTvm):
    DATA_TYPE: type = AccountData

    def __init__(self, address: str, data: AccountData | None, exists: bool = True):
        super().__init__(address)
        self.data = data
        self.exists = exists

    @staticmethod
    def gql_query(address: str) -> ParamsOfQueryCollection:
        return ParamsOfQueryCollection(
            collection='accounts',
            result='boc',
            limit=1,
            filter={'id': {'eq': address}},
        )

    @classmethod
    async def from_query_result(cls, client: Client, idx: str, result: ResultOfQueryCollection) -> 'Account':
        try:
            boc = result.result[0]['boc']
        except IndexError:
            boc = ...  # None is returned for Deleted accounts (acc_type=3, acc_type_name=NonExist)
        return await cls.from_boc(client, boc, idx=idx)

    @classmethod
    async def from_boc(cls, client: Client, boc: str, **kwargs) -> 'Account':
        kw_address = kwargs.pop('idx', None)
        if boc is ...:  # account never existed
            assert kw_address is not None, 'Account must have boc or address'
            return cls(kw_address, data=None, exists=False)
        if boc is None:  # account is deleted
            assert kw_address is not None, 'Account must have boc or address'
            return cls(kw_address, data=None, exists=True)
        parse_params = ParamsOfParse(boc=boc)
        parsed = await client.boc.parse_account(params=parse_params)
        address = parsed.parsed['id']
        data = AccountData(**parsed.parsed, **kwargs)
        return cls(address, data)

    @classmethod
    async def from_address(cls, client: Client, address: str) -> 'Account':
        return await cls.from_idx(client, address)

    @property
    def address(self) -> str:
        return self.idx

    @property
    def balance(self) -> int:
        return self.data.balance
