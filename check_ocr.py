#!/usr/bin/env python
"""
Quick diagnostic script to check OCR setup
"""

print("=" * 60)
print("OCR SYSTEM DIAGNOSTIC")
print("=" * 60)

# Check 1: Python version
import sys
print(f"\n1. Python Executable: {sys.executable}")
print(f"   Version: {sys.version}")

# Check 2: Pytesseract
print("\n2. Checking Pytesseract...")
try:
    import pytesseract
    print(f"   ✅ Pytesseract: INSTALLED")
    print(f"   Path: {pytesseract.__file__}")
except ImportError as e:
    print(f"   ❌ Pytesseract: NOT INSTALLED")
    print(f"   Error: {e}")

# Check 3: PIL/Pillow
print("\n3. Checking PIL (Image processing)...")
try:
    from PIL import Image
    print("   ✅ PIL/Pillow: INSTALLED")
except ImportError:
    print("   ❌ PIL/Pillow: NOT INSTALLED")

# Check 4: Tesseract binary
print("\n4. Checking Tesseract Binary...")
import shutil
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    print(f"   ✅ Tesseract Found: {tesseract_path}")
else:
    print(f"   ❌ Tesseract NOT FOUND in PATH")
    print(f"   Download: https://github.com/UB-Mannheim/tesseract/wiki")

# Check 5: Test OCR
print("\n5. Testing OCR capability...")
if 'pytesseract' in sys.modules and tesseract_path:
    try:
        from PIL import Image
        import pytesseract
        # Create a simple test image
        img = Image.new('RGB', (100, 30), color='white')
        result = pytesseract.image_to_string(img)
        print("   ✅ OCR Test: SUCCESS")
    except Exception as e:
        print(f"   ❌ OCR Test: FAILED - {e}")
else:
    print("   ⏳ Skipped (missing dependency)")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if 'pytesseract' in sys.modules and tesseract_path:
    print("✅ System is READY for OCR operations!")
    print("   Upload feature should work now!")
else:
    print("❌ OCR System INCOMPLETE")
    if 'pytesseract' not in sys.modules:
        print("   - Install pytesseract: pip install pytesseract")
    if not tesseract_path:
        print("   - Install Tesseract binary")
        print("     Download: https://github.com/UB-Mannheim/tesseract/wiki/Downloads-for-Windows")

print("=" * 60)
