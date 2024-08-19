from rest_framework import serializers
from .models import Story
from user_app.serializers import UserSerializer
from django.contrib.auth.models import User

# Serializer for the User model
class StorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    contributions = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Story
        fields = '__all__'

    def get_contributions(self, obj):
        user_contributions = []
        for contribution in obj.contributions:
            user = User.objects.get(id=contribution['userId'])
            user_data = UserSerializer(user).data
            user_contributions.append({
                'user': user_data,
                'content': contribution['content']
            })
        return user_contributions

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['title'] = str(representation['title']).title()
        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        title = request.data.get('title')
        if not title or title.strip() == '':
            raise serializers.ValidationError("Title cannot be empty")
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['title'] = str(request.data.get('title')).title()
        content = request.data.pop('content', None)
        validated_data['contributions'] = [
            {
                'userId': request.user.id,
                'content': content
            }
        ]
        instance = Story.objects.create(**validated_data)

        if 'image' in request.FILES:
            instance.image = request.FILES['image']
            instance.save()
            
        return instance

    def update(self, instance, validated_data):
        import pdb;pdb.set_trace()
        request = self.context.get('request')
        content = request.data.pop('content', None)
        instance.contributions.append({
            'userId': request.user.id,
            'content': content
        })
        validated_data['contributions'] = instance.contributions
        for attr, value in validated_data.items():
            if attr == 'title':
                value = str(value).title()
            setattr(instance, attr, value)
        instance.save()
        return instance


    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB max size
            raise serializers.ValidationError("Image file too large ( > 5MB ).")

        if not value.name.endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Only .jpg, .jpeg, .png files are allowed.")
        return value

    def validate(self, data):
        content = self.context['request'].data.get('content', None)
        if not content or content.strip() == '':
            raise serializers.ValidationError("Content cannot be empty")
        return data
