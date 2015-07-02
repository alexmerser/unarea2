import argparse
import sys
from traceback import format_exc

from unarea_core.users.bins import USER_MODEL
from unarea_core.session.bins import SESSION_MODEL
from unarea_core.users.domains import User


def register_user():
    parser = argparse.ArgumentParser(description='Registers user.')
    parser.add_argument("first_name", help="User's name")
    parser.add_argument("last_name", help="User's last name")
    parser.add_argument("email", help="User's email")
    parser.add_argument("password", help="User's password")
    args = parser.parse_args()

    try:
        new_user = User(args.first_name, args.last_name, args.email, args.password)
        success = USER_MODEL.create(new_user, args.password)

        if not success:
            sys.exit(1)
        print "Success! New user id: %s" % success

    except StandardError:
        print "Exception occured while trying to create user:\n%s" % format_exc()
        sys.exit(1)


def get_session():
    """
    bin/cli/users/register first_name lastggg email@ggg pass1111
    Success! New user id: 55926effb3820554761675af

    bin/cli/users/get_session 55926effb3820554761675af

    :return:
    """
    parser = argparse.ArgumentParser(description='Get or creates a session for this user.')
    parser.add_argument("user_id", help="User's id.")
    args = parser.parse_args()
    try:
        user = USER_MODEL.get_by_id(args.user_id)
        session = SESSION_MODEL.get_by_user(user)
        if not session:
            print "Session for user not found. Creating..."
            session = SESSION_MODEL.create_session_for_user(user)

        return session.token

    except StandardError:
        print "Exception occured while trying to create user:\n%s" % format_exc()
        sys.exit(1)