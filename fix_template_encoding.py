# -*- coding: utf-8 -*-
"""
Script to fix UTF-8 encoding issues in MessageTemplate table
Run this AFTER ensuring the database connection is UTF-8

Usage:
    python manage.py shell < fix_template_encoding.py
"""

from core.models import MessageTemplate

def fix_latin1_to_utf8(text):
    """Convert latin1/ISO-8859-1 encoded text back to proper UTF-8"""
    if not text:
        return text
    
    try:
        # Try to encode as latin1 and decode as utf-8
        # This fixes double-encoded text like "Ã©" → "é"
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If that fails, return original
        return text


def fix_message_templates():
    """Fix all message templates with encoding issues"""
    
    print("🔍 Scanning MessageTemplates for encoding issues...")
    
    fixed_count = 0
    templates = MessageTemplate.objects.all()
    
    for template in templates:
        original_subject = template.subject
        original_body = template.body
        
        # Fix subject
        template.subject = fix_latin1_to_utf8(template.subject)
        
        # Fix body
        template.body = fix_latin1_to_utf8(template.body)
        
        # Check if anything changed
        if template.subject != original_subject or template.body != original_body:
            template.save()
            fixed_count += 1
            print(f"✅ Fixed template #{template.id}: {template.name}")
            print(f"   Subject before: {original_subject[:50]}")
            print(f"   Subject after:  {template.subject[:50]}")
            print()
    
    print(f"\n{'='*60}")
    print(f"✅ REPAIR COMPLETE!")
    print(f"   Templates scanned: {templates.count()}")
    print(f"   Templates fixed:   {fixed_count}")
    print(f"{'='*60}\n")
    
    # Show examples
    print("📋 Examples of fixed templates:")
    print()
    
    fr_templates = MessageTemplate.objects.filter(language='fr', is_default=True)
    for t in fr_templates[:3]:
        print(f"📄 {t.name} ({t.stage})")
        print(f"   Subject: {t.subject[:80]}")
        print(f"   Body preview: {t.body[:100]}...")
        print()


if __name__ == "__main__":
    fix_message_templates()
