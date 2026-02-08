"""
Decision Maker Module
Makes intelligent decisions using LLM
"""

from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime
from enum import Enum
import re

class DecisionType(Enum):
    """Types of decisions supervisor can make"""
    AUTO_RESOLVE = "AUTO_RESOLVE"
    ESCALATE_JUDGE = "ESCALATE_TO_JUDGE"
    HUMAN_INTERVENTION = "HUMAN_INTERVENTION"
    POLICY_CHANGE = "POLICY_CHANGE"
    SYSTEM_UPDATE = "SYSTEM_UPDATE"

class PriorityLevel(Enum):
    """Priority levels"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class DecisionMaker:
    """
    Makes intelligent decisions using LLM
    """
    
    def __init__(self, llm):
        """
        Initialize decision maker
        
        Args:
            llm: LangChain LLM instance
        """
        self.llm = llm
        self.decision_log = []
        
    def make_decision(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make intelligent decision about an issue
        
        Args:
            issue_data: {
                "type": "issue type",
                "description": "issue description",
                "agent": "reporting agent",
                "severity": "HIGH/MEDIUM/LOW",
                "data": "additional data"
            }
            
        Returns:
            Decision with action plan
        """
        from supervisor.prompt import get_supervisor_prompt
        
        try:
            print(f"🤔 Supervisor making decision for: {issue_data.get('type', 'Unknown')}")
            
            # Prepare decision prompt
            prompt = get_supervisor_prompt("escalation")
            
            # Format with issue data
            formatted_prompt = prompt.format(
                issue_description=issue_data.get("description", "No description"),
                affects_patients=issue_data.get("affects_patients", False),
                causes_downtime=issue_data.get("causes_downtime", False),
                involves_sensitive_data=issue_data.get("involves_sensitive_data", False),
                has_happened_before=issue_data.get("has_happened_before", False),
                financial_impact=issue_data.get("financial_impact", "unknown"),
                time_sensitive=issue_data.get("time_sensitive", False)
            )
            
            # Create messages
            messages = [
                {"role": "system", "content": get_supervisor_prompt("system")},
                {"role": "user", "content": formatted_prompt}
            ]
            
            # Call LLM
            response = self.llm.invoke(messages)
            
            # Parse decision
            decision = self._parse_decision_response(response.content)
            
            # Add metadata
            decision["decision_id"] = f"DEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            decision["made_at"] = datetime.now().isoformat()
            decision["original_issue"] = issue_data
            
            # Generate action plan
            decision["action_plan"] = self._generate_action_plan(decision, issue_data)
            
            # Log decision
            self.decision_log.append(decision)
            
            print(f"✅ Decision made: {decision.get('decision_type', 'Unknown')}")
            
            return decision
            
        except Exception as e:
            print(f"❌ Decision making error: {e}")
            return self._make_fallback_decision(issue_data)
    
    def _parse_decision_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured decision
        
        Args:
            response_text: LLM response
            
        Returns:
            Structured decision
        """
        try:
            # Try to extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                decision_json = json.loads(json_match.group())
                
                # Validate decision type
                valid_types = [dt.value for dt in DecisionType]
                if decision_json.get("decision") in valid_types:
                    decision_json["decision_type"] = decision_json.pop("decision")
                else:
                    decision_json["decision_type"] = DecisionType.ESCALATE_JUDGE.value
                
                return decision_json
            else:
                # Fallback parsing
                return {
                    "decision_type": DecisionType.ESCALATE_JUDGE.value,
                    "reason": "Could not parse LLM response",
                    "raw_response": response_text,
                    "priority": PriorityLevel.MEDIUM.value
                }
                
        except Exception as e:
            print(f"❌ Decision parsing error: {e}")
            return {
                "decision_type": DecisionType.ESCALATE_JUDGE.value,
                "reason": f"Parsing error: {str(e)}",
                "priority": PriorityLevel.HIGH.value
            }
    
    def _generate_action_plan(self, decision: Dict[str, Any], issue_data: Dict[str, Any]) -> List[str]:
        """
        Generate action plan based on decision
        
        Args:
            decision: Decision data
            issue_data: Original issue
            
        Returns:
            List of action steps
        """
        decision_type = decision.get("decision_type")
        severity = issue_data.get("severity", "MEDIUM")
        
        base_actions = []
        
        # Common actions
        base_actions.append(f"Log decision: {decision.get('decision_id')}")
        base_actions.append(f"Notify reporting agent: {issue_data.get('agent', 'Unknown')}")
        
        # Type-specific actions
        if decision_type == DecisionType.AUTO_RESOLVE.value:
            base_actions.extend([
                "Execute automated resolution script",
                "Verify resolution success",
                "Update system logs"
            ])
            
        elif decision_type == DecisionType.ESCALATE_JUDGE.value:
            base_actions.extend([
                "Create Judge Agent ticket",
                "Provide all case details to Judge",
                "Set resolution deadline",
                "Monitor progress"
            ])
            
        elif decision_type == DecisionType.HUMAN_INTERVENTION.value:
            base_actions.extend([
                "Create human intervention ticket",
                "Assign to appropriate team",
                "Set SLA based on severity",
                "Send notifications to team"
            ])
            
        elif decision_type == DecisionType.POLICY_CHANGE.value:
            base_actions.extend([
                "Document policy gap",
                "Create policy update proposal",
                "Review with clinic management",
                "Implement updated policy"
            ])
            
        elif decision_type == DecisionType.SYSTEM_UPDATE.value:
            base_actions.extend([
                "Create system update ticket",
                "Assess update priority",
                "Schedule update window",
                "Prepare rollback plan"
            ])
        
        # Severity-based additional actions
        if severity == "HIGH":
            base_actions.append("⏰ Immediate action required")
            base_actions.append("🚨 High priority monitoring")
        elif severity == "MEDIUM":
            base_actions.append("📅 Schedule within 24 hours")
        
        return base_actions
    
    def _make_fallback_decision(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make fallback decision when LLM fails
        
        Args:
            issue_data: Issue data
            
        Returns:
            Fallback decision
        """
        severity = issue_data.get("severity", "MEDIUM")
        affects_patients = issue_data.get("affects_patients", False)
        
        # Simple rule-based decision
        if severity == "HIGH" and affects_patients:
            decision_type = DecisionType.HUMAN_INTERVENTION.value
            priority = PriorityLevel.HIGH.value
            reason = "High severity patient issue - human intervention required"
        elif severity == "HIGH":
            decision_type = DecisionType.SYSTEM_UPDATE.value
            priority = PriorityLevel.HIGH.value
            reason = "High severity system issue - needs update"
        elif affects_patients:
            decision_type = DecisionType.ESCALATE_JUDGE.value
            priority = PriorityLevel.MEDIUM.value
            reason = "Patient-related issue - needs Judge review"
        else:
            decision_type = DecisionType.AUTO_RESOLVE.value
            priority = PriorityLevel.LOW.value
            reason = "Low impact issue - can auto-resolve"
        
        return {
            "decision_type": decision_type,
            "reason": reason,
            "priority": priority,
            "fallback_decision": True,
            "decision_id": f"FBD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "made_at": datetime.now().isoformat(),
            "original_issue": issue_data,
            "action_plan": [
                f"Execute {decision_type} protocol",
                "Monitor resolution",
                "Document as fallback decision"
            ]
        }
    
    def evaluate_performance(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate agent performance
        
        Args:
            agent_data: Agent performance metrics
            
        Returns:
            Performance evaluation
        """
        from supervisor.prompt import get_supervisor_prompt
        
        try:
            prompt = get_supervisor_prompt("performance")
            
            formatted_prompt = prompt.format(
                agent_name=agent_data.get("agent_name", "Unknown"),
                time_period=agent_data.get("time_period", "recent"),
                total_requests=agent_data.get("total_requests", 0),
                success_rate=agent_data.get("success_rate", 0),
                avg_response_time=agent_data.get("avg_response_time", 0),
                error_count=agent_data.get("error_count", 0),
                error_types=", ".join(agent_data.get("error_types", [])),
                observed_issues=agent_data.get("observed_issues", "None")
            )
            
            messages = [
                {"role": "system", "content": get_supervisor_prompt("system")},
                {"role": "user", "content": formatted_prompt}
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse evaluation
            evaluation = self._parse_evaluation_response(response.content)
            
            # Add metadata
            evaluation["evaluation_id"] = f"PERF_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            evaluation["evaluated_at"] = datetime.now().isoformat()
            evaluation["agent"] = agent_data.get("agent_name")
            
            return evaluation
            
        except Exception as e:
            print(f"❌ Performance evaluation error: {e}")
            return self._fallback_performance_evaluation(agent_data)
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse performance evaluation response"""
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "raw_evaluation": response_text,
                    "rating": "UNKNOWN",
                    "summary": "Could not parse detailed evaluation"
                }
        except:
            return {
                "raw_response": response_text,
                "parsing_error": True
            }
    
    def _fallback_performance_evaluation(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback performance evaluation"""
        success_rate = agent_data.get("success_rate", 0)
        error_count = agent_data.get("error_count", 0)
        
        if success_rate >= 90 and error_count == 0:
            rating = "EXCELLENT"
            summary = "Agent performing excellently"
        elif success_rate >= 80:
            rating = "GOOD"
            summary = "Agent performing well with minor issues"
        elif success_rate >= 70:
            rating = "FAIR"
            summary = "Agent needs improvement"
        else:
            rating = "POOR"
            summary = "Agent requires immediate attention"
        
        return {
            "rating": rating,
            "performance_summary": summary,
            "main_issues": ["Basic evaluation - LLM unavailable"],
            "immediate_actions": ["Review agent logs", "Check for patterns"],
            "fallback_evaluation": True
        }
    
    def get_decision_stats(self, time_period: str = "daily") -> Dict[str, Any]:
        """
        Get decision statistics
        
        Args:
            time_period: Time period for stats
            
        Returns:
            Statistics
        """
        now = datetime.now()
        
        if time_period == "daily":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_period == "weekly":
            start_time = now.replace(day=now.day-7)
        else:  # monthly
            start_time = now.replace(day=1)
        
        # Filter decisions for period
        period_decisions = []
        for decision in self.decision_log:
            made_at = decision.get("made_at")
            if made_at:
                decision_time = datetime.fromisoformat(made_at)
                if decision_time >= start_time:
                    period_decisions.append(decision)
        
        # Calculate statistics
        stats = {
            "total_decisions": len(period_decisions),
            "decision_types": {},
            "priority_distribution": {},
            "average_decision_time": "N/A",
            "fallback_decisions": sum(1 for d in period_decisions if d.get("fallback_decision", False))
        }
        
        # Count by type
        for decision in period_decisions:
            d_type = decision.get("decision_type", "UNKNOWN")
            priority = decision.get("priority", "UNKNOWN")
            
            stats["decision_types"][d_type] = stats["decision_types"].get(d_type, 0) + 1
            stats["priority_distribution"][priority] = stats["priority_distribution"].get(priority, 0) + 1
        
        return {
            "period": time_period,
            "stats": stats,
            "sample_decisions": period_decisions[-5:] if period_decisions else [],
            "generated_at": now.isoformat()
        }