# Planned Features

## High Priority

### 7. Convert Skill to Generic (Country-Agnostic) 📋
**Release Target:** v10.0 (Major Version)  
**Status:** Specifications Complete ✅ | Ready for Implementation  
**Last Updated:** October 30, 2025  
**Estimated Effort:** 10-15 hours  
**Breaking Changes:** Yes (requires v10.0)

**Priority Components** (User-Defined):
- **P1** (Highest): First-run setup wizard
- **P2**: Market-specific salary templates
- **P3**: Multi-currency support (USD, EUR, GBP, etc.)
- **P4**: Multiple country support in single config
- **P5** (Lower): Backward compatibility with existing data

**Supported Countries:**
1. Israel (existing, reference implementation)
2. United States
3. United Kingdom
4. Canada
5. Germany
6. France
7. Netherlands
8. Singapore
9. Australia
+ Custom/Other option

**Key Features:**
- Auto-detect country from system locale
- Interactive setup wizard
- Market-specific defaults and terminology
- Currency-neutral salary templates
- Automated migration for existing Israel data
- Hybrid global + regional tier system

**Implementation Phases:**
1. Configuration Foundation (2-3 hours)
2. Core Module Updates (3-4 hours)
3. Templates & Documentation (2-3 hours)
4. Migration & Testing (2-3 hours)
5. Polish & Release (1-2 hours)

**Documentation:** Full specification in main PROJECT_PLAN.md under Feature #7.

---

### 8. Create Feature to Generate Personal Data via Chat Questions 📋
**Priority:** High  
**Status:** Design phase  
**Estimated Effort:** 8-12 hours

**Overview:**
Interactive onboarding wizard to collect user data through conversational questions.

**Components:**
- Interactive onboarding wizard
- LinkedIn CV import option
- Location and storage preference selection
- Initial market research
- Self-assessment for skills
- Location priorities configuration

**Qualifying Questions Needed:**
- Separate onboarding module or integrated into main skill?
- LinkedIn import: API-based or manual upload?
- Filesystem vs. Google Drive: Auto-detect or always ask?
- Market research data sources?
- Self-assessment: Rating scale?
- Validate inputs or trust user?
- Repeatable or one-time only?
- How to handle updates over time?

---

## Medium Priority

### 9. Update Headers Structure 📋
**Priority:** Medium  
**Status:** Planning phase  
**Estimated Effort:** 2-4 hours

**Goals:**
- Improve YAML frontmatter consistency
- Add metadata standards
- Better categorization

**Qualifying Questions Needed:**
- What specific header improvements?
- Which files need updated headers?
- New metadata fields to add?
- Migrate existing files or only new files?

---

### 10. Update Excel Python Script for Friendly Report 📋
**Priority:** Medium  
**Status:** Design phase  
**Estimated Effort:** 4-6 hours

**Goals:**
- Generate downloadable Excel reports in chat
- Enhanced formatting and charts
- Summary statistics
- Export functionality

**Qualifying Questions Needed:**
- What specific reports? (Summary, detailed, trends?)
- Automatic or on-demand?
- Important visualizations?
- Multiple export formats? (Excel, CSV, PDF?)
- Report frequency?

---

### 11. Update Personal Data 📋
**Priority:** Medium  
**Status:** Planning phase  
**Estimated Effort:** 3-5 hours

**Goals:**
- Enhance candidate profile structure
- Better CV organization
- Improved salary data templates

**Qualifying Questions Needed:**
- What's missing from current structure?
- Which fields cause most friction?
- Add more CV metadata?
- Handle multiple versions of same CV type?

---

## Lower Priority (Future - Post v10.0)

### 12. Resume Generation & Tailoring System ✅
**Status:** Specifications Complete | Ready for Implementation  
**Priority:** P1 (High) - Implement in v10.0 alongside Feature #7  
**Last Updated:** October 30, 2025  
**Estimated Effort:** 12-18 hours  
**Documentation:** `docs/FEATURE_RESUME_GENERATION_SYSTEM.md`

**Feature Summary:**
- LinkedIn profile import (Bright Data MCP + manual fallback)
- Professional markdown resume generation (English + Hebrew)
- Job-specific resume tailoring (<30% changes)
- Cover letter generation (interactive, 5-10 questions)
- HTML → PDF export pipeline (browser-based)
- Deep integration with job analysis system
- HTML database management tab

