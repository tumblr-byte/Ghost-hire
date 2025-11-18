# 👻 Ghost Crew Feature - Find Your Hackathon Squad!

## The Problem You Described

- Self-taught devs have no team for hackathons
- LinkedIn is fake networking, no real connections
- Need genuine friendships, not corporate BS
- Want constructive criticism, not fake positivity
- Need teammates with complementary skills

## The Solution: Ghost Crew 🔥

### Feature 1: The Roast Zone 🔥
**Post your projects, get ROASTED (constructively)**

- Post your code/projects
- Get REAL feedback (no "great work!" BS)
- AI detects fake positivity
- Upvote helpful roasts
- Learn and grow from criticism

### Feature 2: Crew Browser 👻
**Discover developers by their REAL skills**

- Browse all verified ghosts
- See their GitHub stats, Devpost wins
- Filter by skills (Python, React, etc.)
- See "Skill Match %" (complementary skills)
- Check their Ghost Power Level

### Feature 3: Ghost Crew Formation 🎃
**Send invitations, build your squad**

- Create a Ghost Crew (max 5 members)
- Send crew invitations to developers
- They accept/decline
- Build your hackathon dream team
- Track crew success

### Feature 4: Crew Chat 💬
**Real-time chat with your crew**

- Private crew chat room
- Share code, links, files
- Plan hackathons together
- No corporate spam
- Genuine friendships

## The Flow

```
1. Browse Crew Browser
   ↓
2. Find developer with complementary skills
   ↓
3. Check their Haunted Portfolio
   ↓
4. Send Crew Invitation
   ↓
5. They accept
   ↓
6. Chat in Crew Room
   ↓
7. Build projects together
   ↓
8. Win hackathons! 🏆
```

## Why This Slaps 🔥

✅ **No Fake Networking** - Real friendships only
✅ **Skill-Based Matching** - Find complementary teammates
✅ **Real Feedback** - Roasts that actually help
✅ **Anti-Corporate** - No "synergy" BS
✅ **Hackathon Ready** - Built for collaboration
✅ **Gen Z Vibes** - Fun, casual, authentic

## Features to Build

### Phase 1: Crew Browser
- [ ] Page showing all verified developers
- [ ] Display GitHub stats, Devpost wins
- [ ] Filter by skills
- [ ] Show Skill Match %
- [ ] "Send Crew Invitation" button

### Phase 2: Ghost Crew
- [ ] Create crew (max 5 members)
- [ ] Send/receive invitations
- [ ] Accept/decline invitations
- [ ] Crew member list
- [ ] Leave crew option

### Phase 3: Crew Chat
- [ ] Real-time chat (WebSockets)
- [ ] Share code/links
- [ ] Online/offline status
- [ ] Notifications
- [ ] File sharing

### Phase 4: The Roast Zone
- [ ] Create posts (title, description, code)
- [ ] Comment on posts
- [ ] AI detects fake positivity
- [ ] Upvote helpful roasts
- [ ] "Actually Helpful" badge

## Database Models Needed

### GhostCrew Model
```python
- name (e.g., "The Python Haunters")
- members (max 5 users)
- created_by (user)
- created_at
- crew_bio
- hackathons_won
```

### CrewInvitation Model
```python
- from_user
- to_user
- crew
- status (pending/accepted/declined)
- message
- created_at
```

### CrewMessage Model
```python
- crew
- sender
- message
- created_at
- is_code (boolean)
```

### RoastPost Model
```python
- author
- title
- description
- code_snippet
- project_link
- created_at
- roast_score
```

### RoastComment Model
```python
- post
- author
- comment
- is_helpful (voted by post author)
- upvotes
- created_at
```

## Tech Stack

- **Backend**: Django Channels (WebSockets for chat)
- **Frontend**: HTMX for real-time updates
- **Database**: MySQL (existing)
- **AI**: OpenAI API for fake positivity detection

## Gen Z Language 🎃

Instead of:
- ❌ "Team" → ✅ "Ghost Crew"
- ❌ "Networking" → ✅ "Making friends"
- ❌ "Professional" → ✅ "Real"
- ❌ "Feedback" → ✅ "Roast"
- ❌ "Collaborate" → ✅ "Build together"
- ❌ "Connect" → ✅ "Vibe with"

## This is What We Need! 🔥

No more fake LinkedIn connections. No more solo hackathons. No more corporate BS.

Just real devs, real skills, real friendships. Let's build! 👻🎃

Ready to implement? Let me know which phase to start with! 🚀
