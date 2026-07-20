class ServiceExceptions(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)

class EmailRegistered(ServiceExceptions):
    def __init__(self):
        super().__init__(detail="Email already registered")

class InvalidCredentials(ServiceExceptions):
    def __init__(self):
        super().__init__(detail="Email inexistant ou mot de passe incorrect")


class TodoNotFound(ServiceExceptions):
    def __init__(self):
        super().__init__(detail="Todo not found")


class AccessUnauthorized(ServiceExceptions):
    def __init__(self):
        super().__init__(detail="Access unauthorized")