import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# ezafe kardan fild hay mored niaz be modele user
class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True ,default = uuid.uuid4,)
    nid = models.CharField(max_length=11, null=False)