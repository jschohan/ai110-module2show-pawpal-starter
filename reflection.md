# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
3 core actions a user should be able to perform are to add their pet, add and edit tasks as well as set priorities for the tasks, and the user should be able to generate a daily plan.

My initial plan is to have 3 classes - Pet, Owner, Task, and Plan. The pet class will have variables to store name, species, and tasks. Owner will store name and pets. The task class will store task names, priority, and times. The Plan class will store tasks and generate a plan with those tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
The Claude Code review of my skeleton pointed out that scheduler does not have any link
to the owners or pets that a task belongs to, it only stores a list of tasks. As suggested, I changed scheduler to instead pull tasks from the owner's list of pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler considers time to create the schedule. I decieded this mattered the most because tasks should be completed in the order
that they are required. If a task is high priority it can simply be scheduled to the earliest time. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff that my scheduler makes is that it only detects when multiple tasks start at the same time and not when they overlap. To find overlap we would have to add an attribute for duration in addition to start times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI during every phase of the project. I started by brainstorming classes and attributes then asked AI to generate a UML diagram based on that description. Then I 
asked it to implement a skeleton using that diagram, then I asked it implement the logic. I also used it for refactoring my main file to display a cleaner print message
to the terminal.

- What kinds of prompts or questions were most helpful?
Prompting the AI to make changes with specific instructions for the functionality of the chanegs were the most helpful. Also prompting the AI
when to plan versus make changes. This allowed me to review changes before adding them to the file so that I can ensure I understand the 
code. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Based on my prompts, AI only made edits that I asked it to. I did not find any unwanted edits or functionality so I accepted the suggestions as is. One time I did not accept a suggestion was a 'fix' that stated my reoccuring task logic was incorrect. The AI failed to understand that if a task is overdue by 3 days of the 'duedate' it would not make sense to reschedule it for the duedate + 1 day. Since that would mean it is still overdue. 
- How did you evaluate or verify what the AI suggested?
I read through the code and ran the tests that it generated. I also asked clarifying questions based on the code suggested which sometimes exposed oversights made by the AI or inaccurate understanding of the prompt/goal.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested the UI to System wiring manually, this was important since the test cases only cover the system logic.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I am confident that my scheduler works correctly though there are some features that were not implemented or covered. I would test the UI more with time and test the functionality of switching between owner objects and ensure that pets are correctly stored per owner and not just per session.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisifed with writing a backend then creating a UI that reflects that backend. 
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the 'wiring' between the UI and backend as I believe some functions aren't actually made available to a user in the 
streamlit UI. 
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned was how complicated it can be to design an entire app even while working with AI. It is also important to be very specific with prompts to ensure that the app has the intended functionality. Also, even though the AI is great at generating tests for the system logic that was written, the UI testing requires a human.