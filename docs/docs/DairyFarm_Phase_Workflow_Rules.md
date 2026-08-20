# DairyFarm — Phase Execution Rules

## Standard Workflow

```text
Read specification
↓
Inspect actual project
↓
Analyze files
↓
Identify dependencies
↓
Map to syllabus
↓
Plan
↓
Implement one small step
↓
Test
↓
Verify
↓
Continue
↓
Full regression
↓
Git review
↓
Commit
↓
Clean checkpoint
```

## Before Modifying Any File
1. Read it.
2. Understand its responsibility.
3. Check imports/dependencies.
4. Identify existing behavior.
5. Make the smallest required change.

## VS Code / PowerShell Workflow
For a new directory, provide an exact PowerShell command.

For a new file, provide an exact PowerShell command.

After each implementation step:
- provide the run command
- provide expected output
- stop for the user's result

## Failure Rule

```text
STOP
↓
Diagnose
↓
Explain root cause
↓
Fix
↓
Retest
↓
Verify
```

## Git
At checkpoints:

```powershell
git status
git diff --stat
```

After successful verification:

```powershell
git add .
git commit -m "<phase-specific message>"
git status
```

Never commit `.env`, passwords, database credentials, API keys, or secrets.
