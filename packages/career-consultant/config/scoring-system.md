# Scoring System v3.0

## Total Score Formula
```
TOTAL = Match + Income + Growth + LowPrep + Stress + Location
Range: 40-90 points typical
Target: ≥54 (First Priority)
Excellence: ≥80 🏆 (Challenge Achievement)
```

## Component Breakdowns

### 1. Match Score (0-35 points + 5 bonus)

**Formula:**
```
Base Score = Weighted average of matched skills (0-35)
Weight = Skill proficiency from candidate-profile (1-10)
Bonus = +5 if Intel role
```

**Calculation:**
1. Identify required skills from job description
2. Map to candidate skills (1-10 proficiency)
3. Calculate weighted average: Σ(skill_match × proficiency) / Σ(proficiency)
4. Scale to 0-35 points
5. Add +5 if Intel (institutional knowledge)

**Scoring Guide:**
- 30-35: Perfect match, all key skills 8-10 proficiency
- 25-29: Strong match, most skills covered
- 20-24: Good match, some gaps
- 15-19: Moderate match, significant gaps
- 10-14: Weak match, major skill gaps
- 0-9: Poor match, wrong role type

### 2. Income Score (0-25 points)

**Formula:**
```
Base = Role tier × Experience level × Location factor
Premiums: AI (+15-25%), Hardware (+10-15%), Platform PM (+15-20%)
Score = Map estimate to 0-25 scale
```

**Israeli Market Tiers (14+ years experience):**
- **Tier 1** (Public/market leaders): ₪1.4M-2.0M base range
- **Tier 2** (Well-funded): ₪1.2M-1.6M base range
- **Tier 3** (Established): ₪1.0M-1.4M base range
- **Tier 4** (Early stage): ₪0.8M-1.2M base range

**Role Factors:**
- Engineering Manager: 1.2x
- Director: 1.4x
- VP/Head: 1.6x
- Senior TPM: 1.1x
- Platform PM: 1.15x

**Location Factors:**
- Tel Aviv: 1.0x (baseline)
- Petah Tikva: 0.95x
- Herzliya/Raanana: 0.98x
- Haifa: 0.90x
- Jerusalem: 0.85x

**Premiums (multiply):**
- AI/ML focus: +15-25%
- Hardware/semiconductors: +10-15%
- Platform products: +15-20%
- Cybersecurity: +5-10%

**Scoring Scale:**
```
25 points: ≥₪2.0M (Outstanding)
20 points: ₪1.6M-2.0M (Excellent)
15 points: ₪1.2M-1.6M (Target)
10 points: ₪1.0M-1.2M (Acceptable)
5 points: ₪960K-1.0M (Floor)
0 points: <₪960K (Below minimum)
```

**CRITICAL:** Never web search for compensation. Use only salary-data.md.

### 3. Growth Score (0-20 points + 3 bonus)

**Formula:**
```
Company Trajectory (0-10) + Role Scope (0-10) + Hardware Bonus (+3)
```

**Company Trajectory (0-10):**
- Tier 1, market leader, growing: 9-10
- Tier 2, fast growth, funded: 7-8
- Tier 3, stable, mature: 5-6
- Tier 4, uncertain, early: 2-4
- Declining or troubled: 0-1

**Role Scope (0-10):**
- VP/C-level, >200 people: 9-10
- Director, 100-200 people: 7-8
- Senior Manager, 50-100: 5-6
- Manager, 20-50: 3-4
- Senior IC or small team: 1-2

**Additional Factors:**
- Learning opportunities: +1-2
- New technology domain: +1-2
- Global impact/visibility: +1-2
- Career path clarity: +1-2

**Bonus:**
- +3 if hardware/semiconductor company (aligns with background)

**Scoring Guide:**
- 18-20: Exceptional growth, career-defining
- 14-17: Strong growth, clear trajectory
- 10-13: Moderate growth, some opportunity
- 6-9: Limited growth, lateral move
- 0-5: No growth, potential regression

### 4. LowPrep Score (0-15 points)

**Formula:**
```
Estimated Prep Hours = Company complexity + Role gap + Interview difficulty
Score = Inverse scale (less prep = higher score)
```

**Prep Hour Estimation:**

**Company Complexity (20-60 hours):**
- Tier 1, familiar domain: 20-30 hours
- Tier 2, some familiarity: 30-40 hours
- Tier 3, new domain: 40-50 hours
- Tier 4, unknown space: 50-60 hours

