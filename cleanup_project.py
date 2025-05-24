#!/usr/bin/env python3
"""
Project Cleanup Script - IAB Toolkit
Removes unused files while preserving the current working simplified system.
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up unused files from the IAB toolkit project."""
    
    print("🧹 IAB TOOLKIT PROJECT CLEANUP")
    print("=" * 50)
    print("This script will remove unused files while preserving your working system.")
    print()
    
    # Files to keep (essential for current system)
    essential_files = {
        # Main system
        'enhanced_hybrid_classifier_v2.py',  # Your current working classifier
        
        # Test scripts (current)
        'test_simplified_with_json.py',      # Main JSON test script
        'test_individual_json.py',           # Individual JSON testing
        'test_simplified_system.py',         # Console testing
        
        # Japanese test data
        'japanese_text_sample.txt',          # Automotive
        'japanese_beauty_sample.txt',        # Beauty
        'japanese_business_sample.txt',      # Business
        'japanese_health_sample.txt',        # Health
        'japanese_technology_sample.txt',    # Technology
        
        # Configuration and data
        'Content Taxonomy 3.1.tsv',         # IAB taxonomy
        'pyproject.toml',                    # Project config
        'README.md',                         # Documentation
        
        # Latest completion documentation
        'JSON_OUTPUT_COMPLETE.md',           # Your latest completion
        'SIMPLIFIED_SYSTEM_COMPLETE.md',     # Simplified system docs
        
        # Latest JSON results (keep one recent one)
        'simplified_classification_results_20250524_004846.json',  # Most recent
        'individual_test_result.json',       # Individual test result
        'sample_json_structure.json',        # Sample structure
    }
    
    # Essential directories to keep
    essential_dirs = {
        'iab_toolkit',        # Core toolkit
        'iab_toolkit.egg-info',  # Package info
        '__pycache__',        # Python cache
        'examples',           # Examples
        'tests',              # Tests
        'scripts',            # Build scripts
    }
    
    # Files to remove (old/obsolete versions)
    files_to_remove = [
        # Old classifier versions
        'enhanced_hybrid_classifier.py',
        'hybrid_classifier_v2.py', 
        'hybrid_classifier.py',
        
        # Old test scripts
        'test_enhanced_system.py',
        'test_japanese_comprehensive.py',
        'test_japanese_samples.py',
        'test_japanese.py',
        'test_compact_formats.py',
        'test_edge_cases.py',
        'demo_hybrid_improvement.py',
        'final_demonstration.py',
        'quick_test.py',
        'test_script.py',
        
        # Old CLI tools
        'cli.py',
        
        # Development tools (not needed for current system)
        'show_taxonomy_subset.py',
        'simple_build_vectors.py',
        
        # Old documentation/summaries (keep only latest)
        'ENHANCED_SYSTEM_COMPLETE.md',
        'HYBRID_CLASSIFICATION_COMPLETE.md',
        'REQUIREMENTS_COMPLETE.md',
        'COMPLETION_SUMMARY.md',
        
        # Old result files
        'simplified_classification_results_20250524_004239.json',
        'simplified_classification_results_20250524_004652.json',
        'results.csv',
        'results.json',
        'test_results.json',
        'sample_urls.txt',
    ]
    
    # Count files before cleanup
    total_files_before = sum(len(files) for _, _, files in os.walk('.'))
    
    # Create backup directory
    backup_dir = Path('backup_removed_files')
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir()
    
    print("📁 Creating backup of removed files...")
    
    removed_count = 0
    
    # Remove files
    for file_to_remove in files_to_remove:
        file_path = Path(file_to_remove)
        if file_path.exists():
            print(f"   Removing: {file_to_remove}")
            # Backup before removing
            shutil.copy2(file_path, backup_dir / file_to_remove)
            file_path.unlink()
            removed_count += 1
        else:
            print(f"   Not found: {file_to_remove}")
    
    # Count files after cleanup
    total_files_after = sum(len(files) for _, _, files in os.walk('.'))
    
    print()
    print("✅ CLEANUP COMPLETE")
    print("=" * 50)
    print(f"📊 Files before cleanup: {total_files_before}")
    print(f"📊 Files after cleanup: {total_files_after}")
    print(f"🗑️  Files removed: {removed_count}")
    print(f"💾 Backup created: {backup_dir}")
    print()
    print("🎯 ESSENTIAL FILES PRESERVED:")
    print("=" * 30)
    
    # Show what's kept
    current_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    essential_found = [f for f in current_files if f in essential_files]
    
    for category, files in [
        ("📋 Main System", ['enhanced_hybrid_classifier_v2.py']),
        ("🧪 Test Scripts", ['test_simplified_with_json.py', 'test_individual_json.py', 'test_simplified_system.py']),
        ("📄 Japanese Samples", [f for f in essential_found if f.startswith('japanese_')]),
        ("⚙️  Configuration", ['pyproject.toml', 'Content Taxonomy 3.1.tsv']),
        ("📚 Documentation", ['README.md', 'JSON_OUTPUT_COMPLETE.md', 'SIMPLIFIED_SYSTEM_COMPLETE.md']),
        ("📊 Latest Results", [f for f in essential_found if f.endswith('.json')])
    ]:
        print(f"\n{category}:")
        for file in files:
            if file in essential_found:
                print(f"   ✅ {file}")
    
    print()
    print("🔧 DIRECTORIES PRESERVED:")
    current_dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    for dir_name in essential_dirs:
        if dir_name in current_dirs:
            print(f"   📁 {dir_name}/")
    
    print()
    print("🎉 Your simplified IAB classification system with JSON output is ready!")
    print("🚀 Run: python test_simplified_with_json.py")

if __name__ == "__main__":
    # Change to project directory
    os.chdir(Path(__file__).parent)
    cleanup_project()
