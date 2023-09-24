from django.db.models import Model

from typing import Optional, Dict


def get_instance(model: Model, **kwargs) -> Optional[Model]:
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def add_get_params(url: str, **params: Dict) -> str:
    url += "?"
    for key, value in params.items():
        url += f"{key}={value}&"
    return url[:-1]
