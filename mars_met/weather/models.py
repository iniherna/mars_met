from django.db import models


from django.db import models
from datetime import datetime, timedelta
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager

class report_QuerySet(QuerySet):
	pass

class report(models.Model):
	sol=models.IntegerField(primary_key=True)
	terrestrial_date=models.DateTimeField(null=True)
	objects=PassThroughManager.for_queryset_class(report_QuerySet)()

	def __unicode__(self):
		return str(self.sol)

class magnitude(models.Model):
	sol=models.ForeignKey('report',db_column='sol',primary_key=True)
	min_temp=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	max_temp=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	pressure=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	pressure_string=models.CharField(max_length=64, null=True)
	abs_humidity=models.CharField(max_length=64, null=True)
	wind_speed=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	wind_direction=models.CharField(max_length=16, null=True)
	atmo_opacity=models.CharField(max_length=64, null=True)
	season=models.CharField(max_length=64, null=True)
	ls=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	sunrise=models.CharField(max_length=16, null=True)
	sunset=models.CharField(max_length=16, null=True)
	
	def __unicode__(self):
		return self.sol.terrestrial_date.strftime('%Y-%m-%d')