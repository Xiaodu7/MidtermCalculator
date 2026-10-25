
# Enhanced Calculator Command-Line Application

## Project Description

This is my IS601 Midterm Project. The goal of this project is to build a Python command-line calculator with basic and advanced arithmetic operations.

The calculator supports calculation history, undo and redo, logging, CSV file storage, and input validation. It also uses several design patterns, including Factory, Memento, and Observer.

I also added color-coded outputs to make the command-line interface easier to use.

## Features

- Basic operations: addition, subtraction, multiplication, and division
- Advanced operations: power, root, modulus, integer division, percentage, and absolute difference
- Command-line interface (REPL)
- Calculation history
- Undo and redo
- Automatic logging
- Automatic and manual CSV saving
- Loading calculation history from CSV
- Configuration using environment variables
- Input validation and error handling
- Color-coded terminal outputs
- Unit testing with pytest
- Continuous Integration using GitHub Actions

## Technologies Used

- Python 3.14
- pytest
- pytest-cov
- pandas
- python-dotenv
- colorama
- Git and GitHub
- GitHub Actions

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd MidtermCalculator
```

Replace `<YOUR_REPOSITORY_URL>` with the actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate the virtual environment on Linux or WSL:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example configuration file:

```bash
cp .env.example .env
```

The `.env` file contains settings for logging, history management, and calculations.

## Configuration

The application uses `python-dotenv` to load settings from `.env`.

Example configuration:

```env
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_LOG_FILE=logs/calculator.log
CALCULATOR_HISTORY_FILE=history/calculations.csv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

These settings control where files are saved, the maximum history size, whether automatic saving is enabled, calculation precision, and input limits.

Default values are provided if settings are missing.

## Running the Calculator

Start the application with:

```bash
python main.py
```

The calculator will display:

```text
Enhanced Calculator
Type 'help' for commands.
Calculator>
```

You can then enter commands directly.

### Arithmetic Commands

| Command | Description | Example |
|---|---|---|
| add | Addition | add 5 3 |
| subtract | Subtraction | subtract 10 3 |
| multiply | Multiplication | multiply 4 2 |
| divide | Division | divide 10 2 |
| power | Exponentiation | power 2 3 |
| root | Nth root | root 27 3 |
| modulus | Remainder | modulus 10 3 |
| int_divide | Integer division | int_divide 10 3 |
| percent | Percentage | percent 25 100 |
| abs_diff | Absolute difference | abs_diff 5 10 |

Each arithmetic operation takes two numbers.

### Other Commands

| Command | Description |
|---|---|
| history | Display calculation history |
| clear | Clear calculation history |
| undo | Undo the last history change |
| redo | Restore the last undone change |
| save | Manually save history to CSV |
| load | Load history from CSV |
| help | Display available commands |
| exit | Exit the calculator |

## Example Usage

```text
Calculator> add 5 3
Result: 8

Calculator> multiply 4 2
Result: 8

Calculator> history
1. add 5 3 = 8
2. multiply 4 2 = 8

Calculator> undo
Undo successful.

Calculator> redo
Redo successful.

Calculator> save
History saved to: history/calculations.csv

Calculator> exit
Goodbye!
```

The actual save message displays the configured file path.

## Design Patterns

### Factory Pattern

The Factory Pattern is used in `calculation.py`.

`CalculationFactory` selects the correct operation based on the user's command and creates a Calculation object.

### Memento Pattern

The Memento Pattern is used to manage calculation history.

`CalculatorMemento` saves previous history states so users can undo or redo changes.

### Observer Pattern

The Observer Pattern automatically responds to new calculations.

- `LoggingObserver` records calculation details in a log file.
- `AutoSaveObserver` saves the updated calculation history to CSV when auto-save is enabled.

These patterns help organize the application into separate components.

## History and CSV Storage

Calculation history is managed by `CalculationHistory`.

The application uses pandas to save and load history in CSV format.

The CSV file contains:

- operation
- operands
- result
- timestamp

When automatic saving is enabled, the history file is updated after calculations and history changes.

When automatic saving is disabled, users can save history manually using the `save` command.

The `load` command reads the saved CSV file.

## Logging

Python's logging module is used to record important events.

The application uses different logging levels:

- INFO: Successful calculations and normal events
- WARNING: Invalid commands or rejected calculations
- ERROR: Certain application and storage errors

By default, logs are saved in:

```text
logs/calculator.log
```

The location can be changed using the `.env` file.

## Error Handling

The application includes input validation and custom exceptions.

Some examples include:

- Division by zero
- Invalid numerical inputs
- Unsupported operations
- Inputs exceeding the configured maximum
- Missing or invalid CSV files
- Invalid configuration values

The REPL displays error messages so users can correct their input without restarting the application.

## Color-Coded Outputs

I added color-coded outputs using `colorama` as an optional feature.

- Green: Successful calculation results
- Red: Error messages
- Yellow: Undo, redo, and other status messages
- Cyan: Help menu heading

This makes the terminal output easier to read.

## Unit Testing

The project uses pytest for unit testing.

Run all tests:

```bash
python -m pytest tests/ -v
```

Check test coverage:

```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

Enforce the required 90% coverage:

```bash
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=90
```

The tests cover arithmetic operations, design patterns, history management, configuration, logging, CSV storage, input validation, and the REPL.

The current local test results are:

- 142 tests passed
- 96.33% code coverage

These results were measured locally before final submission.

## Continuous Integration

GitHub Actions is used to run automated tests.

The workflow is defined in:

```text
.github/workflows/python-app.yml
```

It runs when code is pushed to the main branch or when a pull request targets main.

The workflow:

1. Checks out the repository
2. Sets up Python
3. Installs project dependencies
4. Runs pytest
5. Fails if test coverage is below 90%

This helps verify that new changes do not break the calculator.

## Project Structure

```text
MidtermCalculator/
├── app/
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── history_storage.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── observers.py
│   ├── operations.py
│   └── repl.py
├── tests/
│   ├── __init__.py
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_config.py
│   ├── test_history.py
│   ├── test_history_storage.py
│   ├── test_logger.py
│   ├── test_operations.py
│   └── test_repl.py
├── .github/
│   └── workflows/
│       └── python-app.yml
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Conclusion

Through this project, I practiced building a larger Python application by connecting several smaller modules.

I also learned more about design patterns, automated testing, error handling, logging, and GitHub Actions.

One important part of this project was learning how to organize different features while keeping the code readable and testable.
