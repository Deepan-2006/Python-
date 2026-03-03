# Quick Testing Guide

## How to Test the Fixes

### 1. Testing Certificate Preview (Fix #1)

**Steps:**
1. Go to http://localhost:8000
2. Login with your account
3. Select any category (e.g., Technical)
4. Choose a topic (e.g., Programming)
5. Configure the quiz (select difficulty)
6. Take the quiz and answer questions
7. Score at least 75% (answer at least 8 out of 10 questions correctly for an easy 80%)
8. Check the results page

**Expected Result:**
- You should see a beautiful certificate preview displayed directly on the results page
- The certificate shows:
  - Your username
  - Quiz topic name
  - Your score percentage
  - Certificate ID
  - Issue date
- Below the certificate, you'll see two buttons:
  - "View Full Screen" - opens certificate in new tab
  - "Download PDF" - downloads the certificate

**What was fixed:**
- Before: Certificate only downloadable, not visible
- After: Certificate previews inline PLUS download option

---

### 2. Testing Topic-Specific Questions (Fix #2)

**Steps:**
1. Go to http://localhost:8000
2. Login with your account
3. On the category list page, you should now see **4 tabs**:
   - Technical
   - Non-Technical
   - Academic
   - Entertainment

4. Click each tab to verify categories display

**Test Technical Category:**
1. Click "Technical" tab
2. Verify you see the Technical category
3. Click "Start Quiz"
4. You should see 5 topics:
   - Programming
   - Data Structures
   - DBMS
   - Networking
   - Cyber Security
5. Select "Programming"
6. Take the quiz - questions should be about programming (HTML, Python, JavaScript, etc.)

**Test Different Topics:**
1. Go back and select "Data Structures"
2. Take the quiz - questions should be about stacks, queues, arrays, etc.
3. Compare - questions should be DIFFERENT between Programming and Data Structures

**Test Other Categories:**

**Non-Technical:**
- Topics: Aptitude, Reasoning, General Knowledge, Current Affairs
- Try "Aptitude" - expect math and logic questions
- Try "General Knowledge" - expect geography, history questions

**Academic:**
- Topics: Physics, Chemistry, Mathematics
- Try "Physics" - expect questions about force, energy, light
- Try "Chemistry" - expect questions about elements, compounds

**Entertainment:**
- Topics: Sports, Movies, Music
- Try "Sports" - expect questions about athletes, games
- Try "Movies" - expect questions about films, directors

**Expected Result:**
- Each topic shows questions relevant to that specific topic
- Questions are NOT the same across all topics
- Questions are specific to the selected topic

**What was fixed:**
- Before: All quizzes showed same generic questions
- After: Each topic has its own specific relevant questions

---

## Quick Verification Checklist

- [ ] 4 category tabs visible (Technical, Non-Technical, Academic, Entertainment)
- [ ] Click through each tab successfully
- [ ] Each category shows multiple topics
- [ ] Technical category has 5 topics
- [ ] Non-Technical category has 4 topics
- [ ] Academic category has 3 topics
- [ ] Entertainment category has 3 topics
- [ ] Questions in Programming topic are about programming
- [ ] Questions in Physics topic are about physics
- [ ] Questions in Sports topic are about sports
- [ ] After scoring 75%+, certificate preview appears on results page
- [ ] Certificate shows correct user name and score
- [ ] "View Full Screen" button works
- [ ] "Download PDF" button works

---

## Database Populated With:

Total: **15 Topics** with **75 Questions** (5 per topic)

**Technical (5 topics, 25 questions):**
- Programming (HTML, Python, JavaScript)
- Data Structures (Stack, Queue, Linked List)
- DBMS (SQL, Normalization, Primary Keys)
- Networking (IP, HTTP, Routers)
- Cyber Security (Phishing, SSL, Encryption)

**Non-Technical (4 topics, 20 questions):**
- Aptitude (Math, Percentages, Series)
- Reasoning (Logic, Patterns, Analogies)
- General Knowledge (Countries, Geography, Science)
- Current Affairs (Politics, Economics, Events)

**Academic (3 topics, 15 questions):**
- Physics (Force, Energy, Speed of Light)
- Chemistry (Elements, Compounds, pH)
- Mathematics (Algebra, Geometry, Calculus)

**Entertainment (3 topics, 15 questions):**
- Sports (Cricket, Football, Olympics)
- Movies (Directors, Actors, Films)
- Music (Instruments, Composers, Artists)

---

## Troubleshooting

**Issue: Certificate not showing**
- Check if score is >= 75%
- Ensure you completed the quiz
- Check browser console for errors

**Issue: Topics not showing**
- Ensure populate_db.py ran successfully
- Check database has categories and subcategories
- Verify in Django admin panel

**Issue: Same questions in different topics**
- This should NOT happen with the new implementation
- If it does, run: `python populate_db.py` again
- Clear browser cache

---

## Next Steps After Testing

If everything works:
1. ✅ Delete old/duplicate data if any
2. ✅ Add more questions per topic (currently 5 each)
3. ✅ Customize certificate design if needed
4. ✅ Add more topics to categories if desired
