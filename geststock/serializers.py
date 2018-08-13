from rest_framework.serializers import  ModelSerializer
from .models import Pays, Province








class PaysSerializer(ModelSerializer):

	class Meta:
		model = Pays
		fields = ['libelle', 'code']


class ProvinceSerializer(ModelSerializer):
	pays = PaysSerializer()

	def to_internal_value(self, data):
		self.fields['Pays'] = serializers.PrimaryKeyRelatedField(
			queryset = Pays.objects.all()
			)
		return super(ProvinceSerializer, self).to_internal_value(data)

	class Meta:
		model = Province
		fields = ['libelle', 'code', 'pays',]

	




	


