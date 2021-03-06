from django.db import models, transaction
from copy import copy
from datetime import datetime

# Create your models here.

class TemporalManager(models.Manager):
    use_for_related_fields = True

    def current(self):
        return self.get_queryset().filter(sys_end_date=datetime.max)

    def as_of(self, time):
        return self.get_queryset().filter(sys_start_date__lte=time, sys_end_date__gt=time)

    def add_version(self, temporalModel):
        txn_now = datetime.now()
        # If accessed via a reverse relation, queryset should have an 'instance' hint with
        # parent of relation
        qs = self.get_queryset()

        # Determine identity model instance
        # If this function is called via a reverse relation, identity will be set to the owner,
        # even if already specified in the model.
        # Otherwise, the model being added must already specify its identity
        if 'instance' not in qs._hints and not temporalModel.identity:
            raise Exception('')
        if 'instance' in qs._hints:
            temporalModel.identity = qs._hints['instance']

        def archive(version):
            hist_version = copy(version)
            hist_version.pk = None
            hist_version.sys_end_date = txn_now
            hist_version.save()

            version.sys_start_date = txn_now
            return version

        with transaction.atomic():
            overlapping_versions = qs.filter(valid_start_date__lt=temporalModel.valid_end_date, valid_end_date__gt=temporalModel.valid_start_date, sys_end_date=datetime.max, identity=temporalModel.identity)
            contained_versions = [version for version in overlapping_versions
                                  if version.valid_start_date >= temporalModel.valid_start_date and version.valid_end_date <= temporalModel.valid_end_date]
            left_overlap = [version for version in overlapping_versions
                            if version.valid_start_date < temporalModel.valid_start_date
                            and version.valid_end_date <= temporalModel.valid_end_date]
            right_overlap = [version for version in overlapping_versions
                             if version.valid_start_date >= temporalModel.valid_start_date
                             and version.valid_end_date > temporalModel.valid_end_date]
            super_overlap = [version for version in overlapping_versions
                             if version.valid_start_date < temporalModel.valid_start_date
                             and version.valid_end_date > temporalModel.valid_end_date]
            # TODO: final case

            if len(left_overlap) > 1 or len(right_overlap) > 1 or len(super_overlap) > 1:
                raise Exception("This temporal queryset does not meet the temporal invariant")

            for version in contained_versions:
                # version.delete()
                version.sys_end_date = txn_now
                version.save()

            for version in left_overlap:
                archive(version)

                version.valid_end_date = temporalModel.valid_start_date
                version.save()

            for version in right_overlap:
                archive(version)
                version.valid_start_date = temporalModel.valid_end_date
                version.save()

            for version in super_overlap:
                archive(version)
                end_version = copy(version)
                end_version.pk = None
                end_version.valid_start_date = temporalModel.valid_end_date
                version.valid_end_date = temporalModel.valid_start_date
                version.save()
                end_version.save()

            temporalModel.sys_start_date = txn_now
            temporalModel.save()

            FooTimestamp.objects.create(identity=temporalModel.identity, timestamp=txn_now)


class TemporalModel(models.Model):
    class Meta:
        abstract = True
        ordering = ("valid_start_date",)

    valid_start_date = models.DateField(null=False)
    valid_end_date = models.DateField(null=False)
    sys_start_date = models.DateTimeField(null=False)
    sys_end_date = models.DateTimeField(null=False, default=datetime.max)

    temporal = TemporalManager()
    objects = TemporalManager()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.valid_start_date} {self.valid_end_date} {self.value}>"


    # def between(self, start_date, end_date):
    #     return self.get_queryset().filter(start_date__lt=end_date, end_date__gt=start_date, identity=self.identity)


class Foo(models.Model):
    pass


class FooVersion(TemporalModel):
    identity = models.ForeignKey(Foo, on_delete=models.PROTECT, related_name="temporal")
    value = models.FloatField(default=0)

class FooTimestamp(models.Model):
    identity = models.ForeignKey(Foo, on_delete=models.PROTECT, related_name="versions")
    timestamp = models.DateTimeField(null=False)