**Implementation Phases:**
1. Core generation (4-6 hours)
2. HTML report integration & PDF export (3-4 hours)
3. Cover letter generator (2-3 hours)
4. Documentation & polish (2-3 hours)

**Success Criteria:**
- LinkedIn import works (MCP or manual)
- Resume generated in <5 minutes
- Tailoring improves job match scores
- 80%+ user adoption
- Seamless end-to-end workflow

---

### 13. STAR Framework Questionnaire with Template 📋
**Priority:** Lower  
**Status:** Concept phase  
**Estimated Effort:** 6-8 hours

**Goals:**
- Interactive STAR framework helper
- Pre-filled templates
- Example responses
- Company/role-specific customization

**Qualifying Questions Needed:**
- Integrate with existing interview prep tools?
- How many STAR stories to prepare?
- Suggest which stories fit which roles?
- Template format?
- Score/rank prepared stories?
- Integration with job analysis workflow?

---

### 14. Industry Tracker: Show User Status vs. Market 📋
**Priority:** Lower  
**Status:** Concept phase  
**Estimated Effort:** 10-15 hours

**Goals:**
- Compare user profile to industry benchmarks
- Skill gap analysis
- Improvement recommendations
- Career trajectory visualization

**Qualifying Questions Needed:**
- Data sources for industry benchmarks?
- Which metrics to track?
- How often to refresh industry data?
- Automated or manual refresh?
- Visualization format?
- Privacy concerns?
- Prescriptive or suggestive recommendations?

---

## Vision / Future Evolution (Post v11.0+)

### 15. Career Guard: Proactive Career Management System 🚀
**Release Target:** v12.0+ (Major Product Evolution)  
**Status:** Vision / Concept Phase  
**Last Updated:** October 30, 2025  
**Estimated Effort:** 100+ hours (6-12 months development)  
**Product Evolution:** From reactive job tool → proactive career advisor

**Vision Statement:**
Transform from a job analysis tool into a comprehensive, always-on career management system that proactively guides your long-term career growth. Career Guard removes career planning from your mental load by continuously monitoring your progress, market trends, and opportunities—presenting actionable insights when you need them.

---

#### 🎯 Core Concept

**"Fully Active FOR YOU"**
- Proactive, not reactive: The system initiates check-ins and recommendations
- Removes career management from your mental overhead
- Continuous monitoring and guidance
- Personal career dashboard showing current state and momentum
- Adaptive to life stages and goals

**Philosophy:**
- Free your mind from career anxiety
- Atomic habits approach for sustainable growth
- Context-aware advice based on age, family, market conditions
- Long-term strategy with short-term actionable steps

---

#### 🏗️ Core Components

##### 1. **Proactive Qualifying Questions System**
**What it does:**
- Periodically asks strategic career questions (weekly/monthly)
- Adapts questions based on current life stage and goals
- Builds comprehensive career profile over time
- Non-intrusive timing (suggests best moments to check in)

**Example Questions:**
- "How satisfied are you with your current role this month? (1-10)"
- "Any significant changes in your team or company situation?"
- "What skill did you invest time in this month?"
- "How's your work-life balance feeling lately?"
- "Any interesting opportunities that crossed your path?"

**Frequency:**
- Weekly: Quick pulse check (2-3 questions, 2 minutes)
- Monthly: Deeper reflection (10-15 questions, 15 minutes)
- Quarterly: Strategic review (career direction, goals assessment)
- Annual: Major life stage review

---

##### 2. **Personal Career Dashboard**
**What it shows:**
- **Current State**: Role, company, tenure, satisfaction levels
- **Career Momentum**: Trending up, stable, or declining
- **Life Stage**: Pivot, Sustain, Growth, Double Down
- **Market Position**: How you compare to market benchmarks
- **Recent Activity**: Skills developed, accomplishments, challenges
- **Opportunities**: New roles, internal moves, market trends
- **Action Items**: Recommended next steps with priority

**Visual Elements:**
- Career trajectory graph (past 5 years + projected)
- Skills heat map (strength vs. market demand)
- Compensation tracking (vs. market + your targets)
- Network health score
- Interview readiness gauge
- Learning momentum tracker

