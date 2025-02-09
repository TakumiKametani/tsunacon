import re
from django.core.exceptions import ValidationError

def validate_katakana(value):
    katakana_regex = re.compile(r'^[\u30A0-\u30FF]+$')
    if not katakana_regex.match(value):
        raise ValidationError(
            'このフィールドはカタカナのみを含む必要があります。', params={'value': value},
        )