**Role Skills Gap (10-50 hours):**
- Perfect match (Match ≥30): 10-15 hours
- Strong match (Match 25-29): 20-30 hours
- Good match (Match 20-24): 30-40 hours
- Moderate match (Match <20): 40-50 hours

**Interview Difficulty (10-40 hours):**
- Glassdoor "Easy" or familiar: 10-15 hours
- Glassdoor "Average": 20-30 hours
- Glassdoor "Difficult": 30-40 hours

**Total Prep = Company + Role Gap + Interview**

**Scoring Scale (Inverse):**
```
15 points: 40-50 hours (Low prep, quick start)
12 points: 50-70 hours (Moderate prep)
9 points: 70-90 hours (Substantial prep)
6 points: 90-120 hours (Heavy prep)
3 points: 120-150 hours (Extensive prep)
0 points: >150 hours (Unrealistic)
```

**Conservative Approach:**
Always estimate on the high side. Better to overestimate prep time.

### 5. Stress Score (-5 to -10 points)

**Formula:**
```
Glassdoor culture + Work-life indicators + Role demands
All stress is penalty (negative points)
```

**Glassdoor Culture:**
- ≥4.0 rating, positive WLB: -5 (Low stress)
- 3.0-3.9 rating, mixed WLB: -7 (Medium stress)
- <3.0 rating, negative WLB: -10 (High stress)

**Work-Life Indicators:**
- Remote/flexible: -1 (reduce penalty)
- Reasonable hours culture: -1 (reduce penalty)
- Crunch time mentions: +2 (increase penalty)
- Always-on culture: +3 (increase penalty)
- On-call requirements: +2 (increase penalty)

**Role Demands:**
- IC/Senior IC: -0 (baseline)
- Manager, small team: +1
- Manager, large team: +2
- Director/multi-team: +3
- VP/Exec: +4

**Final Calculation:**
```
Base stress + WLB adjustments + Role demands
Capped at -10 (worst) to -5 (best)
```

**Scoring Guide:**
- -5: Low stress, sustainable, family-friendly
- -7: Medium stress, manageable, some pressure
- -10: High stress, demanding, family impact

### 6. Location Score (-8 to +5 points)

**Fixed Scoring (Israel-specific):**
```
Remote: +5 (Ideal - maximum flexibility)
Tel Aviv: 0 (Central, acceptable)
Petah Tikva: -1 (Close, doable)
Herzliya: -4 (Further, traffic)
Raanana: -5 (Long commute)
Haifa: -7 (Very far, relocation consideration)
Jerusalem: -8 (Challenging commute)
```

**Modifiers:**
- Hybrid 2-3 days: +1 to location score (more flexibility)
- Full office required: -1 to location score (less flexibility)
- Monthly travel required: -2 (time away from family)

**Special Cases:**
- International: Auto-reject (not relocating)
- Multiple locations: Use worst-case location
- Future relocation expected: Flag as concern

## Priority Thresholds

### First Priority (≥54 points)
- Strong consideration
- Worth significant prep time
- Apply unless red flags

### Second Priority (<54 points)
- Backup options
- Apply if limited alternatives
- Monitor but don't prioritize

### Challenge Achievement (≥80 points) 🏆
- Exceptional opportunity
- Top priority
- Maximum prep investment justified
- Flag prominently in all outputs

## Calculation Validation

**Before saving scores:**
1. Verify all components sum correctly
2. Check bonus applications (Intel +5, Hardware +3)
3. Confirm penalties are negative (Stress, often Location)
4. Validate total is in reasonable range (40-90)
5. Flag if score seems inconsistent with analysis

**Common Errors to Catch:**
- Forgetting to apply bonuses
- Double-counting skills in Match
- Web searching for compensation (forbidden!)
- Optimistic prep estimates (be conservative!)
- Location score wrong sign (Tel Aviv should be 0, not penalty)

## Usage Notes

### When to Override
These are guidelines. Override with justification if:
- Unique circumstances warrant
- Strong gut feeling contradicts formula
- Missing information makes formula unreliable

### Conservative Bias
When uncertain:
- Round scores DOWN (not up)
- Estimate prep time HIGH
- Assume MEDIUM stress (not low)
- Be realistic about match quality

### User Calibration
After 5-10 jobs analyzed:
- Review if scores align with user's interest
- Adjust weights if needed
- Update formulas in consultation with user

---

**Version:** 3.0
**Last Updated:** October 27, 2025
**Status:** Production