**Update Frequency:**
- Real-time: When you add new data
- Weekly: Automated insights refresh
- Monthly: Comprehensive status update

---

##### 3. **Atomic Habits for Career Growth**
**Integration with James Clear's Framework:**

**Make it Obvious:**
- Visual career progress tracking
- Clear next actions always visible
- Habit stacking suggestions

**Make it Attractive:**
- Celebrate small wins (skill milestones, accomplishments)
- Visualize long-term compound growth
- Connect daily habits to career goals

**Make it Easy:**
- Micro-habits: 5-minute learning sessions
- Pre-built templates for common tasks
- Automated tracking and reminders

**Make it Satisfying:**
- Progress streaks and milestones
- Before/after comparisons
- Share wins with mentors/peers

**Example Career Habits:**
- **Daily:** 15 min of industry reading
- **Weekly:** Connect with 1 person in your network
- **Monthly:** Update 1 section of your resume
- **Quarterly:** Have 1 coffee chat with someone outside your company

**Habit Personalization:**
- Based on your career path (IC, Manager, Executive)
- Adapted to your life stage (early career, established, senior)
- Aligned with your goals (promotion, pivot, learn new skill)

---

##### 4. **Life Stage Intelligence**
**Adaptive advice based on current stage:**

**🌱 PIVOT Stage** (Major career change)
- Age/Situation: Career transition, industry switch, first management role
- Focus: Exploration, networking, skill building
- Advice: Take calculated risks, invest in learning, build new networks
- Timeline: 6-18 months intensive effort
- Success Metrics: New skills acquired, interview performance, offers received

**⚡ GROWTH Stage** (Active advancement)
- Age/Situation: Mid-career (30s-40s), energy high, family situation stable
- Focus: Aggressive skill building, promotions, compensation growth
- Advice: Maximize learning, take visible projects, build leadership
- Timeline: 2-5 years of sustained effort
- Success Metrics: Promotions, compensation increases, scope expansion

**🏡 SUSTAIN Stage** (Maintain position)
- Age/Situation: Young family, lifestyle priority, senior role achieved
- Focus: Maintain current level, work-life balance, steady income
- Advice: Optimize current role, avoid burnout, protect family time
- Timeline: 1-3 years, then reassess
- Success Metrics: Satisfaction, stability, family well-being

**🚀 DOUBLE DOWN Stage** (Maximum acceleration)
- Age/Situation: Clear opportunity, optimal conditions, high ambition
- Focus: All-in on career advancement, maximize momentum
- Advice: Take big swings, leadership roles, equity opportunities
- Timeline: 6-24 months intensive push
- Success Metrics: Step-function career jump, equity value, impact

**🌅 COAST Stage** (Pre-retirement optimization)
- Age/Situation: 50s+, financial security achieved, legacy focus
- Focus: Mentorship, strategic work, lifestyle optimization
- Advice: Leverage experience, reduce stress, meaningful work
- Timeline: 5-15 years to retirement
- Success Metrics: Satisfaction, legacy projects, next-gen impact

**Auto-Detection:**
- Age + family situation + career goals + current role
- User can override or manually set stage
- System suggests stage transitions based on context

---

##### 5. **Company & Business Health Monitoring**
**What it tracks:**
- Company financial health (public data, news, funding rounds)
- Layoff risks and warning signs
- Market position vs. competitors
- Your team's situation (hiring, reorgs, budget changes)
- Leadership changes and their implications

**Alerts:**
- 🔴 **High Risk**: Company in trouble, consider exit strategy
- 🟡 **Medium Risk**: Monitor closely, prepare contingency
- 🟢 **Stable**: Good position, focus on growth
- 🔵 **Hot**: Company thriving, maximize opportunity

**User Input:**
- Monthly: "How's your company/team doing?"
- Captures: Morale, changes, concerns, opportunities
- System combines with external data for full picture

---

##### 6. **Monthly Activity Review**
**Automated Check-In:**
- "What did you accomplish this month?"
- "What new skills did you practice?"
- "Any challenges or setbacks?"
- "Interesting conversations or learnings?"

