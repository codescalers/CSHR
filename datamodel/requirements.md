<!-- This file wil contain all project requirements and their dependencies-->

<!-- DataBase Tables -->
<!-- * End of probation period (a link to the evaluation form) <Date> RunTime: celery task will run every day and calculate today's date / joined date -->
## UserTable

* UserTable:
  * email address
  * Joining date
  * Vacations-Balance
  * Full name
  * Mobile number
  * Telegram
  * Picture Photo
  * birthday
  * Location 1:1 <Office>
  * Skills M:M <Skills>
  * Trainings-courses 1:M <Trainings-courses >
  * Social insurance number
  * Team <ENUM> => (Dev-QA-Ops-Marketing-Management-Accounting)
  * Evaluations M:M <Evaluations>
  * company-properties 1:M <Company-properties>
  * Salary: {
      Net Salary before joining (optional),
      Joining Salary (optional),
      Current Salary NET (Required),
      Current Salary GROSS (Required)
    } 

* Skills:
  * name UQ

* Office
  * name UQ
  * country

* Trainings-courses 
  * id
  * name
  * certificate-link


* Evaluations
  * id
  * user <User>e
  * link
  * date

* Company-properties
  <!-- that have been given to (laptop, bag, screen, sim card,.... -->
  * id
  * image-of
  * name
  * user <User>
  * date

* Vacations:
  * id
  * User <User> > Applying
  * User <User> > Accepting || Denied
  * Type (ENUM) ENUM("Annual Leaves","Public Holidays","Emergency Leave","Leave Excuses ( calculate based on his annual days )")
  * Changlelog

* Compensation:
  * User <User> 
  * id
  * Reason
  * dates of work

* HR-letters:
  * id
  * User <User> 
  * addressee
    ### TODO: asking about `if salary should be mentioned (checkbox)` and `if certain dates should be mentioned (checkbox + date picker)` and `Request official docs from HR` 

* Requests:
  * id
  * Vacations <Vacations>
  * Compensation <Compensation>
  * HR-letters <HR-letters>
  * Type ENUM("Vacations","Compensation","HR-letters")

  * approve
