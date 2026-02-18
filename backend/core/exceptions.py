class RetailException(Exception):
    """Base exception for Retail DSS"""
    pass

class ResourceNotFoundException(RetailException):
    def __init__(self, resource: str, id: str = None):
        self.resource = resource
        self.id = id
        self.message = f"{resource} not found"
        if id:
            self.message += f": {id}"
        super().__init__(self.message)

class BusinessRuleException(RetailException):
    def __init__(self, detail: str):
        self.message = detail
        super().__init__(self.message)
