"""
Rule Loader Service - Loads all JSON rules, constants, and profiles
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

from app.core.config import settings


class RuleLoader:
    """Service to load and manage all rules from JSON files"""
    
    def __init__(self):
        self.data_path = Path(settings.DATA_PATH)
        self.constants_path = Path(settings.CONSTANTS_PATH)
        self.profiles_path = Path(settings.PROFILES_PATH)
        self.rules_path = Path(settings.RULES_PATH)
        
        self._constants: Dict[str, Any] = {}
        self._profiles: Dict[str, Any] = {}
        self._rules: Dict[str, Dict[str, Any]] = {}
    
    def _load_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load a single JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def load_constants(self) -> Dict[str, Any]:
        """Load all constant files"""
        if self._constants:
            return self._constants
        
        constants = {}
        
        # Load stages
        stages_path = self.constants_path / "stages.json"
        if stages_path.exists():
            constants['stages'] = self._load_json_file(stages_path)
        
        # Load regions
        regions_path = self.constants_path / "regions.json"
        if regions_path.exists():
            constants['regions'] = self._load_json_file(regions_path)
        
        # Load thresholds
        thresholds_path = self.constants_path / "thresholds.json"
        if thresholds_path.exists():
            constants['thresholds'] = self._load_json_file(thresholds_path)
        
        self._constants = constants
        return constants
    
    def load_profiles(self) -> Dict[str, Any]:
        """Load all farm profiles"""
        if self._profiles:
            return self._profiles
        
        profiles = {}
        
        profile_files = [
            ("wheat", "wheat_profile.json"),
            ("livestock", "livestock_profile.json"),
            ("orchard", "orchard_profile.json"),
            ("vegetable", "vegetable_profile.json"),
            ("mixed", "mixed_profile.json")
        ]
        
        for farm_type, filename in profile_files:
            file_path = self.profiles_path / filename
            if file_path.exists():
                profiles[farm_type] = self._load_json_file(file_path)
        
        self._profiles = profiles
        return profiles
    
    def load_all_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load all rules from all farm types and categories"""
        if self._rules:
            return self._rules
        
        rules = {}
        
        # Define farm types and their rule categories
        farm_rule_categories = {
            "wheat": ["irrigation", "fertilization", "pest_disease", "harvest"],
            "livestock": ["disease_risk", "feeding", "veterinary"],
            "orchard": ["irrigation", "fertilization", "pruning", "pest_disease"],
            "vegetable": ["irrigation", "fertilization", "greenhouse", "pest_disease"],
            "mixed": ["integration", "resource_allocation", "daily_coordination"]
        }
        
        for farm_type, categories in farm_rule_categories.items():
            rules[farm_type] = {}
            farm_rules_path = self.rules_path / farm_type
            
            for category in categories:
                file_path = farm_rules_path / f"{category}.json"
                if file_path.exists():
                    rules[farm_type][category] = self._load_json_file(file_path)
        
        self._rules = rules
        return rules
    
    def get_rules_for_farm_type(self, farm_type: str) -> Dict[str, Any]:
        """Get all rules for a specific farm type"""
        if not self._rules:
            self.load_all_rules()
        return self._rules.get(farm_type, {})
    
    def get_profile(self, farm_type: str) -> Optional[Dict[str, Any]]:
        """Get profile for a specific farm type"""
        if not self._profiles:
            self.load_profiles()
        return self._profiles.get(farm_type)
    
    def get_thresholds(self) -> Optional[Dict[str, Any]]:
        """Get threshold constants"""
        if not self._constants:
            self.load_constants()
        return self._constants.get('thresholds')
    
    def get_regions(self) -> Optional[Dict[str, Any]]:
        """Get region constants"""
        if not self._constants:
            self.load_constants()
        return self._constants.get('regions')
    
    def get_stages(self) -> Optional[Dict[str, Any]]:
        """Get stage constants"""
        if not self._constants:
            self.load_constants()
        return self._constants.get('stages')
    
    def get_all_rule_ids(self) -> List[str]:
        """Get list of all rule IDs"""
        if not self._rules:
            self.load_all_rules()
        
        rule_ids = []
        for farm_type, categories in self._rules.items():
            for category, data in categories.items():
                if data and 'rules' in data:
                    for rule in data['rules']:
                        rule_ids.append(rule.get('rule_id', ''))
        
        return [rid for rid in rule_ids if rid]
    
    def count_rules(self) -> Dict[str, int]:
        """Count rules by farm type and category"""
        if not self._rules:
            self.load_all_rules()
        
        counts = {}
        total = 0
        
        for farm_type, categories in self._rules.items():
            counts[farm_type] = {}
            farm_total = 0
            
            for category, data in categories.items():
                if data and 'rules' in data:
                    count = len(data['rules'])
                    counts[farm_type][category] = count
                    farm_total += count
            
            counts[farm_type]['_total'] = farm_total
            total += farm_total
        
        counts['_total'] = total
        return counts
    
    def search_rules(self, keyword: str) -> List[Dict[str, Any]]:
        """Search rules by keyword in name or message"""
        if not self._rules:
            self.load_all_rules()
        
        keyword_lower = keyword.lower()
        results = []
        
        for farm_type, categories in self._rules.items():
            for category, data in categories.items():
                if data and 'rules' in data:
                    for rule in data['rules']:
                        # Search in various fields
                        searchable = [
                            rule.get('name_az', ''),
                            rule.get('name_en', ''),
                            rule.get('message_az', ''),
                            rule.get('message_en', ''),
                            rule.get('rule_id', '')
                        ]
                        
                        if any(keyword_lower in s.lower() for s in searchable):
                            results.append({
                                'farm_type': farm_type,
                                'category': category,
                                **rule
                            })
        
        return results
