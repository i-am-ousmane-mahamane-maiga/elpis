from tortoise import fields
from tortoise.models import Model

class Peer(Model):
    id = fields.IntField(pk=True)
    peer_id = fields.CharField(max_length=64, unique=True)
    secret_hash = fields.CharField(max_length=64)
    port = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
