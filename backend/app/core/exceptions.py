class CompanyNameAlreadyExistsException(Exception):
    def __init__(self, company_name: str):
        self.company_name = company_name


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email '{email}' already exists.")


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Invalid email or password.")