**System Analyzes:**
- Progress against goals
- Skill development patterns
- Career momentum trends
- Potential gaps or risks

**Generates:**
- Monthly summary report
- Insights and patterns
- Recommended focus areas for next month
- Celebration of wins

---

##### 7. **Local Market Trends & Opportunities**
**Automated Market Intelligence:**
- Tracks Israeli tech market (or user's market)
- Monitors roles matching your profile
- Identifies emerging opportunities
- Salary trend analysis
- Hot companies and roles

**Proactive Alerts:**
- "3 new Engineering Manager roles at tier-1 companies"
- "Wix just announced 200-person hiring plan"
- "Average EM salary increased 8% this quarter"
- "Your target companies are actively hiring"

**Smart Filtering:**
- Only surfaces relevant opportunities
- Based on your current stage (not annoying if in SUSTAIN)
- Respects your preferences and priorities
- Can be paused/adjusted anytime

---

##### 8. **Continuous Profile Updates**
**What it maintains:**
- Resume/CV always current
- Skills inventory (with recency)
- Accomplishments log
- Network contacts and notes
- Interview talking points (STAR stories)
- Compensation history

**How it works:**
- Monthly: "Anything to add to your profile?"
- Captures new projects, skills, accomplishments
- System suggests resume updates
- Maintains different CV variants automatically

**Benefits:**
- Always interview-ready
- No last-minute scramble to update resume
- Comprehensive career history
- Easy to generate tailored resumes on-demand

---

##### 9. **Long-Term Strategy Engine**
**Strategic Career Planning:**
- Multi-year career roadmap
- Milestone tracking
- Momentum-based recommendations
- Decision point identification

**Key Recommendations:**
- **When to move:** Based on tenure, growth, market conditions
- **When to ask for raise:** Timing, preparation, negotiation strategy
- **When to pivot:** Signals that it's time for change
- **When to double down:** Maximize current opportunity
- **When to coast:** Optimize for lifestyle/balance

**Momentum Analysis:**
- Tracks your career velocity
- Identifies acceleration or deceleration
- Suggests interventions to maintain/improve trajectory
- Warns about stagnation risks

**Example Insights:**
- "You've been in current role 18 months. Market data shows optimal tenure is 24-36 months for your level."
- "Your skill development pace has slowed. Consider: [specific actions]"
- "Compensation is 15% below market. Recommend preparing for raise discussion in Q2."
- "Company situation declining. Consider activating job search in 3-6 months."

---

#### 🎨 User Experience

**Dashboard View:**
```
┌─────────────────────────────────────────────────────────┐
│ Career Guard Dashboard - November 2025                  │
├─────────────────────────────────────────────────────────┤
│ 👤 Profile: Gur Sannikov                               │
│ 🎯 Stage: GROWTH                                        │
│ 📊 Momentum: ↗️ Trending Up (+12% this quarter)        │
│ 🏢 Company Health: 🟢 Stable                           │
│ 💰 Market Position: Top 20% for EM roles              │
├─────────────────────────────────────────────────────────┤
│ 📋 This Month's Summary:                               │
│ ✅ Completed GraphQL course                            │
│ ✅ Led 3 hiring interviews                             │
│ ✅ Shipped major feature release                        │
│ ⚠️  Work-life balance slipping (6→5 rating)           │
├─────────────────────────────────────────────────────────┤
│ 🎯 Recommended Actions:                                │
│ 1. [High] Schedule raise discussion (18mo tenure)      │
│ 2. [Medium] Update STAR story for recent launch        │
│ 3. [Low] Connect with 2 EMs at target companies        │
├─────────────────────────────────────────────────────────┤
│ 🔔 Market Updates:                                     │
│ • 5 new EM roles at tier-1 companies (view)           │
│ • Average EM salary up 7% this quarter                 │
│ • Wix announced major expansion                        │
└─────────────────────────────────────────────────────────┘
```

**Interaction Patterns:**
- **Passive Mode**: Dashboard updates, no action required
- **Check-in Mode**: System asks questions, user responds
- **Active Mode**: User requests analysis or advice
- **Alert Mode**: Critical updates or opportunities

**Communication Style:**
- Encouraging, not pushy
- Data-driven, not preachy
- Actionable, not overwhelming
- Respectful of user's time and autonomy

---

#### 🚀 Implementation Phases

**Phase 1: Foundation (Months 1-3)**
- Basic dashboard framework
- Monthly check-in system
- Profile continuous update mechanism
- Life stage detection logic

**Phase 2: Intelligence (Months 4-6)**
- Market trend tracking
- Company health monitoring
- Momentum analysis engine
- Habit tracking system

**Phase 3: Proactive Features (Months 7-9)**
- Automated insights generation
- Strategic recommendation engine
- Opportunity surfacing
- Alert system

**Phase 4: Polish & Integration (Months 10-12)**
- Full dashboard UI
- Mobile companion app consideration
- Integration with existing features
- User testing and refinement

---

#### 📊 Success Metrics

**User Engagement:**
- Weekly active users
- Check-in completion rate
- Dashboard view frequency
- Action item completion rate

**Career Outcomes:**
- Promotions achieved
- Salary increases
- Successful pivots
- Interview success rate
- User satisfaction scores

**System Performance:**
- Recommendation relevance
- Alert accuracy
- Profile completeness
- Market intelligence freshness

---

#### 🔐 Privacy & Data

**Data Ownership:**
- All data stays on user's machine
- No external data collection
- User controls all sharing
- Can export/delete anytime

**Optional Cloud Sync:**
- For multi-device access
- End-to-end encrypted
- User controls sync schedule
- Can disable entirely

---

#### 💭 Open Questions / Design Decisions

**Product Questions:**
1. **Opt-in vs. Opt-out:** Is Career Guard default on, or explicit activation?
2. **Notification Channels:** In-app only, or email/mobile notifications too?
3. **Check-in Frequency:** User configurable? How to avoid notification fatigue?
4. **Data Retention:** How long to keep historical data? Auto-archive old data?
5. **Mobile App:** Separate mobile companion, or web-only?
6. **Monetization:** Premium feature tier, or keep fully free?

**Technical Questions:**
1. **Background Processing:** How to run periodic checks without user interaction?
2. **State Management:** How to persist dashboard state across sessions?
3. **Market Data Sources:** Which APIs to use for market intelligence?
4. **Scheduling:** How to trigger time-based check-ins?
5. **Performance:** How to keep dashboard fast with lots of historical data?

**User Experience Questions:**
1. **Onboarding:** How to introduce Career Guard without overwhelming users?
2. **Stage Transitions:** Manual or automatic life stage changes?
3. **Action Overload:** How to prevent too many recommendations?
4. **Habit Formation:** How to make career habits actually stick?
5. **Dashboard Customization:** How much control to give users over layout/content?

---

#### 🎯 Next Steps (When Ready to Start)

1. **User Research:**
   - Interview 10-20 target users about career management pain points
   - Survey current users about interest in proactive features
   - Identify most valuable components to build first

2. **MVP Definition:**
   - Choose 3-5 core features for v1.0 of Career Guard
   - Define minimum viable dashboard
   - Design lightest-weight check-in system

3. **Technical Spike:**
   - Prototype background job system
   - Test market data API integrations
   - Build simple dashboard mockup

4. **Documentation:**
   - Detailed technical specification
   - API integration plan
   - Database schema design
   - UI/UX mockups

5. **Roadmap Integration:**
   - Break into smaller milestones
   - Estimate realistic timeline
   - Identify dependencies on existing features
   - Plan gradual rollout strategy

---

#### 💡 Related Features

**Synergies with Existing Roadmap:**
- #7 (Country-Agnostic): Career Guard needs market data for multiple countries
- #8 (Personal Data via Chat): Foundation for qualifying questions system
- #12 (Resume Generation): Profile continuous updates enable always-current resumes
- #13 (STAR Framework): Feeds into interview readiness tracking
- #14 (Industry Tracker): Powers market intelligence component

**New Capabilities Enabled:**
- Career Guard makes the tool sticky (daily/weekly engagement)
- Opens premium/monetization opportunities
- Creates network effects (aggregate market insights)
- Enables coaching/advisory services
- Builds comprehensive career dataset over time

---

**Status:** 💡 Vision - Requires extensive user research and product validation before development  
**Next Review:** After MVP release and initial user feedback collection
