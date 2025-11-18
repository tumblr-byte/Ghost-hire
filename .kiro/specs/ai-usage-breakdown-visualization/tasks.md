# Implementation Plan

- [x] 1. Create AI Usage Categorizer module







  - Create `haunted_profiles/ai_usage_categorizer.py` with AIUsageCategorizer class
  - Implement `categorize_by_task_type()` method to categorize code into task types (core_algorithms, api_integration, ui_ux, documentation, boilerplate)
  - Implement `identify_core_vs_supporting()` method to separate core skills from supporting tasks based on user profile
  - Use user's `expertise_area`, `core_skills`, and `weaknesses` fields to determine what is core vs supporting
  - _Requirements: 1.1, 1.2, 1.3_





- [ ] 2. Create Breakdown Calculator module
  - Create `haunted_profiles/breakdown_calculator.py` with BreakdownCalculator class
  - Implement `calculate_category_breakdown()` method to calculate AI% for each category with status (excellent/good/smart/needs_improvement)
  - Implement `calculate_self_awareness_score()` method to reward developers who are honest about their AI usage


  - Generate context-aware messages for each category based on whether it's core or supporting
  - _Requirements: 1.4, 3.1, 3.2, 3.3_

- [ ] 3. Create Visualization Generator module
  - Create `haunted_profiles/visualization_generator.py` with VisualizationGenerator class


  - Implement `generate_stacked_bar_data()` method for chart data (Core Skills vs Supporting Tasks)
  - Implement `generate_category_cards()` method to create visual cards for each category with icons, colors, and messages
  - Implement `generate_employer_summary()` method to create employer-friendly summary highlighting core skills
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 4.1, 4.2, 4.3_



- [ ] 4. Create Messaging Engine module
  - Create `haunted_profiles/messaging_engine.py` with MessagingEngine class
  - Implement `generate_motivational_message()` method to create main encouraging message
  - Implement `generate_category_messages()` method to create positive messages for each category
  - Implement `generate_improvement_suggestions()` method to provide actionable recommendations prioritizing core skills


  - _Requirements: 3.4, 5.1, 5.2, 5.3, 5.4_

- [ ] 5. Integrate breakdown calculation into portfolio analysis
  - Update `haunted_profiles/portfolio_analyzer.py` `analyze_full_portfolio()` function
  - Import and instantiate AIUsageCategorizer, BreakdownCalculator, VisualizationGenerator, and MessagingEngine
  - Add `ai_usage_breakdown` field to portfolio_data with all breakdown information

  - Ensure backward compatibility for portfolios without detailed user profiles
  - _Requirements: 1.1, 1.5_

- [ ] 6. Update portfolio template with breakdown visualization
  - Update `templates/haunted_portfolio.html` to display the new AI usage breakdown
  - Replace single AI% display with Core vs Supporting breakdown

  - Add stacked bar visualization showing Core Skills (90% Human) vs Supporting Tasks (80% AI)
  - Add category cards for each task type with icons, percentages, examples, and messages
  - Add "Smart AI User" badge and motivational message at the top
  - _Requirements: 1.5, 2.1, 2.5, 3.2_


- [ ] 7. Add Employer View section to portfolio
  - Add new section in `templates/haunted_portfolio.html` for employer-friendly summary
  - Display headline emphasizing core skill independence (e.g., "Writes Core Algorithms Independently")
  - Show key points highlighting technical depth and strategic AI usage
  - Include specific examples of complex work done without AI assistance
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_



- [ ] 8. Add Self-Awareness badge and scoring
  - Display Self-Awareness Score in portfolio when user provides detailed AI usage context
  - Show "✅ Self-Aware Developer" badge for developers who are honest about weaknesses
  - Add tooltip or explanation of what self-awareness means in this context
  - _Requirements: 3.1, 3.2, 3.5_

- [ ] 9. Style the breakdown visualization with motivating design
  - Add CSS for category cards with appropriate colors (green for excellent, purple for smart)
  - Style stacked bar charts with neon green (human) and neon purple (AI) colors
  - Add icons and visual indicators (🔥 for core skills, ✅ for smart AI usage)
  - Ensure mobile-responsive design with stacked cards on small screens
  - _Requirements: 1.5, 2.5_

- [ ] 10. Add improvement suggestions section
  - Display actionable recommendations based on category breakdown
  - Prioritize core skill improvements over supporting task improvements
  - Show positive reinforcement for areas where developer is doing well
  - Include specific exercises or projects for areas needing improvement
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 11. Add AI usage trend tracking (optional future enhancement)
  - Store historical portfolio_data snapshots with timestamps
  - Calculate trend showing AI usage changes over time for core vs supporting
  - Display trend chart showing improvement in core skill independence
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
