# arkUtil

Common utility functions for Python and Javascript

To Do:
- [ ] move javascript ui stuff to coren.ui
- [ ] better test coverage



## Refactor Changes
### Renamed
- clientTest > clientOnly - more generic
- serverTest > serverOnly - more generic
- utcTime > utcNow - clearer
- createHash > randomHash - in line w/ python
- joinURL > joinUrl - just feels right ya dig?

### Moved
- getExtension - duplicated in cOS, belongs there
- normalizeExtension - duplicated in cOS, belongs there
- removeExtension - duplicated in cOS, belongs there
- ensureExtension - duplicated in cOS, belongs there
- loadLazyImages - duplicated in coren.ui
- getSiteRoot - doesn't belong in helpers
- getArgs - moved to cOS

### Removed
- defaultStringReplace - not needed post Caretaker 2
- defaultStringInsert - not needed post Caretaker 2
- uriReplace - only used w/in arkUtil once
- dictToAndFrom - antipattern
- callbackError - unused, makes no sense
- removeClass - moved to UI
- addClass - moved to UI
- getCSS - moved to UI
- copyCSS - moved to UI
- cloneWithCSS - moved to UI
- wrapWithEmptyParents - moved to UI
- cloneWithEmptyParents - moved to UI
- setLastArray - moved to UI
- stopBubble - moved to UI
- isJQuery - moved to UI
- isJQueryEvent - moved to UI
- setDataAndAttribute - moved to UI
- removeDataAndAttribute - moved to UI
