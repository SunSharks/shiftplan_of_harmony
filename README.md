# shiftplan_of_harmony

## deftab/
### index.php
index.php uses def.js for definitions of day and job credentials.
**Day input fields** can be added by clicking the plus sign in the top left corner. Deletion by clicking the minus symbol next to the last day box. You can only delete the last day box.

**Job input fields** can be added by clicking the second plus sign. Deletion by clicking the minus symbol of the job box. You can delete each job box on its own.
**Helper checkbox** is made for jobs that don't follow the usual rules of shift assignment and build a seperate data set for an own model.
In def.js, the `name_special` variable can be changed to change the label for this checkbox. It can be used to mark all kinds of exceptions.
**Sensibel checkbox** makes the default preference value equals 5 for all jobs of that jobtype.

### tab.php
tab.php uses deftabsketch.js to create a editable table to define time intervals of jobs.

### delete_jobtype.php

## crew_prios/
Website to define preferences for each job that is not a helper job.
For a costum man text rename the file "indexman.php" to "_indexman.php" and edit its containing text.
### index.php

.
## TODO

* Barrierefreie Farben!
* Layout von allem.
* Mehr utf8s in die encoding Funktionen.

### deftab
#### Appearence
* Calculate & show day of griditems.
* [DONE] Show how many griditems are currently selected.
* Red frame around each job after saving for a short time.
* Nicer css

#### Functionality
* The person who created a job(type) should be the only one who is able to delete/edit that job(type).
* [DONE] Delete jobtype and corresponding jobs. (button, functionality, security, integrety)
* [DONE] Link day entries of table Jobs to corresponding entry of table Days.
* [DONE] Numeric date format for day.
* [DONE[ German Umlauts!!!
* [DONE] Insert Jobtypes into DB only once even if tab.php is reloaded.
* [DONE] Create day view: edit one day at whole page.

* [DONE] Job db table with a column that refers to corresponding jobtype.
* [DONE] Insert new job only if its not predefined.
* [DONE] Show predefined jobs in deftabsketch.

* Create view to edit only new jobs.
* Competences --> Create file upload (*.txt)
* [DONE] Show competences text as info text on hover
* Button to view competences text as whole Document (optional)
* Download button for competences text.
* Number input in jobbox for twins (dublicate jobs).

### prios
#### index
* Equal width of table columns.
* [DONE] Style fixed table row headers.
* Nicer css
* selectable rows and columns

#### signup
* [DONE] Hash PW
* Autocomplete full name


### New file structure
