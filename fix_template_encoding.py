# -*- coding: utf-8 -*-
"""
Script to fix UTF-8 encoding issues in MessageTemplate table
Run this AFTER ensuring the database connection is UTF-8

Usage:
    python manage.py shell < fix_template_encoding.py
"""

from core.models import MessageTemplate


def fix_text(text):
    """Fix common UTF-8 corruption patterns"""
    if not text:
        return text
    
    # Direct character replacements for known corruption patterns
    replacements = {
        'âœ…': '✅',
        'â‚¬': '€',
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ã ': 'à',
        'Ã¹': 'ù',
        'Ã¢': 'â',
        'Ãª': 'ê',
        'Ã®': 'î',
        'Ã´': 'ô',
        'Ã»': 'û',
        'Ã«': 'ë',
        'Ã¯': 'ï',
        'Ã¼': 'ü',
        'Ã§': 'ç',
        'Ã': 'À',
        'Ãˆ': 'È',
        'Ã‰': 'É',
        'Ã™': 'Ù',
        'ÃŠ': 'Ê',
        'ÃŽ': 'Î',
        'Ã”': 'Ô',
        'Ã›': 'Û',
        'Ã‹': 'Ë',
        'Ã': 'Ï',
        'Ãœ': 'Ü',
        'Ã‡': 'Ç',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text


def fix_message_templates():
    """Fix all message templates with encoding issues"""
    
    print("🔍 Scanning MessageTemplates for encoding issues...")
    
    fixed_count = 0
    templates = MessageTemplate.objects.all()
    
    for template in templates:
        original_subject = template.subject
        original_body = template.body
        
        # Fix subject and body
        template.subject = fix_text(template.subject)
        template.body = fix_text(template.body)
        
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
    
    # Verify template #6 specifically
    try:
        t6 = MessageTemplate.objects.get(id=6)
        print("=== Template #6 Verification ===")
        print(f"Contains ✅: {'✅' in t6.body}")
        print(f"Contains âœ…: {'âœ…' in t6.body}")
        print(f"Body preview: {t6.body[100:200]}")
        print()
    except MessageTemplate.DoesNotExist:
        pass


if __name__ == "__main__":
    fix_message_templates()
