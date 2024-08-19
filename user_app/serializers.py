from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        instance = self.instance

        if User.objects.exclude(pk=instance.pk if instance else None).filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")

        if User.objects.exclude(pk=instance.pk if instance else None).filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):

        password = validated_data.pop('password', None)

        instance = super().create(validated_data)

        if password:
            instance.set_password(password)

        instance.save()


        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)

        instance.save()

        return instance
