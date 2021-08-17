from rest_framework import serializers

from .models import CustomUser
from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=3, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=3, required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs.get('password')
        password_conf = attrs.pop('password_confirm')
        if password != password_conf:
            raise serializers.ValidationError('Passwords aren\'t same!')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activations_code,
                             status='register')
        return user


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(min_length=3, required=True)
    password_confirm = serializers.CharField(min_length=3, required=True)

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('This user is not registered')
        return email

    def validate_activation_code(self, activation_code):
        if not CustomUser.objects.filter(activations_code=activation_code, is_active=False).exists():
            raise serializers.ValidationError('Activation code is False!')
        return activation_code


    def validate(self, attrs):
        password = attrs.get('password')
        password_conf = attrs.pop('password_confirm')
        if password != password_conf:
            raise serializers.ValidationError('Passwords aren\'t same!')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')
        try:
            user = CustomUser.objects.get(email=email, activations_code=activation_code,
                                          is_active=False)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User does not fined')

        user.is_active = True
        user.activations_code = ''
        user.set_password(password)
        user.save()
        return user
