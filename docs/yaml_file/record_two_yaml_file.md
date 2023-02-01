# Record Two YAML File

This YAML file contains basic information about a record_two.

The keys included in the file are:

- `title`: a string that represents the title.

- `description`: a field that is optional and provides a description or additional information about the record.

- `visible`: a boolean that indicates whether the record is visible or not. The default value is True.

- `editors`: an optional list of strings that represent the users who have editing rights for the record.

- `viewers`: an optional list of strings that represent the users who have viewing rights for the record.

Example usage:

    title: Record from John Doe
    description: This is an example of record
    visible: True
    editors:
        - JaneDoe
        - BobSmith
    viewers: 
        - AliceJohnson
        - DavidBrown
