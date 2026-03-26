# Singapore Job Market AI Impact Visualizer

## Summary Email

---

**Subject:** Singapore AI Job Impact Analysis - Interactive Visualization

Hi,

I've built an interactive visualization analyzing AI exposure across Singapore's job market. You can explore it here: **[YOUR GITHUB PAGES URL]**

### What It Shows

- **432 occupations** from Singapore Standard Occupational Classification (SSOC) 2024
- **2.31M workers** across all occupation categories (2024 data)
- AI exposure scores (0-10) for each occupation, with higher scores indicating greater potential impact
- Interactive treemap with filtering (view top 10-432 jobs) and multiple color modes

### Data Sources

1. **Occupations**: SSOC 2024 from Ministry of Manpower (MOM)
   - 433 detailed 5-digit occupation codes parsed from official PDF
   - Complete descriptions and classifications

2. **Employment**: MOM Resident Employment by Detailed Occupation 2024
   - 41 sub-major groups (2-digit SSOC codes) from `mrsd_69_Emp_Res_DetailedOcc_Sex.xlsx`
   - Distributed to 5-digit occupations using wage-weighted or statistical variation
   - Total: 2.31M workers (matches official 2024 resident workforce data)

3. **Wages**: MOM Occupational Wage Survey 2024
   - 201 occupations matched with median monthly wages (46.5% coverage)
   - Extracted from 6 MOM Excel files using fuzzy title matching
   - Average match confidence: 88.2%

4. **AI Exposure Scores**: OpenAI GPT-4o
   - Singapore-specific prompts considering local job characteristics
   - Scored on complementarity, substitutability, and exposure dimensions
   - Calibrated using local examples (hawkers, ministers, doctors, etc.)

### Key Findings

- **Average AI exposure**: 5.71/10 (job-weighted)
- **PME workers** (Professionals, Managers, Executives): 65.3% of workforce
- **PME AI exposure**: 5.80/10 (higher than overall average)
- **Wage coverage**: 201 occupations (46.5%) with salary data
- **Median monthly wage** (where available): $3,500
- Highest exposure: Data analysts, software developers, administrative roles
- Lowest exposure: Hands-on trades, personal care, food service workers

### Business Impact Interpretation

**1. Knowledge Workers Face Higher AI Disruption (65.3% of workforce)**

- PME roles—the backbone of Singapore's high-value economy—show AI exposure of 5.80/10, **above the overall average**
- These roles typically earn higher salaries and require years of education/training
- **Business implication**: Companies heavily reliant on PMEs (finance, tech, professional services) need proactive AI integration strategies now, not later
- **Talent strategy**: Traditional PME hiring may need to pivot toward "AI + Human" hybrid models

**2. The "Automation Paradox" - Cognitive Work More Exposed Than Physical Work**

- High-earning administrative, analytical, and professional roles show higher AI exposure
- Lower-paid hands-on work (hawkers, caregivers, tradespeople) shows lower exposure
- **Business implication**: Cost-saving automation may impact higher-paid roles first, inverting traditional automation patterns
- **Workforce planning**: Budget for reskilling programs for displaced high-skill workers, not just low-skill

**3. Mid-Tier Administrative Functions at Greatest Risk**

- Clerical support, data entry, basic customer service showing high exposure scores
- These roles often form the organizational "middle layer" supporting operations
- **Business implication**: 
  - Opportunity for 30-50% productivity gains through AI augmentation in next 2-3 years
  - Risk of middle-management compression as AI handles coordination tasks
- **Action item**: Pilot AI tools in these functions now to understand productivity curves and redeployment needs

**4. Service Excellence Becomes Human Competitive Advantage**

- Personal care, food service, hospitality show lower AI exposure despite Singapore's service economy focus
- Human touch, cultural nuance, and physical presence remain difficult to automate
- **Business implication**: Premium positioning through superior human service becomes more valuable as AI commoditizes knowledge work
- **Differentiation strategy**: Invest in training for empathy, cultural intelligence, and complex problem-solving that AI cannot replicate

**5. Singapore's Workforce Structure Creates Unique Challenges**

- 2.31M resident workers analyzed, but ~30% of workforce are non-residents (not in dataset)
- Non-resident workers often concentrated in construction, domestic work, lower-skill services (lower AI exposure)
- **Economic implication**: AI disruption may disproportionately affect resident Singaporeans in PME roles while leaving non-resident workforce less affected
- **Policy consideration**: Skills training and job transition programs need to focus on citizen/PR workforce

