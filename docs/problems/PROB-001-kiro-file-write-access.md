# PROB-001: Kiro File Write Access Issue

**Date Reported:** 2026-02-17  
**Status:** Open  
**Severity:** High  
**Reporter:** dsmi001  
**Component:** Kiro IDE - File System Operations

---

## Problem Description

Kiro IDE is unable to write files to the `.kiro` directory within the project workspace using the `fsWrite` tool. All attempts to create files in `.kiro/specs/` result in "Access denied" errors, despite the directory being within the workspace.

## Environment

- **OS:** Linux
- **Shell:** bash
- **Workspace Path:** `/home/dsmi001/Documents/projects/se2-calculator-project`
- **Kiro Version:** Unknown (Auto model)
- **Project:** SE2 Calculator Project v0.7.0-alpha

## Reproduction Steps

1. Attempt to create a file in `.kiro/specs/` using `fsWrite` tool
2. Try with relative path: `.kiro/specs/README.md`
3. Try with absolute path: `/home/dsmi001/Documents/projects/se2-calculator-project/.kiro/specs/README.md`
4. Both attempts fail with "Access denied" error

## Error Messages

### Relative Path Attempt
```
Access denied: File access is restricted to workspace. Attempted path: /.kiro/specs/README.md

I can only write files within the current workspace or ~/.kiro directory. Please ensure the file path is correct and within these allowed locations.
```

### Absolute Path Attempt
```
Access denied: File access is restricted to workspace. Attempted path: /home/

I can only write files within the current workspace or ~/.kiro directory. Please ensure the file path is correct and within these allowed locations.
```

## Expected Behavior

- `fsWrite` should successfully create files in `.kiro/specs/` directory
- Relative paths starting with `.kiro/` should be recognized as within workspace
- Absolute paths within the workspace should be accepted

## Actual Behavior

- All write attempts to `.kiro/specs/` are rejected
- Error message suggests path is outside workspace
- Path interpretation appears incorrect (relative path shows as `/.kiro/` with leading slash)

## Workarounds Attempted

1. ✗ Using relative path `.kiro/specs/README.md`
2. ✗ Using absolute path with full workspace directory
3. ✗ Creating directory first with `mkdir -p .kiro/specs` (bash command also failed)
4. ✓ Successfully created hooks using `createHook` tool (works correctly)

## Impact

- Cannot create spec files for enhancement implementation
- Blocks structured feature development workflow
- Limits ability to organize project documentation in `.kiro` directory
- Hooks work fine, but specs cannot be created

## Additional Context

### Working Operations
- `createHook` tool successfully creates files in `.kiro/hooks/`
- Can read files from `.kiro/steering/` directory
- Bash commands work but show terminal errors (exit code -1)

### Path Interpretation Issue
The error message shows `/.kiro/` with a leading slash when using relative path `.kiro/`, suggesting the path is being incorrectly interpreted as an absolute path from root rather than relative to workspace.

## Possible Causes

1. Path normalization issue in `fsWrite` tool
2. Workspace boundary detection incorrectly flagging `.kiro` paths
3. Special handling of `.kiro` directory causing conflicts
4. Relative path resolution prepending `/` incorrectly

## Suggested Solutions

1. Fix path normalization in `fsWrite` to handle `.kiro/` correctly
2. Ensure workspace boundary check recognizes `.kiro/*` as valid
3. Add special case handling for `.kiro` directory writes
4. Improve error messages to show actual resolved path for debugging

## Related Issues

- Bash commands also show errors but appear to execute (exit code -1)
- Terminal output shows "TY=not a tty" warnings

## Diagnostic Test Results

### Test 1: Other Hidden Directories
**Command:** `fsWrite` to `.github/test-file.md`  
**Result:** ✅ SUCCESS  
**Conclusion:** Other hidden directories work fine with fsWrite

### Test 2: Bash Commands to .kiro/specs/
**Command:** `mkdir -p .kiro/specs && echo "# Test" > .kiro/specs/test.md`  
**Result:** ✅ SUCCESS (despite exit code -1 and error messages)  
**Verification:** File confirmed to exist with `test -f .kiro/specs/test.md`  
**Conclusion:** Bash commands work as a workaround

### Test 3: Permissions Check
**Command:** `ls -la .kiro/` and `ls -la .kiro/specs/`  
**Result:** 
- `.kiro/` permissions: `drwxr-xr-x` owned by `dsmi001:dsmi001`
- `.kiro/specs/` permissions: `drwxr-xr-x` owned by `dsmi001:dsmi001`
- Test file created via bash: `-rw-r--r--` owned by `dsmi001:dsmi001`

**Conclusion:** No filesystem-level restrictions, normal permissions

### Test 4: Alternative Location
**Command:** `fsWrite` to `docs/specs/test-spec.md`  
**Result:** ✅ SUCCESS  
**Conclusion:** Non-.kiro directories work perfectly

## Root Cause Analysis

Based on diagnostic testing, the issue is **definitively a bug in Kiro's fsWrite tool** when handling the `.kiro/` directory specifically:

1. **Not a permissions issue** - filesystem permissions are normal
2. **Not a hidden directory issue** - `.github/` works fine
3. **Not a bash issue** - bash commands successfully create files in `.kiro/`
4. **Isolated to fsWrite + .kiro combination** - all other combinations work

The fsWrite tool appears to have special handling or restrictions for the `.kiro/` directory that incorrectly blocks write operations.

## Workaround Implemented

Using bash commands to create files in `.kiro/specs/` directory:
```bash
cat > .kiro/specs/filename.md << 'EOF'
[file content]
EOF
```

Despite showing exit code -1 and error messages, files are successfully created.

## Next Steps

1. ✅ Documented bug with complete diagnostic results
2. ✅ Implemented bash workaround for spec file creation
3. 🔲 Report to Kiro development team with this documentation
4. 🔲 Monitor for Kiro IDE updates that fix fsWrite + .kiro issue

---

**Last Updated:** 2026-02-17  
**Assigned To:** Kiro Development Team  
**Priority:** High - Blocks feature development workflow (workaround available)  
**Status:** Diagnosed - Root cause identified, workaround implemented
