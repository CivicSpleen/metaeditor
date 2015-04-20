Feature: List of the datasets

    Scenario: 1. Authenticated user sees table with existing datasets
        Given 3 datasets exists
          and I am authenticated user
          and I access the "/" url
        Then I see dataset list page
          and I see table with all three datasets
          and "Dataset List" menu option is active

    Scenario: 2. Authenticated user opens first dataset from list
        Given dataset with "title1" title exists
          and I am authenticated user
          and I have permission to add dataset
          and I have permission to change dataset
          and I access the "/" url
        Then I see dataset list page
        When I click dataset with "title1" title
        Then I see "title1" dataset edit page
