from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh_ = RefreshToken.for_user(user)
    return({
        "refresh":str(refresh_),
        "access":str(refresh_.access_token)
    })
    
    