# In Progress Features

## 5. Replace Excel with Interactive HTML Database 🔄
**Status:** Ready for Implementation ✅  
**Priority:** High  
**Estimated Effort:** 5-8 hours

### Overview
Generate self-contained HTML file with interactive table using DataTables.js. Works everywhere: filesystem, Google Drive, mobile, offline.

### Features
- Sort, filter, search capabilities
- Export to Excel/CSV/PDF built-in
- Charts and statistics
- Responsive and mobile-friendly
- Read-only by design (YAML remains source of truth)

### Implementation Phases
1. **Phase 1:** Core HTML generator (2-3 hours)
2. **Phase 2:** Module integration (1-2 hours)
3. **Phase 3:** Enhanced features - charts, styling (1-2 hours)
4. **Phase 4:** Documentation and testing (1 hour)

### Benefits
- ✅ One unified flow (same file everywhere)
- ✅ Works on Claude Web (not just Desktop)
- ✅ No API setup needed (vs Google Sheets)
- ✅ Beautiful professional UI
- ✅ Self-contained (works offline)

### Migration Strategy
- **v9.2:** Generate both HTML + Excel (transition)
- **v9.3:** HTML primary, Excel optional
- **v10.0:** HTML only

### Documentation
See `docs/FEATURE_HTML_DATABASE.md` for full specification.

---

## 6. Add Donation Option in Git and Badges 📋
**Status:** Planning phase  
**Priority:** Medium  
**Estimated Effort:** 1-2 hours

### Qualifying Questions Needed
- Which donation platforms? (GitHub Sponsors, Ko-fi, Buy Me a Coffee, PayPal)
- Different tiers/rewards?
- README only or also CONTRIBUTING.md?
- Specific messaging about donations?

### Next Steps
- Answer qualifying questions
- Design donation strategy
- Add badges to README
- Setup donation platform accounts
