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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
