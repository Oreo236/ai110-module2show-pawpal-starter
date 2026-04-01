# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Add a pet and owner
Add a task
See daily schedule to be able to plan appropriately

- What classes did you include, and what responsibilities did you assign to each?
I included a Owner, Pet, Task and Scheduler. Owner holds the owner’s info, how much time they have each day, and their preferences; responsible for expressing the constraints and habits the planner must respect. Pet contains the pet’s details and the tasks that pet needs; responsible for listing what care that pet requires and any pet-specific rules. Task describes one care action (what it is, how long it takes, how important it is, and any preferred timing or must-do status); responsible for defining the units of work the planner schedules. Scheduler takes the owner’s constraints and the pets’ tasks and decides which tasks to do today, in what order, and which to skip; responsible for balancing time, priority, preferences, and mandatory tasks and for explaining the result.

**b. Design changes**

- Did your design change during implementation? Yes, it did, I added a Schedule class as well
- If yes, describe at least one change and why you made it.
Copilot suggested I add a Schedule class because it separates the planner's decision-making from the final plan so totals, summaries, and edits are handled cleanly and are easier to test.



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
