"""
Check what the actual Spectral output looks like for operation-tags warnings.
We need to see the exact path format to understand why GUI resolution fails.
"""

# The issue is:
# - Spectral reports: "paths > /vop/v1/payee-information > post"
# - GUI converts to: "paths./vop/v1/payee-information.post"
# - Source map has:
#   - "paths./vop/v1/payee-information.post" -> operation file (fallback)
#   - "paths./vop/v1/payee-information.post.tags" -> $index.xlsx, Paths
#
# But the GUI lookup stops at the first match (the operation fallback),
# so it never reaches the .tags entry!

# The problem is in the FALLBACK registration at line 280 of generator.py:
# self._record_source(f"paths.{path_url}.{method}", file_ref, root_sheet)
#
# This creates a catch-all that prevents more specific paths from being found.

print("PROBLEM IDENTIFIED:")
print("==================")
print()
print("The fallback registration for operation root path is too broad.")
print("It matches before the specific .tags path can be found.")
print()
print("SOLUTION:")
print("=========")
print("Remove or modify the fallback registration to not interfere with")
print("specific sub-paths like .tags, .summary, .description, etc.")
print()
print("The GUI resolution algorithm stops at the FIRST match while")
print("traversing UP the path hierarchy. So if we have:")
print("  - paths./vop/v1/payee-information.post.tags -> $index.xlsx, Paths")
print("  - paths./vop/v1/payee-information.post -> operation file")
print()
print("And Spectral reports: 'paths > /vop/v1/payee-information > post'")
print("The GUI will:")
print("  1. Try: paths./vop/v1/payee-information.post -> MATCH! (operation file)")
print("  2. Stop searching")
print()
print("It never tries paths./vop/v1/payee-information.post.tags because")
print("it already found a match at the parent level.")
