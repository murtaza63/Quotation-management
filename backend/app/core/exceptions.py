class CompanyNameAlreadyExistsException(Exception):
    def __init__(self, company_name: str):
        self.company_name = company_name
