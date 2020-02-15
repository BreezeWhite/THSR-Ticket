class ConfirmTicketInfo:
    def __init__(self) -> None:
        pass

    def personal_id_info(self, default_value: str = None, select: bool = True) -> str:
        return input("輸入身分證字號(預設: {}): ".format(default_value)) or default_value

    def phone_info(self, default_value: str = "", select: bool = True) -> str:
        return input("輸入手機號碼(預設: {}): ".format(default_value)) or default_value
