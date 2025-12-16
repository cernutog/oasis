# Project History - README

This folder contains comprehensive documentation for the OAS Generation Tool project. Use these documents to quickly onboard new developers or resume work after a break.

## Quick Start Guide

### For New Chat Sessions
When starting a new chat to continue work on this project, share these files:

1. **START HERE**: `PROJECT_OVERVIEW.md` - High-level project understanding
2. **REFERENCE**: `KEY_FILES.md` - Detailed file-by-file breakdown
3. **CONTEXT**: `IMPLEMENTATION_HISTORY.md` - Recent major changes and why decisions were made
4. **DETAILS**: `WALKTHROUGH.md` - Technical implementation walkthrough

### Document Purposes

#### PROJECT_OVERVIEW.md
- Project purpose and architecture
- Directory structure
- Key components overview
- Critical implementation details
- How to run the tool
- Common patterns used

#### KEY_FILES.md
- Detailed breakdown of each source file
- Important methods and their locations
- Excel template structure
- Configuration details

#### IMPLEMENTATION_HISTORY.md
- Complete history of custom extension formatting solution
- Evolution of approaches (what failed and why)
- Final solution with code examples
- Key insights and lessons learned

#### WALKTHROUGH.md
- Technical walkthrough of final implementation
- Code snippets and file references
- Verification results

## Project Status (as of 2025-12-16)

### ✅ Completed Features
- [x] Parse Excel templates to OAS YAML
- [x] Generate both OAS 3.0 and 3.1
- [x] Custom extension formatting with literal block style (`|`)
- [x] Preserve extension order from Excel source
- [x] Position extensions before responses in operations
- [x] Correct indentation (6 spaces at operation level)

### 🎯 Known Working Patterns
- Raw YAML insertion for custom extensions
- OrderedDict usage for key order preservation
- `.rstrip()` for leading whitespace preservation
- Post-processing YAML output to replace markers

### ⚠️ Important Gotchas
1. **Don't use `.strip()`** on raw extension text - use `.rstrip()` only
2. **Excel text has absolute indentation** - insert as-is, don't add indent
3. **`__RAW_EXTENSIONS__` marker** must be in extension ordering list
4. **Always use OrderedDict** for dictionaries that need order preservation

## Debugging Tips

### If Extensions Don't Appear
1. Check `parser.py` line 157 - is `"extensions"` field populated?
2. Check `generator.py` line 102 - does raw text get stored?
3. Search output YAML for `__RAW_EXTENSIONS__` - if present, post-processing failed

### If Indentation Wrong
1. Check raw Excel content - use debug to write to file
2. Verify `.rstrip()` not `.strip()` is used
3. Check post-processing doesn't add extra indent

### If Order Wrong
1. Check `generator.py` lines 140-150 - is `__RAW_EXTENSIONS__` in extensions list?
2. Verify no `sorted()` calls on extension keys
3. Check OrderedDict used everywhere

## Contact Points in Code

### To Modify Extension Handling
- `src/parser.py:157` - Reading from Excel
- `src/generator.py:99-103` - Storing raw text
- `src/generator.py:688-751` - Post-processing insertion

### To Modify Operation Structure
- `src/generator.py:140-150` - Key ordering
- `src/generator.py:698-727` - Section ordering in `get_yaml()`

### To Modify Schema Generation
- `src/schema_builder.py` - JSON Schema construction
- `src/generator.py` - Schema reference handling

## Version History

- **2025-12-16**: Custom extension formatting implementation completed
- **2025-12-15**: Raw YAML insertion approach designed
- **2025-12-12**: Initial analysis of extension formatting issues

## Next Steps / Future Enhancements

Potential improvements for future work:
- [ ] Add validation of generated OAS against OpenAPI spec
- [ ] Support for additional custom extension patterns
- [ ] Improve error handling and user feedback
- [ ] Add unit tests for critical functionality
- [ ] Consider GUI for easier template editing

## How to Use This Documentation

1. **Starting fresh?** Read PROJECT_OVERVIEW.md first
2. **Making changes?** Check KEY_FILES.md for exact file locations
3. **Debugging?** Review IMPLEMENTATION_HISTORY.md for gotchas  
4. **Need details?** WALKTHROUGH.md has code examples

## File Maintenance

Keep these documents updated when making significant changes:
- Add new sections to PROJECT_OVERVIEW.md for architectural changes
- Update KEY_FILES.md when adding/removing files or changing APIs
- Document new discoveries in IMPLEMENTATION_HISTORY.md
- Update WALKTHROUGH.md after major feature completions
