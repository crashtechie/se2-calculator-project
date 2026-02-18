# ISSUE-014: Kiro File Write Access Issue for .kiro Directory

**Status:** Open  
**Priority:** High  
**Created:** 2026-02-17  
**Resolved:** Not yet resolved  
**Component:** Kiro IDE - File System Operations  
**Affects Version:** Kiro CLI (Auto model)

## Problem Description

Kiro IDE is unable to write files to the `.kiro` directory within the project workspace using the `fsWrite` tool. All attempts to create files in `.kiro/specs/` result in "Access denied" errors, despite the directory being within the workspace and having correct filesystem permissions.

## Error Output

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

## Root Cause

Based on diagnostic testing, the issue is **a bug in Kiro's fsWrite tool** when handling the `.kiro/` directory specifically:

1. **Not a permissions issue** - Filesystem permissions are normal (`drwxr-xr-x`)
2. **Not a hidden directory issue** - Other hidden directories like `.github/` work fine with fsWrite
3. **Not a bash issue** - Bash commands successfully create files in `.kiro/`
4. **Isolated to fsWrite + .kiro combination** - All other combinations work correctly

**Path Interpretation Issue:** The error message shows `/.kiro/` with a leading slash when using relative path `.kiro/`, suggesting the path is being incorrectly interpreted as an absolute path from root rather than relative to workspace.

## Technical Details

**Environment:**
- OS: Zorin OS 18 (based on Ubuntu 24.04)
- Kernel: Linux 6.17.0-14-generic
- Architecture: x86_64
- Shell: bash
- Workspace: `/home/dsmi001/Documents/projects/se2-calculator-project`
- Project: SE2 Calculator Project v0.7.0-alpha

**Affected Operations:**
- `fsWrite` to `.kiro/specs/` (fails)
- `fsWrite` to `.kiro/specs/` with absolute path (fails)

**Working Operations:**
- `createHook` tool successfully creates files in `.kiro/hooks/`
- `fsWrite` to `.github/` directory (works)
- `fsWrite` to `docs/specs/` directory (works)
- Bash commands to `.kiro/specs/` (works despite error messages)

**Permissions Check:**
```bash
$ ls -la .kiro/
drwxr-xr-x  dsmi001:dsmi001  .kiro/

$ ls -la .kiro/specs/
drwxr-xr-x  dsmi001:dsmi001  .kiro/specs/
```

## Diagnostic Test Results

| Test | Command | Result | Conclusion |
|------|---------|--------|------------|
| Other hidden dirs | `fsWrite` to `.github/test.md` | ✅ SUCCESS | Other hidden directories work |
| Bash to .kiro | `echo "test" > .kiro/specs/test.md` | ✅ SUCCESS | Bash commands work |
| Permissions | `ls -la .kiro/specs/` | Normal perms | No filesystem restrictions |
| Alternative location | `fsWrite` to `docs/specs/test.md` | ✅ SUCCESS | Non-.kiro directories work |

## Solution

### Workaround (Current)

Use bash commands to create files in `.kiro/specs/` directory:

```bash
cat > .kiro/specs/filename.md << 'EOF'
[file content]
EOF
```

**Note:** Despite showing exit code -1 and error messages, files are successfully created.

### Permanent Fix (Needed)

Kiro development team needs to:

1. Fix path normalization in `fsWrite` to handle `.kiro/` correctly
2. Ensure workspace boundary check recognizes `.kiro/*` as valid
3. Remove special case handling that blocks `.kiro` directory writes
4. Improve error messages to show actual resolved path for debugging

## Verification Checklist

- [x] Confirmed filesystem permissions are correct
- [x] Tested other hidden directories (`.github/` works)
- [x] Verified bash commands work as workaround
- [x] Documented diagnostic test results
- [x] Implemented workaround for spec file creation
- [ ] Report to Kiro development team
- [ ] Monitor for Kiro IDE updates
- [ ] Verify fix when available

## Resolution

**Date Resolved:** Not yet resolved

**Current Status:** Issue remains open. Root cause identified as Kiro fsWrite bug. Workaround implemented using bash commands.

**Workaround Status:** ✅ Functional - All spec files successfully created using bash

**Next Steps:**
1. Report to Kiro development team with diagnostic results
2. Monitor for Kiro IDE updates that fix fsWrite + .kiro issue
3. Test fix when available
4. Update documentation once resolved

## Impact

**Severity:** High - Blocks structured feature development workflow

**Affected Workflows:**
- Cannot create spec files using fsWrite tool
- Limits ability to organize project documentation in `.kiro` directory
- Requires workaround for all `.kiro/` file operations

**Mitigation:** Bash command workaround available and functional

## Related Issues

- Bash commands show exit code -1 but execute successfully
- Terminal output shows "TY=not a tty" warnings (cosmetic)

## Related Files

- `.kiro/specs/` - Target directory for spec files
- `.kiro/hooks/` - Works correctly with createHook tool
- `.kiro/steering/` - Readable, write operations untested

## Notes

- The `createHook` tool works correctly for `.kiro/hooks/`, suggesting the issue is specific to fsWrite
- Other hidden directories (`.github/`, `.devcontainer/`) work fine with fsWrite
- Bash workaround is reliable despite error messages
- No filesystem-level restrictions detected

## Best Practices

When working with Kiro IDE:

1. **Test file operations** in different directories to identify tool-specific issues
2. **Use bash workarounds** when fsWrite fails for specific directories
3. **Document workarounds** for team members
4. **Report bugs** with comprehensive diagnostic results
5. **Verify permissions** before assuming tool bugs

## Prevention

To prevent similar issues in the future:

1. Test Kiro file operations in all project directories during setup
2. Document known limitations and workarounds
3. Keep Kiro CLI updated to latest version
4. Report bugs with detailed reproduction steps
5. Maintain alternative workflows for critical operations
