"""
Installation Verification Script
Checks if all required components are properly installed
"""
import sys
import importlib
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need Python 3.8+)")
        return False


def check_packages():
    """Check required packages"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        ("fastapi", "FastAPI framework"),
        ("uvicorn", "ASGI server"),
        ("sqlalchemy", "Database ORM"),
        ("pydantic", "Data validation"),
        ("jose", "JWT authentication"),
        ("passlib", "Password hashing"),
        ("sentence_transformers", "RAG embeddings"),
        ("chromadb", "Vector database"),
    ]
    
    all_installed = True
    
    for package, description in required_packages:
        try:
            importlib.import_module(package.replace("-", "_"))
            print(f"   ✅ {package:25} - {description}")
        except ImportError:
            print(f"   ❌ {package:25} - {description} (NOT INSTALLED)")
            all_installed = False
    
    return all_installed


def check_files():
    """Check required files"""
    print("\n📁 Checking required files...")
    
    required_files = [
        "main.py",
        "agents.py",
        "rag_system.py",
        "database.py",
        "models.py",
        "schemas.py",
        "auth.py",
        "config.py",
        "knowledge_base.json",
        "requirements.txt",
        ".env.example",
    ]
    
    all_present = True
    
    for filename in required_files:
        if Path(filename).exists():
            print(f"   ✅ {filename}")
        else:
            print(f"   ❌ {filename} (MISSING)")
            all_present = False
    
    return all_present


def check_directories():
    """Check required directories"""
    print("\n📂 Checking required directories...")
    
    required_dirs = [
        "templates",
        "static",
    ]
    
    all_present = True
    
    for dirname in required_dirs:
        if Path(dirname).is_dir():
            # Count files in directory
            files = list(Path(dirname).rglob("*.*"))
            print(f"   ✅ {dirname}/ ({len(files)} files)")
        else:
            print(f"   ❌ {dirname}/ (MISSING)")
            all_present = False
    
    return all_present


def check_env_file():
    """Check .env file"""
    print("\n⚙️  Checking configuration...")
    
    if Path(".env").exists():
        print("   ✅ .env file exists")
        return True
    else:
        print("   ⚠️  .env file not found")
        print("   ℹ️  Copy .env.example to .env and update settings")
        print("   Command: cp .env.example .env")
        return False


def main():
    """Main verification function"""
    print("="*70)
    print("INSTALLATION VERIFICATION")
    print("Agentic AI IT Support System")
    print("="*70)
    
    results = []
    
    # Run checks
    results.append(("Python Version", check_python_version()))
    results.append(("Required Packages", check_packages()))
    results.append(("Required Files", check_files()))
    results.append(("Required Directories", check_directories()))
    results.append(("Environment Config", check_env_file()))
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70 + "\n")
    
    all_passed = all(result[1] for result in results)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} - {check_name}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("="*70 + "\n")
        print("🚀 You're ready to run the application!")
        print("\nStart the application with:")
        print("  python main.py")
        print("\nOr use:")
        print("  run.bat    (Windows)")
        print("  ./run.sh   (Linux/Mac)")
        print("\nThen access:")
        print("  http://localhost:8000        - Main interface")
        print("  http://localhost:8000/docs   - API documentation")
        print("\nDefault login: admin / admin123")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("="*70 + "\n")
        print("Please fix the issues above before running the application.")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nTo create .env file:")
        print("  cp .env.example .env")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
