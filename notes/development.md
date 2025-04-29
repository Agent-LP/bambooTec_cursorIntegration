# Development Notes

## Setup Instructions

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Development Tools**
   - VS Code with Python extension
   - Pylint for linting
   - Black for code formatting
   - pytest for testing

3. **Common Commands**
   ```bash
   # Run tests
   pytest tests/
   
   # Format code
   black .
   
   # Run linter
   pylint src/
   ```

## Debugging Tips

1. **Common Issues**
   - Type errors: Check Pydantic models
   - CLI formatting: Verify Rich usage
   - Task persistence: Memory management

2. **Testing Strategy**
   - Unit tests for core functionality
   - Integration tests for CLI
   - Mock external dependencies

3. **Performance Optimization**
   - Profile with cProfile
   - Monitor memory usage
   - Optimize data structures 