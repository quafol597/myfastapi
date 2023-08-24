from pydantic import BaseModel
from pydantic import BaseConfig


class ProjectConfig(BaseConfig):
    db_url: str = None
    pass



project_config = ProjectConfig()