**6. Wage-Employment Relationship Inverted**

- Traditional automation targeted low-wage, repetitive work to reduce costs
- AI targets high-value cognitive tasks where wage premiums are highest
- **Business implication**: ROI calculations now favor automating $5K-$10K/month roles over low-wage positions
- **Productivity insight**: Companies can achieve same output with smaller, higher-skilled teams augmented by AI

**7. Immediate Action Areas for Singapore Businesses**

**Short-term (6-12 months):**
- Audit current workforce for high-exposure roles (data analysts, admin staff, junior professionals)
- Pilot AI productivity tools in these areas to measure impact
- Begin reskilling programs focusing on AI-collaboration skills

**Medium-term (1-2 years):**
- Restructure workflows to optimize human-AI collaboration
- Redesign job roles from "doer" to "supervisor of AI systems"
- Invest in roles showing lower AI exposure (complex problem-solving, physical services, creative strategy)

**Long-term (3-5 years):**
- Transform business models around AI-augmented operations
- Shift hiring strategy toward AI-literate talent across all levels
- Build competitive moats in areas where human judgment + AI creates unique value

**8. Sector-Specific Implications**

- **Financial Services**: High concentration of exposed roles (analysts, advisors). Early movers gain 2-3 year advantage
- **Professional Services**: Legal, consulting, accounting face significant augmentation. Billing models may need rethinking
- **Healthcare**: Mixed exposure—admin high, direct patient care low. Opportunity to redirect skilled healthcare workers from administration to patient care
- **Manufacturing**: Already highly automated. AI adds predictive maintenance, supply chain optimization
- **Retail/F&B**: Lower baseline exposure, but AI enables micro-personalization at scale

**9. The 5.71/10 Average Tells a Critical Story**

- This is **moderate-to-high** exposure, not existential replacement
- AI augments rather than replaces in most cases, but augmentation still means:
  - Same output with fewer people, OR
  - More output per person
- **Net result**: Workforce needs will shrink or shift, even if jobs aren't "eliminated"

**10. Competitive Advantage Window is Narrowing**

- Tools are becoming commoditized (ChatGPT, Claude, Copilot widely available)
- Competitive advantage comes from organizational change management, not technology access
- **Strategic insight**: Winners will be companies that reskill fastest and redesign workflows most effectively, not those with the most AI tools

### Limitations

1. **Wage Data Coverage**: Only 201 of 432 occupations (46.5%) have wage data from MOM files. Remaining occupations show as null due to:
   - MOM uses SSOC 2020, we use SSOC 2024 (matched by fuzzy title matching)
   - Some occupations not covered in MOM wage survey
   - Low-confidence matches filtered out (<60% similarity)

2. **Employment Distribution**: While based on accurate 2-digit SSOC totals (41 groups), distribution to 5-digit occupations (432 detailed jobs) uses:
   - Wage-weighted distribution for 201 occupations with wage data
   - Statistical modeling with random variation for remaining 231 occupations
   - Not actual occupation-level counts

3. **AI Scoring Subjectivity**: Scores generated by LLM based on occupation descriptions, not empirical studies. Represents informed estimates rather than measured impacts.

4. **Static Snapshot**: Data reflects 2024 employment structure. AI capabilities and job market evolve rapidly.

5. **Resident Workers Only**: Excludes non-resident workforce (approximately 30% of Singapore's total workforce).

### Technical Details

- **Pipeline**: Python scripts for data fetching, parsing, scoring, and aggregation
- **Visualization**: Vanilla JavaScript with Canvas-based squarified treemap algorithm
- **Architecture**: Full reproducible pipeline from raw data to interactive site
- **Repository**: [GitHub link will be added after deployment]

### Next Steps

Potential improvements:
- Increase wage coverage by manual mapping of difficult-to-match occupations
- Obtain actual occupation-level employment counts from MOM
- Add temporal dimension (track changes over time)
- Include non-resident workforce estimates
- Add occupation similarity search and career pathway suggestions
- Cross-validate AI exposure scores with Singapore-specific labor market research

---

**Explore the interactive visualization**: [YOUR GITHUB PAGES URL]

Let me know if you have questions or suggestions!

Best regards,
[Your name]
