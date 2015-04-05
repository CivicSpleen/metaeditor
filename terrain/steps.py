# -*- coding: utf-8 -*-

# global (common) steps for all features

from lettuce import step, world

from accounts.tests.factories import UserFactory


@step(u'(Given|and) I am authenticated user')
def given_i_am_authenticated_user(step, unused):
    # I have to be staff to make admin login.
    # TODO: find way to authenticate user without admin to get rid of making user staff.
    user1 = UserFactory()
    user1.is_staff = True
    user1.save()
    logged_in = world.do_admin_login(user1.username, '1', world.browser)
    assert logged_in, 'Failed to log in'
