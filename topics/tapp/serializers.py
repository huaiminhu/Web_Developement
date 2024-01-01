from rest_framework import serializers
from tapp.models import Topics
class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = "__all__" # RESTful API 所有 HTTP Methods