#!/usr/bin/env python3
"""
JSON Data Validator for AgriAdvisor Rule-Based System
Validates all JSON files in the data directory
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def validate_json_file(filepath: Path) -> tuple[bool, str]:
    """Validate a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def validate_rule_structure(rule: Dict[str, Any], rule_id: str) -> List[str]:
    """Validate rule structure"""
    errors = []
    required_fields = ['rule_id', 'name_az', 'name_en', 'priority', 'conditions', 'action', 'message_az']

    for field in required_fields:
        if field not in rule:
            errors.append(f"Rule {rule_id}: Missing required field '{field}'")

    # Validate conditions
    if 'conditions' in rule:
        cond = rule['conditions']
        if 'operator' in cond and cond['operator'] not in ['AND', 'OR']:
            errors.append(f"Rule {rule_id}: Invalid operator '{cond['operator']}'")
        if 'items' not in cond:
            errors.append(f"Rule {rule_id}: Missing 'items' in conditions")

    # Validate action
    if 'action' in rule:
        action = rule['action']
        if 'urgency' in action and action['urgency'] not in ['critical', 'high', 'medium', 'low', 'info']:
            errors.append(f"Rule {rule_id}: Invalid urgency '{action['urgency']}'")
        if 'urgency_score' in action:
            score = action['urgency_score']
            if not (0 <= score <= 100):
                errors.append(f"Rule {rule_id}: urgency_score must be 0-100, got {score}")

    return errors

def main():
    base_dir = Path(__file__).parent / 'app' / 'data'

    print("=" * 60)
    print("AGRIADVISOR JSON DATA VALIDATION")
    print("=" * 60)

    total_files = 0
    valid_files = 0
    invalid_files = 0
    total_rules = 0
    rule_errors = []

    # Validate all JSON files
    for json_file in base_dir.rglob('*.json'):
        total_files += 1
        rel_path = json_file.relative_to(base_dir)

        is_valid, message = validate_json_file(json_file)

        if is_valid:
            valid_files += 1
            print(f"✅ {rel_path}")

            # Additional validation for rule files
            if '/rules/' in str(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if 'rules' in data:
                    rules = data['rules']
                    total_rules += len(rules)

                    for i, rule in enumerate(rules):
                        rule_id = rule.get('rule_id', f'UNKNOWN_{i}')
                        errors = validate_rule_structure(rule, rule_id)
                        if errors:
                            rule_errors.extend(errors)
        else:
            invalid_files += 1
            print(f"❌ {rel_path}: {message}")

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total JSON files: {total_files}")
    print(f"Valid files: {valid_files}")
    print(f"Invalid files: {invalid_files}")
    print(f"Total rules validated: {total_rules}")

    if rule_errors:
        print(f"\n⚠️  Found {len(rule_errors)} rule structure issues:")
        for error in rule_errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(rule_errors) > 10:
            print(f"  ... and {len(rule_errors) - 10} more")
    else:
        print("\n✅ All rules have valid structure!")

    print("\n" + "=" * 60)

    # Count rules by category
    rules_by_type = {}
    for rules_dir in (base_dir / 'rules').iterdir():
        if rules_dir.is_dir():
            farm_type = rules_dir.name
            rules_by_type[farm_type] = 0

            for json_file in rules_dir.glob('*.json'):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if 'rules' in data:
                    rules_by_type[farm_type] += len(data['rules'])

    print("RULES BY FARM TYPE:")
    for farm_type, count in sorted(rules_by_type.items()):
        print(f"  {farm_type}: {count} rules")

    print("=" * 60)

    return 0 if invalid_files == 0 and len(rule_errors) == 0 else 1

if __name__ == '__main__':
    exit(main())
