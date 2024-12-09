from components.inventory import is_tools

class ItemInfo:
    """아이템 정보를 가지고, 계산한다"""
    def __init__(self, index, count, durability):
        self.index = index
        self.count = count
        self.durability = durability

    @property
    @staticmethod
    def null():
        return ItemInfo(
            None,
            0,
            None
        )

    def copy(self):
        return ItemInfo(
            self.index,
            self.count,
            self.durability
        )

    def create_item_low(self, index: int, count: int, durability:int|None=None):
        self.index = index
        self.count = count
        self.durability = durability

    def create_item(self, info: 'ItemInfo'):
        self.index = info.index
        self.count = info.count
        self.durability = info.durability

    def set_count(self, count):
        self.count = count

        if self.count == 0:
            self.clear()

    def add_item_low(self, value: int):
        if self.is_clean():
            raise ValueError("need index")
        self.set_count(self.count + value)
    
    def add_item(self, info: 'ItemInfo'):
        if self.index == None:
            self.create_item(info)
        else:
            if self.index != info.index:
                raise ValueError("index must be equal")
            self.add_item_low(info.count)

    def sub_item_low(self, value: int):
        if self.count >= value:
            self.set_count(self.count - value)            
        else:
            raise ValueError("over sub")

    def sub_item(self, info: 'ItemInfo'):
        if self.index != info.index:
            raise ValueError("index must equal")
        self.sub_item_low(info.count)

    def extract_item(self, value: int):
        try:
            index = self.index
            self.sub_item_low(value)
            return ItemInfo(
                index,
                value,
                is_tools.get(index, None)
            )
        except:
            raise ValueError("over extract")

    def is_zero(self):
        return self.count == 0

    def is_clean(self):
        return self.index == None and self.count == 0
            
    def clear(self):
        self.index = None
        self.count = 0
        self.durability = None

    def __str__(self):
        return f"index: {self.index}\ncount: {self.count}\ndurabillity: {self.durability}"