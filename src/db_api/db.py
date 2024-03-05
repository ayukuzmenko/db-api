from copy import deepcopy

from db_api.models.item import Item


class Database:
    def __init__(self) -> None:
        self.item_table: list[Item] = []
        self.transactions_stack: list[list[Item]] = []
        self._current_id: int = 0

    def _get_new_id(self) -> int:
        self._current_id += 1
        return self._current_id

    def _get_table(self) -> list[Item]:
        if self.transactions_stack:
            return self.transactions_stack[-1]
        return self.item_table

    async def check_transaction(self) -> bool:
        return len(self.transactions_stack) != 0

    async def get_all(self, is_dirty_read: bool = False) -> list[Item]:
        if is_dirty_read and self.transactions_stack:
            return self.transactions_stack[-1]
        return self.item_table

    async def create(self, value: str) -> Item:
        item = Item(id=self._get_new_id(), value=value)
        self._get_table().append(item)
        return item

    async def delete(self, item_id: int) -> Item | None:
        table = self._get_table()
        for i, item in enumerate(table):
            if item.id == item_id:
                return table.pop(i)
        return None

    async def begin(self) -> None:
        self.transactions_stack.append(deepcopy(self._get_table()))

    async def rollback(self) -> None:
        if self.transactions_stack:
            self.transactions_stack.pop()

    async def commit(self) -> None:
        new_state = self.transactions_stack.pop()
        if self.transactions_stack:
            self.transactions_stack.pop()
            self.transactions_stack.append(new_state)
        else:
            self.item_table = new_state
