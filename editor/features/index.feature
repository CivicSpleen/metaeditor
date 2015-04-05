Feature: Index page.

    Scenario: Anonymous user index page
        Given I access the "/" url
        Then I see the menu
          and I see auth block
          and auth block contains facebook login
          and auth block contains google login

    Scenario: Authenticated user index page
        Given I am authenticated user
          and I access the "/" url
        Then I see the menu
          and I see auth block
          and auth block contains my full name
