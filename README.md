# shiftplan_of_harmony

index.html uses def.js for definitions of day and job credentials.
**Day input fields** can be added by clicking the plus sign in the top left corner. Deletion by clicking the minus symbol next to the last day box. You can only delete the last day box.

**Job input fields** can be added by clicking the second plus sign. Deletion by clicking the minus symbol of the job box. You can delete each job box on its own.
**Helper checkbox** is made for jobs that don't follow the usual rules of shift assignment.
In def.js, the `name_special` variable can be changed to change the label for this checkbox. It can be used to mark all kinds of exceptions.

## TODO

### Appearence
* Calculate & show day of griditems.
* Show how many griditems are currently selected.
* Red frame around each job after saving for a short time.
* Nicer css

### Functionality
* The person who created a job(type) should be the only one who is able to delete/edit that job(type).
* German Umlauts!!!
* [DONE] Job db table with a column that refers to corresponding jobtype.
* Link that Jobtype to its column somehow in sql.
* Insert new job only if its not predefined.
* Show predefined jobs in deftabsketch.
