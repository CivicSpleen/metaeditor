Feature: Dataset creation.
  Background:
    Given "csv" format exists
      and I am authenticated user
      and I have permission to add dataset
      and I have permission to change dataset
      and I have permission to add source
      and I have permission to change source

  Scenario: 1. Authenticated user opens dataset edit form
    Given source edit page is opened
    When I click on "Add dataset" link
    Then I see dataset edit form
      and I see Data files and Documents blocks
      and I see "Scrape" button in the "Data files" block
      and I see "Scrape" button in the "Documents" block

  Scenario: 2. Authenticated user creates new dataset
    Given dataset create form is opened
    When I populate dataset form title with "Test-title1"
      and I populate other fields of the dataset form with random values
      and I click on "Save" button
    Then new dataset with "Test-title1" creates
      and I see dataset edit form

  Scenario: 3. Authenticated user creates new dataset with links to files
    Given dataset create form is opened
    When I populate dataset form title with "Test-title1"
      and I populate other fields of the dataset form with random values
      and I populate "Data files" first form with "File1", "csv" and "http://ya.ru"
      and I populate "Documents" first form with "Doc1", "md" and "http://ya.ru"
      and I click on "Save" button
    Then new dataset with "Test-title1" creates
      and "Test-title1" dataset contains "File1" data file
      and "Test-title1" dataset contains "Doc1" document file
      and I see dataset edit form
      and dataset form contains "File1" data file
      and dataset form contains "Doc1" document file

  Scenario: 4. Authenticated user uses Scrape to populate data files
    Given dataset create form is opened
      and I have permission to add datafile
      and I have permission to change datafile
      and I have permission to add documentfile
      and I have permission to change documentfile
      and pydoc http server is running on "localhost:1234"
      and datafiles filtering drops everything except urls containing "__"
    When I populate dataset form title with "Test-title1"
      and I populate other fields of the dataset form with random values
      and I populate download page with "http://localhost:1234" url
      and I click on "Scrape" button inside "Data files" block
    Then I see popup with urls scrapped from pydoc http server
    When I check input next to the "__builtin__" url
      and I check input next to the "__future__" url
      and I click on "Ok" button
    Then I see "__builtin__, __future__" urls added to "Data files" formset
    When I select "csv" file format in both urls
      and I click on "Save" button
    Then new dataset with "Test-title1" creates
      and "Test-title1" dataset contains "__builtin__" data file
      and "Test-title1" dataset contains "__future__" data file
      and I see dataset edit form
      and dataset form contains "__builtin__" data file
      and dataset form contains "__future__" data file
