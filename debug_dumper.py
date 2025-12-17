
import yaml
import sys
from src.generator import CustomDumper

# Load the generated OAS file to see what ended up in it? 
# No, wait, if I load the generated YAML, I will get the quoted string. 
# I want to simulate what the Generator has in memory.

# But I can load the generated YAML. If it loaded as a string with newlines, why did the dumper quote it?
# Let's try to reproduce it with a sample string found in the report.

sample_yaml = """
x-sandbox-response-body: |
  {
    "errors": [
      <#if validationErrors??>
        <#list validationErrors as error>
          {
            "dateTime": "2019-08-24T14:15:22Z",
            "code": "${error.code}",
            "description": "${error.message}"
          }<#if error?has_next>,</#if>
        </#list>
        <#else>
      {
        "dateTime": "2019-08-24T14:15:22Z", 
        "code":"E400", 
        "description": "Type mismatch"
      }
      </#if>
    ]
  }
"""

data = yaml.safe_load(sample_yaml)
print("Loaded Data Repr:")
print(repr(data['x-sandbox-response-body']))

print("\n--- DUMP with CustomDumper ---")
print(yaml.dump(data, Dumper=CustomDumper, sort_keys=False, allow_unicode=True, indent=2, width=float("inf")))

# Now getting the actual faulty value from the generated file if possible? 
# The user says "x-sandbox-response-body" has wrong formatting in the OUTPUT file.
# So I should check what the generated file actually contains.

try:
    with open("API Templates/generated/generated_oas_3.1.yaml", "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
    
    # Drill down to the specific path
    # root.paths./v1/accounts/assessments.post.x-sandbox-response-extension.400.Bad Request.x-sandbox-response-body
    
    path = "/v1/accounts/assessments"
    if path in content['paths'] and 'post' in content['paths'][path]:
        ext = content['paths'][path]['post'].get('x-sandbox-response-extension')
        if ext and '400' in ext and 'Bad Request' in ext['400']:
            val = ext['400']['Bad Request'].get('x-sandbox-response-body')
            print("\n--- ACTUAL VALUE FROM FILE ---")
            print(f"Type: {type(val)}")
            print(f"Repr: {repr(val)}")
            
            # TEST CLEANUP
            cleaned_lines = [line.rstrip() for line in val.split('\n')]
            cleaned_val = '\n'.join(cleaned_lines)
            
            print("\n--- DUMPING CLEANED VALUE ---")
            print(yaml.dump({'body': cleaned_val}, Dumper=CustomDumper, sort_keys=False, allow_unicode=True, indent=2, width=float("inf")))
            
            print("\n--- REDUMPING ACTUAL VALUE ---")
            print(yaml.dump({'body': val}, Dumper=CustomDumper, sort_keys=False, allow_unicode=True, indent=2, width=float("inf")))
            
            # Check for trailing spaces
            for i, line in enumerate(val.split('\n')):
                if line != line.rstrip():
                    print(f"Line {i} has trailing spaces! '{line}'")

except Exception as e:
    print(e)
