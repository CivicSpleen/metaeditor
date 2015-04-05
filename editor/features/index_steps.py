# -*- coding: utf-8 -*-

from lettuce import step, world


@step(u'Then I see the menu')
def then_i_see_the_menu(step):
    menu_block = world.elem('.masthead')
    assert menu_block.is_displayed()


@step(u'and I see auth block')
def and_i_see_auth_block(step):
    auth_block = world.elem('.auth')
    assert auth_block.is_displayed()


@step(u'and auth block contains facebook login')
def and_auth_block_contains_facebook_login(step):
    auth_block = world.elem('.auth')
    assert 'Login with Facebook' in auth_block.text


@step(u'and auth block contains google login')
def and_auth_block_contains_google_login(step):
    auth_block = world.elem('.auth')
    assert 'Login with Google' in auth_block.text


@step(u'and auth block contains my full name')
def and_auth_block_contains_my_full_name(step):
    user = world.get_current_user()
    auth_block = world.elem('.auth')
    assert user.get_full_name() in auth_block.text
