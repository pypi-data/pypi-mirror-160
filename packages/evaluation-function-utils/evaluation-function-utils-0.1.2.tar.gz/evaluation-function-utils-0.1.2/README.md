# Evaluation Function Utilities

Python package containing a range of utilities that might be used by some (but not all) evaluation functions on the LambdaFeedback platform. This package is pre-installed on the [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer), to be utilised by individual functions to carry a range of common tasks:

- Better error reporting
- Schema checking
- Input symbols (multiple ways of inputing the same answer)

## Testing
Run tests from the root dir with:
```bash
pytest
```

*Useful flags:*
- **-vv**: verbose output
- **-rP**: show captured output of passed tests
- **-rx**: show captured output of failed tests