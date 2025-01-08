from django.db import models
import uuid

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AvailableTrigger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AvailableAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Zap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trigger_identifier = models.CharField(max_length=255)  # Renamed from trigger_id
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="zaps")

    def __str__(self):
        return str(self.id)


class Trigger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zap = models.OneToOneField(Zap, on_delete=models.CASCADE, related_name="zap_trigger")
    trigger_identifier = models.CharField(max_length=255)  # Renamed to avoid ambiguity
    metadata = models.JSONField(default=dict)
    type = models.ForeignKey(AvailableTrigger, on_delete=models.CASCADE, related_name="triggers")

    def __str__(self):
        return str(self.id)


class Action(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zap = models.ForeignKey(Zap, on_delete=models.CASCADE, related_name="actions")
    action_id = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    type = models.ForeignKey(AvailableAction, on_delete=models.CASCADE, related_name="actions")
    sorting_order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)




class ZapRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zap = models.ForeignKey(Zap, on_delete=models.CASCADE, related_name="zap_runs")
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return str(self.id)



class ZapRunOutbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zap_run = models.OneToOneField(ZapRun, on_delete=models.CASCADE, related_name="zap_run_outbox")

    def __str__(self):
        return str(self.id)
