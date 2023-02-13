from django.contrib.auth.models import User, Group
from accounts.serializers import UserSerializer
from django.shortcuts import get_object_or_404


class UserHelper(object):
    @classmethod
    def createUser(klass, userData):
        """
        creates new User instance
        """
        created_user = UserSerializer(data=userData)
        if created_user.is_valid():
            created_user.save()
            return created_user.data, True
        return created_user.errors, False

    @classmethod
    def deleteUser(klass, userPk):
        """
        deletes user by user_id
        """
        user = klass.getUser(userPk)
        return user.delete()

    @classmethod
    def getUser(klass, userPk):
        """
        retrieves user by user_id or responds with 404
        """
        return get_object_or_404(User, pk=userPk)

    @classmethod
    def listUsers(klass):
        """
        returns a list of all users
        """
        return User.objects.all()

    @classmethod
    def updateUser(klass, pk, updateData):
        user_instance = klass.getUser(pk)
        updated_user = UserSerializer(
            user_instance, data=updateData, partial=True)
        if updated_user.is_valid():
            updated_user.save()
            return updated_user.data, True
        return updated_user.errors, False

    @classmethod
    def check_user(klass, user_email):
        """
        # checks for the existence of a user by email property
        """
        try:
            user = User.objects.get(email=user_email)
            if user:
                return True
        except User.DoesNotExist:
            return False
