Feature: Category tree feature
    Background:
      Given I am authenticated user
        and I have permission to add category
        and I have permission to change category

    Scenario: 1. Authenticated user creates category node without parent
        Given I access the "/" url
          and root category node with "root1" name exists
          and category node with "categ1" name exists
          and I click on "Categories Hierarchy Editor" menu option
        Then I see category tree page
        When I click on "categ1" link
        Then I see "categ1" category update form
        When I click on "Add child" link
        Then I see category node creation form
          and parent category field contains "categ1" category
        When I fill "categ2" to the category name field
          and I empty parent category field
          and I click save button
        Then new category with "categ2" name and "root1" parent creates
          and I see "categ2" category update form
          and I see "categ2" category in the tree
          and I see add child link

    Scenario: 2. Authenticated user creates new category with parent
        Given root category node with "root1" name exists
          and category node with "categ2" name exists
          and I access the "/editor/category" url
        Then I see category tree page
        When I click on "categ2" category in the tree
        Then I see "categ2" category update form
        When I click on "Add child" link
        Then I see category node creation form
          and parent category field contains "categ2" category
        When I fill "categ3" to the category name field
          and I click save button
        Then new category with "categ3" name and "categ2" parent creates
          and I see "categ3" category update form
          and I see "categ3" category in the tree
          and I see add child link
