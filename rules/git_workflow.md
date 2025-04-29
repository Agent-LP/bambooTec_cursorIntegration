# Git Workflow Rules

1. **Branch Naming**
   - Feature branches: `feature/description`
   - Bug fixes: `fix/description`
   - Hotfixes: `hotfix/description`
   - Release branches: `release/version`

2. **Commit Messages**
   - Use present tense
   - Start with a capital letter
   - Be descriptive but concise
   - Follow the format:
     ```
     <type>(<scope>): <description>
     
     [optional body]
     [optional footer]
     ```
   - Types: feat, fix, docs, style, refactor, test, chore

3. **Pull Requests**
   - Create PRs for all changes
   - Include clear description
   - Link related issues
   - Request reviews from team members
   - Ensure all tests pass
   - Update documentation if needed

4. **Code Review**
   - Review within 24 hours
   - Provide constructive feedback
   - Check for:
     - Code quality
     - Test coverage
     - Documentation
     - Performance impact 