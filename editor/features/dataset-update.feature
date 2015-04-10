Feature: Dataset creation.
  Background:
    Given "csv" format with "csv" extensions exists
      and I am authenticated user
      and I have permission to add dataset
      and I have permission to change dataset
      and I have permission to add source
      and I have permission to change source

  Scenario: 1. Dataset formats are populated from datafiles and disabled
    Given dataset "dataset1" exists
      and "dataset1" dataset has datafile with "csv" format
      and "dataset1" dataset has datafile with "xlsx" format
    When I open "dataset1" dataset update page
    Then I see "csv" format selected in the dataset formats
      and I see "xlsx" format selected in the dataset formats
      and I see dataset formats checkboxes are disabled
