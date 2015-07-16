from unarea_core.ext.restfull import ApiService
from unarea_accounts.handlers import UserHandler, UserSigninHandler,\
    UserSignupHandler, UserSignoutHandler, UserProfileHandler, UserActivationHandler


USER_ACCOUNT_API = ApiService()

USER_ACCOUNT_API.add_resource(UserSignupHandler, '/signup')
USER_ACCOUNT_API.add_resource(UserSigninHandler, '/signin')
USER_ACCOUNT_API.add_resource(UserSignoutHandler, '/signout')
USER_ACCOUNT_API.add_resource(UserActivationHandler, '/activate/<string:activation_token>')
USER_ACCOUNT_API.add_resource(UserProfileHandler, '/<string:user_id>/profile')
