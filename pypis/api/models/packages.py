from typing import List, Optional

from pydantic import BaseConfig, BaseModel


class PackageCreate(BaseModel):
    name: str
    classifiers: List[str]

    author: str
    author_email: str

    description: str
    description_content_type: Optional[str]

    home_page: str
    license: str
    package_url: str
    project_url: str
    summary: str
    version: str

    class Config(BaseConfig):
        allow_population_by_field_name = True
        orm_mode = True
