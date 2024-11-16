from pydantic import BaseModel


class Website(BaseModel):
    name: str
    url: str
    description: str = ''
    keywords: str = ''
    icon: str = ''
    site_type: int = 0
    overdue: int = 0
    is_delete: int = 0


class User(BaseModel):
    name: str
    phone: str
    password: str
    logo_url: str = ''
