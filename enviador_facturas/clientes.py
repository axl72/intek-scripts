class Cliente:
    def __init__(self, codigo, razon_social: str, email: str, dni=None, ruc=None) -> None:

        if razon_social == None or email == None or codigo == None:
            raise Exception("")
        if dni == None and ruc == None:
            raise Exception("")

        self.razon_social = razon_social
        self.email = email
        self.dni = dni
        self.ruc = ruc

    def get_id(self):
        return ("DNI", self.dni) if self.dni != None else ("RUC", self.ruc)
