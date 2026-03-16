# -*- coding: utf-8 -*-
"""
Django management command to fix UTF-8 encoding in message templates

Usage:
    python manage.py fix_template_encoding
"""

from django.core.management.base import BaseCommand
from core.models import MessageTemplate


class Command(BaseCommand):
    help = 'Fix UTF-8 encoding issues in message templates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without actually fixing it'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write('🔍 DRY RUN MODE - No changes will be made\n')
        else:
            self.stdout.write('🔧 Starting UTF-8 encoding repair...\n')
        
        fixed_count = 0
        templates = MessageTemplate.objects.all()
        
        for template in templates:
            original_subject = template.subject
            original_body = template.body
            
            # Fix encoding
            fixed_subject = self.fix_encoding(template.subject)
            fixed_body = self.fix_encoding(template.body)
            
            # Check if changed
            if fixed_subject != original_subject or fixed_body != original_body:
                if dry_run:
                    self.stdout.write(f'📄 Would fix #{template.id}: {template.name}')
                    self.stdout.write(f'   Subject: {original_subject[:60]} → {fixed_subject[:60]}')
                else:
                    template.subject = fixed_subject
                    template.body = fixed_body
                    template.save()
                    self.stdout.write(f'✅ Fixed #{template.id}: {template.name}')
                
                fixed_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        if dry_run:
            self.stdout.write(f'📋 DRY RUN COMPLETE - {fixed_count} templates would be fixed')
        else:
            self.stdout.write(f'✅ REPAIR COMPLETE - {fixed_count} templates fixed')
        self.stdout.write(f'{"="*60}\n')

    def fix_encoding(self, text):
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
        }
        
        for wrong, right in replacements.items():
            text = text.replace(wrong, right)
        
        return text
