Feature: Dataset creation.
  Background:
    Given "csv" format with "csv" extensions exists
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
      and GET response to example.com returns links: "file1.csv, file2.csv"
    When I populate dataset form title with "Test-title1"
      and I populate other fields of the dataset form with random values
      and I populate download page with "http://example.com" url
      and I click on "Scrape" button inside "Data files" block
    Then I see popup with urls scrapped from http server
    When I check input next to the "file1.csv" url
      and I check input next to the "file2.csv" url
      and I click on "Ok" button
    Then I see "file1.csv, file2.csv" urls added to "Data files" formset
    When I select "csv" file format in both urls
      and I click on "Save" button
    Then new dataset with "Test-title1" creates
      and "Test-title1" dataset contains "file1.csv" data file
      and "Test-title1" dataset contains "file2.csv" data file
      and I see dataset edit form
      and dataset form contains "file1.csv" data file
      and dataset form contains "file2.csv" data file

  Scenario: 5. Guessing and populating data file format
    Given dataset create form is opened
      and I have permission to add datafile
      and I have permission to change datafile
      and I have permission to add documentfile
      and I have permission to change documentfile
      and GET response to example.com returns links: "file1.csv, file2.csv"
    When I populate dataset form title with "Test-title1"
      and I populate other fields of the dataset form with random values
      and I populate download page with "http://example.com" url
      and I click on "Scrape" button inside "Data files" block
    Then I see popup with urls scrapped from http server
      and I see "csv" format name near each data file
    When I check input next to the "file1.csv" url
      and I click on "Ok" button
    Then I see "file1.csv" urls added to "Data files" formset
      and I see "csv" file format is selected
