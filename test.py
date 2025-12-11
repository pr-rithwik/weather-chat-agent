# Run this in Python shell or create test.py
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("OPENWEATHER_API_KEY")

print(f"Key: {key}")
print(f"Length: {len(key) if key else 0}")
print(f"Repr: {repr(key)}")
```

**Expected output:**
```
Key: 564f34adfe88286b8ff23a619869fb21
Length: 32
Repr: '564f34adfe88286b8ff23a619869fb21'