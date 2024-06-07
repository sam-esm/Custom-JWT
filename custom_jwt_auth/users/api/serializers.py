from django.contrib.auth import authenticate

from rest_framework import serializers

from custom_jwt_auth.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    """
    Serializer for the User model. It includes fields that are necessary for user registration and authentication.
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('phone_number', 'username', 'password', 'token',)
        read_only_fields = ("token",)

    def update(self, instance, validated_data):
        """
        Performs an update on a User. If a password is included in validated_data, 
        it sets the password using set_password method.
        """
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
 
            setattr(instance, key, value)

        if password is not None:

            instance.set_password(password)


        instance.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. It includes necessary fields for user registration.
    """

    # The client should not be able to send a token along with a registration
    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    class Meta:
        model = User
        fields = ["username","phone_number","password","token"]

    def create(self, validated_data):
        """
        Creates a new user instance.
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. It includes fields necessary for user authentication.
    """
    phone_number = serializers.CharField(max_length=11)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data) :
        """
        Validates the data during user login. If the phone_number and password does not match, it raises a validation error.
        """
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)
        print(data)
        user = authenticate(username=phone_number, password=password)
        if not user:
            raise serializers.ValidationError(
                "A user with this phone_number and password was not found."
            )
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {"phone_number": user.phone_number, "username": user.username, "token": user.token}
