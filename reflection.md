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
 The scheduler currently detects time conflicts only by exact start-time matches (tasks that share the same "HH:MM" string) instead of computing full interval overlaps using task durations. This keeps conflict-detection very simple and fast.
- Why is that tradeoff reasonable for this scenario?
 This tradeoff is reasonable for a lightweight, owner-facing planner because many routine pet tasks are scheduled at explicit start times (feedings, walks). Exact-match checking is cheap and easy to explain; if users report overlapping intervals as a problem, the logic can be extended later to perform interval-overlap checks or a timeline allocation algorithm.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI for debugging and refactoring but I kept the design choices for myself.
- What kinds of prompts or questions were most helpful?
What does this line mean? If I want to do this, what can I do to achieve it?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
For the time when I was trying to improve the sort by time function, AI had suggested a method that looked cleaner but performance wise was bad and I am not a huge fan of having nested functions.

- How did you evaluate or verify what the AI suggested?
I read through each section of the codebase if I did not understand I asked a question until I understood everything.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested task completion, pet task management, chronological sorting, daily recurrence, conflict detection, schedule generation, empty pet edge case, non-recurring task completion, and completed tasks are ignored in conflicts.

- Why were these tests important?
These tests were important because the scheduler's to test how the scheduler's decisions worked like which tasks get scheduled, in what order, and under what conditions.

**b. Confidence**

- How confident are you that your scheduler works correctly? I am 4/5 confident right now.
- What edge cases would you test next if you had more time? Owner with zero available minutes (should produce an empty schedule, not an error), and a mandatory task whose duration exceeds the owner's total available time

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with the Scheduler class. It ended up covering much more than I originally planned and it all fits together in a way that is easy to read and test. The decision to keep Schedule as a separate class also paid off. It made generate_schedule() cleaner and made total_time and remaining_time easy to track.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
 I would improve conflict detection to check full time intervals (start time + duration) instead of just matching exact start times.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The biggest thing I learned is that a good UML diagram is a living document. My initial diagram was missing the Schedule class entirely, and several methods I ended up building were not planned at all. Working with AI made this more visible when I described what I needed, the AI often surfaced design questions I had not considered, which forced me to make deliberate choices rather than just writing code and hoping it fit together.
