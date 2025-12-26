"""
Rule Engine - Evaluates rules against input context and generates recommendations
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re

from app.models.schemas import (
    RecommendationRequest,
    RecommendationAction,
    DailyScheduleItem,
    RecommendationResponse,
    UrgencyLevel
)


class RuleEngine:
    """
    Core rule evaluation engine.
    Evaluates conditions and generates recommendations.
    """
    
    def __init__(self, rules: Dict[str, Dict[str, Any]], constants: Dict[str, Any]):
        self.rules = rules
        self.constants = constants
    
    def evaluate(self, request: RecommendationRequest) -> RecommendationResponse:
        """
        Main evaluation method - processes request and returns recommendations
        """
        farm_type = request.farm_type.value
        
        # Get rules for this farm type
        farm_rules = self.rules.get(farm_type, {})
        
        # Build context dictionary for evaluation
        context = self._build_context(request)
        
        # Evaluate all rules
        matched_rules: List[RecommendationAction] = []
        
        for category, category_data in farm_rules.items():
            if category_data and 'rules' in category_data:
                for rule in category_data['rules']:
                    if self._is_rule_enabled(rule):
                        match, action = self._evaluate_rule(rule, context, category)
                        if match and action:
                            matched_rules.append(action)
        
        # Sort by urgency score (highest first)
        matched_rules.sort(key=lambda x: x.urgency_score, reverse=True)
        
        # Group by urgency level
        response = self._group_recommendations(matched_rules, request)
        
        # Generate daily schedule
        response.daily_schedule = self._generate_schedule(matched_rules, farm_type)
        
        # Generate summary
        response.summary_az, response.summary_en = self._generate_summary(response)
        response.total_recommendations = len(matched_rules)
        
        return response
    
    def _build_context(self, request: RecommendationRequest) -> Dict[str, Any]:
        """Build flat context dictionary from request for rule evaluation"""
        context = {
            'farm_type': request.farm_type.value,
            'region': request.region.value,
            'date': request.request_date.isoformat(),
        }
        
        # Add weather data
        if request.weather:
            weather_dict = request.weather.model_dump()
            for key, value in weather_dict.items():
                context[f'weather.{key}'] = value
        
        # Add soil data
        if request.soil:
            soil_dict = request.soil.model_dump()
            for key, value in soil_dict.items():
                if value is not None:
                    context[f'soil.{key}'] = value
        
        # Add crop context
        if request.crop_context:
            crop_dict = request.crop_context.model_dump()
            for key, value in crop_dict.items():
                if value is not None:
                    context[f'crop_context.{key}'] = value
        
        # Add livestock context
        if request.livestock_context:
            livestock_dict = request.livestock_context.model_dump()
            for key, value in livestock_dict.items():
                if value is not None:
                    context[f'livestock_context.{key}'] = value
        
        # Add greenhouse context
        if request.greenhouse_context:
            gh_dict = request.greenhouse_context.model_dump()
            for key, value in gh_dict.items():
                if value is not None:
                    context[f'greenhouse_context.{key}'] = value
        
        # Add resource context
        if request.resource_context:
            res_dict = request.resource_context.model_dump()
            for key, value in res_dict.items():
                if value is not None:
                    context[f'resource_context.{key}'] = value
        
        # Add farm components
        if request.farm_components:
            fc_dict = request.farm_components.model_dump()
            for key, value in fc_dict.items():
                context[f'farm_components.{key}'] = value
        
        # Add time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            context['time_of_day'] = 'morning'
        elif 12 <= hour < 17:
            context['time_of_day'] = 'midday'
        elif 17 <= hour < 21:
            context['time_of_day'] = 'evening'
        else:
            context['time_of_day'] = 'night'
        
        # Add day of week
        context['day_of_week'] = request.request_date.strftime('%A').lower()
        
        return context
    
    def _is_rule_enabled(self, rule: Dict[str, Any]) -> bool:
        """Check if rule is enabled"""
        return rule.get('enabled', True)
    
    def _evaluate_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any],
        category: str
    ) -> Tuple[bool, Optional[RecommendationAction]]:
        """
        Evaluate a single rule against context.
        Returns (matched: bool, action: Optional[RecommendationAction])
        """
        conditions = rule.get('conditions', {})
        
        # Check applicable_to filter if present
        applicable_to = rule.get('applicable_to')
        if applicable_to:
            crop_type = context.get('crop_context.crop_type')
            animal_type = context.get('livestock_context.animal_type')
            
            if crop_type and crop_type not in applicable_to:
                return False, None
            if animal_type and animal_type not in applicable_to:
                return False, None
        
        # Evaluate conditions
        if not self._evaluate_conditions(conditions, context):
            return False, None
        
        # Rule matched - build action
        action = self._build_action(rule, context, category)
        return True, action
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate condition block (can be nested with AND/OR)"""
        if not conditions:
            return True
        
        operator = conditions.get('operator', 'AND')
        items = conditions.get('items', [])
        
        if not items:
            return True
        
        results = []
        
        for item in items:
            # Check if this is a nested condition block
            if 'operator' in item and 'items' in item:
                result = self._evaluate_conditions(item, context)
            else:
                result = self._evaluate_single_condition(item, context)
            results.append(result)
        
        if operator == 'AND':
            return all(results)
        elif operator == 'OR':
            return any(results)
        else:
            return all(results)
    
    def _evaluate_single_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single condition item"""
        field = condition.get('field', '')
        op = condition.get('operator', '==')
        expected_value = condition.get('value')
        
        # Get actual value from context
        actual_value = context.get(field)
        
        # Handle missing field
        if actual_value is None:
            # Special operators for checking existence
            if op == 'NOT_EMPTY':
                return False
            if op == 'EMPTY':
                return True
            return False
        
        # Evaluate based on operator
        try:
            if op == '==':
                return actual_value == expected_value
            elif op == '!=':
                return actual_value != expected_value
            elif op == '>':
                return float(actual_value) > float(expected_value)
            elif op == '>=':
                return float(actual_value) >= float(expected_value)
            elif op == '<':
                return float(actual_value) < float(expected_value)
            elif op == '<=':
                return float(actual_value) <= float(expected_value)
            elif op == 'IN':
                if isinstance(expected_value, list):
                    return actual_value in expected_value
                return False
            elif op == 'NOT_IN':
                if isinstance(expected_value, list):
                    return actual_value not in expected_value
                return True
            elif op == 'CONTAINS':
                if isinstance(actual_value, list):
                    if isinstance(expected_value, list):
                        return any(e in actual_value for e in expected_value)
                    return expected_value in actual_value
                return False
            elif op == 'NOT_EMPTY':
                if isinstance(actual_value, list):
                    return len(actual_value) > 0
                return bool(actual_value)
            elif op == 'EMPTY':
                if isinstance(actual_value, list):
                    return len(actual_value) == 0
                return not bool(actual_value)
            else:
                return False
        except (ValueError, TypeError):
            return False
    
    def _build_action(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any],
        category: str
    ) -> RecommendationAction:
        """Build recommendation action from matched rule"""
        action_data = rule.get('action', {})
        
        # Get urgency
        urgency_str = action_data.get('urgency', 'medium')
        try:
            urgency = UrgencyLevel(urgency_str)
        except ValueError:
            urgency = UrgencyLevel.MEDIUM
        
        # Process message templates
        message_az = self._process_template(rule.get('message_az', ''), context)
        message_en = self._process_template(rule.get('message_en', ''), context)
        
        return RecommendationAction(
            rule_id=rule.get('rule_id', ''),
            name_az=rule.get('name_az', ''),
            name_en=rule.get('name_en', ''),
            category=category,
            urgency=urgency,
            urgency_score=action_data.get('urgency_score', 50),
            message_az=message_az,
            message_en=message_en,
            action_type=action_data.get('type', 'info'),
            action_details=action_data,
            timing_az=action_data.get('timing_az')
        )
    
    def _process_template(self, template: str, context: Dict[str, Any]) -> str:
        """Process message template, replacing {field} placeholders with values"""
        if not template:
            return template
        
        def replace_placeholder(match):
            field_name = match.group(1)
            # Try direct field name
            value = context.get(field_name)
            if value is not None:
                return str(value)
            
            # Try with common prefixes
            for prefix in ['weather.', 'soil.', 'crop_context.', 'livestock_context.', 'greenhouse_context.']:
                value = context.get(f'{prefix}{field_name}')
                if value is not None:
                    return str(value)
            
            return match.group(0)  # Return original if not found
        
        return re.sub(r'\{(\w+)\}', replace_placeholder, template)
    
    def _group_recommendations(
        self, 
        recommendations: List[RecommendationAction],
        request: RecommendationRequest
    ) -> RecommendationResponse:
        """Group recommendations by urgency level"""
        response = RecommendationResponse(
            farm_type=request.farm_type,
            region=request.region,
            response_date=request.request_date
        )
        
        for rec in recommendations:
            if rec.urgency == UrgencyLevel.CRITICAL:
                response.critical_alerts.append(rec)
            elif rec.urgency == UrgencyLevel.HIGH:
                response.high_priority.append(rec)
            elif rec.urgency == UrgencyLevel.MEDIUM:
                response.medium_priority.append(rec)
            elif rec.urgency == UrgencyLevel.LOW:
                response.low_priority.append(rec)
            else:
                response.info.append(rec)
        
        return response
    
    def _generate_schedule(
        self, 
        recommendations: List[RecommendationAction],
        farm_type: str
    ) -> List[DailyScheduleItem]:
        """Generate daily schedule from recommendations"""
        schedule = []
        
        # Default time slots based on farm type
        time_slots = {
            'early_morning': '05:00-07:00',
            'morning': '07:00-10:00',
            'late_morning': '10:00-12:00',
            'midday': '12:00-15:00',
            'afternoon': '15:00-17:00',
            'evening': '17:00-19:00',
            'night': '19:00-21:00'
        }
        
        # Assign recommendations to time slots based on action type
        action_time_mapping = {
            'irrigate': 'early_morning',
            'fertilize': 'morning',
            'apply_fungicide': 'morning',
            'apply_insecticide': 'early_morning',
            'harvest': 'late_morning',
            'prune': 'morning',
            'vaccination_reminder': 'morning',
            'vet_checkup_reminder': 'morning',
            'feeding_recommendation': 'early_morning',
            'emergency_cooling': 'midday',
            'monitor': 'morning',
        }
        
        for rec in recommendations[:10]:  # Limit to top 10 for schedule
            action_type = rec.action_type
            time_key = action_time_mapping.get(action_type, 'morning')
            time_slot = time_slots.get(time_key, '08:00-10:00')
            
            priority = 'must_do' if rec.urgency in [UrgencyLevel.CRITICAL, UrgencyLevel.HIGH] else 'should_do'
            
            schedule.append(DailyScheduleItem(
                time_slot=time_slot,
                task_az=rec.name_az,
                task_en=rec.name_en,
                priority=priority,
                related_rule_id=rec.rule_id,
                urgency_score=rec.urgency_score
            ))
        
        # Sort schedule by time slot
        schedule.sort(key=lambda x: x.time_slot)
        
        return schedule
    
    def _generate_summary(self, response: RecommendationResponse) -> Tuple[str, str]:
        """Generate summary text in Azerbaijani and English"""
        critical_count = len(response.critical_alerts)
        high_count = len(response.high_priority)
        medium_count = len(response.medium_priority)
        low_count = len(response.low_priority)
        
        total = critical_count + high_count + medium_count + low_count
        
        if critical_count > 0:
            summary_az = f"⚠️ DİQQƏT: {critical_count} kritik xəbərdarlıq var! Dərhal müdaxilə lazımdır. Ümumi {total} tövsiyə."
            summary_en = f"⚠️ ATTENTION: {critical_count} critical alerts! Immediate action required. Total {total} recommendations."
        elif high_count > 0:
            summary_az = f"📋 Bu gün {high_count} yüksək prioritetli və {medium_count} orta prioritetli tapşırıq var."
            summary_en = f"📋 Today you have {high_count} high priority and {medium_count} medium priority tasks."
        elif total > 0:
            summary_az = f"✅ Vəziyyət sabitdir. {total} ümumi tövsiyə var."
            summary_en = f"✅ Situation stable. {total} total recommendations."
        else:
            summary_az = "✅ Heç bir xüsusi tövsiyə yoxdur. Hər şey qaydasındadır."
            summary_en = "✅ No special recommendations. Everything is in order."
        
        return summary_az, summary_en
