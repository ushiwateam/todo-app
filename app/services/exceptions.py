class ServiceExceptions(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class EmailRegistered(ServiceExceptions):
    def __init__(self):
        super().__init__(detail="Email already registered")

class UnauthorizedUser(ServiceExceptions):
    def __init__(self):
        super().__init__(detail="Email inexistant ou mot de passe incorrect")

