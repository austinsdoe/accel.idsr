=====================
ACCEL IDSR Input Form
=====================
Integrated Disease Surveillance and Response (IDSR) Form
--------------------------------------------------------

Key aspects:

- The system must be simple enough to allow users with minimum IT skills to go throught the whole process of registration.
- The system must have several validators to prevent users to fill (or leave empty) fields that are key elements for further steps, when the sample is received in the lab.
- The system must include a mechanism to keep track of the completness of each form and the user responsible of its completion. This will allow another user with more privileges to verify the work done by others and address shortcomings.
- The system must ensure the security of access and data encryption. Only users with credentials will have access.
- The system must connect with Bika Health LIS instance automatically and register the data into the system, so this information will be later accessible in the lab when receiving the samples.


The ISDR form is made by a number of steps that will end up with a confirmation page that will display the data registered, allowing the user to go back and do some changes or submit it. The structure of this wizard form works like follows:

- A top bar navigation with the numbered steps. The current step should be prominently displayed (e.g, green background). If the user has already filled data in a given step, the number of the step will be displayed as a link to the view for that step. Steps without data will be displayed as a label.
- A central content area where the form will be rendered.
- Each step will contain 5 fields at maximum to make it easier to fill for unskilled people.
- A footer with Previous, Next and Cancel buttons.
- Once the “Cancel” button is pressed, a poup will be displayed (“Are you agree you want to cancel the current submission process?”), with Yes/No buttons. If the user presses the button “Yest” he/she will be redirected to the step 1 of the wizard, allowing him/her to create a new form.
- Each time the user presses “Next”, the system will validate the data introduced and will warn the user if there is something missing or wrong
- In the confirmation view, the “Next” button will be replaced by a “Submit” button.
- In the confirmation form, the data provided will be displayed the same way it looks in the printed form.
- The confirmation page will have a checkbox (by default unselected) stating “I agree with the information provided”. The submit button will be active only when the user selects this checkbox.
- Once submitted, the user will be redirected to Step 1, for the creation of a new form.
- The user could eventually close the browser, so the system must store the information provided earlier in cache (session/cookie). Once the user starts again the browser, the application will redirect the user to the step in which he/she was before closing the browser.
