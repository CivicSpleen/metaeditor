# -*- coding: utf-8 -*-

# initialization script for lettuce BDD framework.
# running BDD tests:
#  $ python manage.py harvest --no-server
# --no-server option is important because dadata BDD tests uses django's live server and test db

from lettuce import before, after, world

import fudge

from django.db import connection, connections
from django.db.transaction import TransactionManagementError
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.models import Session
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management import call_command
from django.test.testcases import LiveServerThread

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# common functions for all features


def wait(fn, timeout=5, msg='Timeout waiting'):
    """
    Waits until fn returns something except None or False or timeout finished.
    """
    ret = WebDriverWait(world.browser, timeout)\
        .until(fn, msg)
    return ret


def wait_selector(query_fn, selector, timeout=7):
    """
    Returns element found by given selector.
    """
    def inner(driver):
        try:
            return query_fn(selector)
        except NoSuchElementException:
            pass

    msg = u'Timeout waiting for %s query with %s selector.' % (query_fn, selector)
    ret = world.wait(inner, msg=msg, timeout=timeout)
    return ret


def _elem(selector, timeout=7):
    """
    returns DOM element found by given selector.
    """
    return wait_selector(
        world.browser.find_element_by_css_selector,
        selector,
        timeout=timeout)


def _elems(selector, timeout=7):
    """
    returns list of DOM elements found by given selector.
    """
    return wait_selector(
        world.browser.find_elements_by_css_selector,
        selector,
        timeout=timeout)


def _get_a(text):
    """ Finds link by text and returns it. """
    for a in world.elems('a'):
        if a.text == text:
            return a
    raise Exception('a with %s text was not found' % text)


def _get_button(text):
    """ Finds button by text and returns it. """
    for btn in world.elems('button'):
        if btn.text == text:
            return btn
    raise Exception('button with %s text was not found' % text)


def _get_current_user(flush=False):
    """ Returns browser user or user who is operating with API.

    Args:
        flush (boolean): if True, does not return cached user, instead get it again.

    Returns:
        User or AnonymousUser:
    """

    # find session cookie
    session_key = world.browser.get_cookie('sessionid')['value']

    # first try to find in the cache
    if not flush and getattr(world, '__cached_session_key', '') == session_key:
        return world.__cached_current_user

    # find session by cookie
    session = Session.objects.get(session_key=session_key)

    # find user by session
    user_id = session.get_decoded().get('_auth_user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = AnonymousUser()
    world.__cached_session_key = session_key
    world.__cached_current_user = user
    return user


def do_admin_login(username, password, browser):
    """
    Logs user in using django admin interface. User should be staff or superuser.
    Returns True if user was logged in, otherwise returns False.
    """

    # user exists and it has access to admin site
    assert User.objects.get(username=username).is_staff
    live_server_url = world.live_server_url
    browser.get('%s%s' % (live_server_url, '/admin/'))
    username_input = world.elem('#id_username')
    username_input.send_keys(username)
    password_input = browser.find_element_by_name('password')
    password_input.send_keys(password)
    world.elem('.submit-row input').click()

    # admin site is shown
    user_tools = world.elem('#user-tools')
    return user_tools.is_displayed()


def select_option(selector, option_value=None, option_text=None):
    """ Selects given option in the given select box. """
    if not option_value and not option_text:
        raise Exception('You should provide either value or text of the option')

    select_elem = world.elem(selector)

    clicked = False

    if option_value:
        checker = lambda elm, val: elm.get_attribute('value') == val
    else:
        checker = lambda elm, txt: elm.text == txt
    for option in select_elem.find_elements_by_css_selector('option'):
        if checker(option, option_value or option_text):
            option.click()
            clicked = True
    if option_value:
        mess = 'Option with %s value was not found in the %s' % (option_value, selector)
    else:
        mess = 'Option with %s text was not found in the %s' % (option_text, selector)
    assert clicked, mess


@before.harvest
def initial_setup(server):

    connection.creation.create_test_db(True, autoclobber=True)

    host = 'localhost'
    possible_ports = [8081]
    connections_override = {}

    for conn in connections.all():
        # If using in-memory sqlite databases, pass the connections to
        # the server thread.
        share_thread = (
            conn.settings_dict['ENGINE'].rsplit('.', 1)[-1] in ('sqlite3', 'spatialite')
            and conn.settings_dict['NAME'] == ':memory:')
        if share_thread:
            # Explicitly enable thread-shareability for this connection
            conn.allow_thread_sharing = True
            connections_override[conn.alias] = conn
    live_server_thread = LiveServerThread(
        host, possible_ports, StaticFilesHandler,
        connections_override=connections_override)
    live_server_thread.daemon = True
    live_server_thread.start()

    # Wait for the live server to be ready
    live_server_thread.is_ready.wait()
    if live_server_thread.error:
        raise live_server_thread.error

    world.live_server_url = 'http://%s:%s' % (
        live_server_thread.host, live_server_thread.port)

    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.chrome.favicons', False)
    fp.set_preference('browser.chrome.site_icons', False)
    world.browser = webdriver.Firefox(fp)

    # helpers
    world.wait = wait
    world.elem = _elem
    world.elems = _elems
    world.get_a = _get_a
    world.get_button = _get_button
    world.get_current_user = _get_current_user
    world.do_admin_login = do_admin_login
    world.select_option = select_option

    settings.DEBUG = True


@after.harvest
def cleanup(server):
    world.browser.quit()
    connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])


@before.each_scenario
def reset_data(scenario):
    # Clean up django.
    try:
        call_command('flush', interactive=False, verbosity=0)
    except TransactionManagementError:
        pass
    try:
        call_command('loaddata', 'all', verbosity=0)
    except TransactionManagementError:
        pass
    fudge.clear_calls()
