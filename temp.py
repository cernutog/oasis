
def analyze_logs_errors():
    try:
        with open("debug_output.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        errors = [line.strip() for line in lines if "CRITICAL ERROR" in line]
        print(f"Found {len(errors)} CRITICAL ERROR logs:")
        for line in errors:
            print(line)
            
        # Also check normal logs
        tuples = [line.strip() for line in lines if "DEBUG SC: New Tuple" in line]
        print(f"Found {len(tuples)} New Tuple logs:")
        
        cols = [line.strip() for line in lines if "Collision: Registered" in line and "SearchCriteria" in line]
        print(f"Found {len(cols)} Collision logs for SearchCriteria:")
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    analyze_logs_errors()
