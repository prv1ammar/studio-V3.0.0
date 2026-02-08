"""
Case Analyzer Module
Analyzes complex cases using LLM
"""

from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime
import re

class CaseAnalyzer:
    """
    Analyzes complex cases escalated to supervisor using LLM
    """
    
    def __init__(self, llm):
        """
        Initialize case analyzer
        
        Args:
            llm: LangChain LLM instance
        """
        self.llm = llm
        self.case_log = []
        self.analysis_cache = {}  # Cache for similar cases
        
    def analyze_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a complex case using LLM
        
        Args:
            case_data: {
                "description": "Case description",
                "agent": "Reporting agent name",
                "severity": "HIGH/MEDIUM/LOW",
                "patient_impact": true/false,
                "data": "Additional case data"
            }
            
        Returns:
            Detailed case analysis
        """
        from supervisor.prompt import get_supervisor_prompt
        
        try:
            print(f"🔍 Supervisor analyzing case: {case_data.get('description', 'Unknown')[:50]}...")
            
            # Prepare prompt
            prompt = get_supervisor_prompt("case_analysis")
            
            # Format prompt with case data
            formatted_prompt = prompt.format(
                case_description=case_data.get("description", "No description"),
                agent_name=case_data.get("agent", "Unknown"),
                timestamp=datetime.now().isoformat(),
                history_summary=self._get_case_history(case_data.get("agent"))
            )
            
            # Create messages for LLM
            messages = [
                {"role": "system", "content": get_supervisor_prompt("system")},
                {"role": "user", "content": formatted_prompt}
            ]
            
            # Call LLM
            response = self.llm.invoke(messages)
            
            # Parse response
            analysis = self._parse_analysis_response(response.content)
            
            # Add metadata
            analysis["analysis_id"] = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            analysis["analyzed_at"] = datetime.now().isoformat()
            analysis["original_case"] = case_data
            
            # Log analysis
            self.case_log.append(analysis)
            
            print(f"✅ Case analysis complete: {analysis.get('analysis_id')}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Case analysis error: {e}")
            return self._get_fallback_analysis(case_data)
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured analysis
        
        Args:
            response_text: LLM response text
            
        Returns:
            Structured analysis dictionary
        """
        try:
            # Try to extract JSON if present
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                analysis_json = json.loads(json_match.group())
                return analysis_json
            else:
                # Parse as text sections
                sections = {
                    "problem_summary": "",
                    "root_causes": [],
                    "immediate_actions": [],
                    "long_term_solutions": [],
                    "risk_assessment": ""
                }
                
                # Simple parsing logic
                lines = response_text.split('\n')
                current_section = None
                
                for line in lines:
                    line_lower = line.lower()
                    
                    if "problem summary" in line_lower or "summary" in line_lower:
                        current_section = "problem_summary"
                    elif "root cause" in line_lower or "causes" in line_lower:
                        current_section = "root_causes"
                    elif "immediate" in line_lower or "actions" in line_lower:
                        current_section = "immediate_actions"
                    elif "long term" in line_lower or "solutions" in line_lower:
                        current_section = "long_term_solutions"
                    elif "risk" in line_lower or "assessment" in line_lower:
                        current_section = "risk_assessment"
                    elif current_section and line.strip():
                        if current_section.endswith("s"):  # List sections
                            sections[current_section].append(line.strip())
                        else:  # Text sections
                            sections[current_section] += line.strip() + " "
                
                return sections
                
        except Exception as e:
            print(f"❌ Response parsing error: {e}")
            return {
                "raw_response": response_text,
                "parsing_error": str(e),
                "analysis_timestamp": datetime.now().isoformat()
            }
    
    def _get_case_history(self, agent_name: str) -> str:
        """
        Get historical cases for an agent
        
        Args:
            agent_name: Agent name
            
        Returns:
            History summary
        """
        agent_cases = [case for case in self.case_log 
                      if case.get("original_case", {}).get("agent") == agent_name]
        
        if not agent_cases:
            return "No previous cases for this agent"
        
        recent_cases = agent_cases[-5:]  # Last 5 cases
        
        summary = f"Recent cases for {agent_name}:\n"
        for i, case in enumerate(recent_cases, 1):
            case_desc = case.get("original_case", {}).get("description", "Unknown")
            summary += f"{i}. {case_desc[:100]}...\n"
        
        return summary
    
    def _get_fallback_analysis(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get fallback analysis when LLM fails
        
        Args:
            case_data: Case data
            
        Returns:
            Basic analysis
        """
        severity = case_data.get("severity", "MEDIUM")
        
        # Simple rule-based analysis
        if severity == "HIGH":
            actions = ["Immediate system check", "Notify technical team", "Monitor closely"]
            risk = "HIGH"
        elif severity == "MEDIUM":
            actions = ["Investigate issue", "Log for review", "Schedule fix"]
            risk = "MEDIUM"
        else:
            actions = ["Monitor", "Log for future reference"]
            risk = "LOW"
        
        return {
            "fallback_analysis": True,
            "problem_summary": case_data.get("description", "Unknown issue"),
            "severity": severity,
            "recommended_actions": actions,
            "risk_level": risk,
            "analyzed_at": datetime.now().isoformat(),
            "note": "Fallback analysis - LLM unavailable"
        }
    
    def get_similar_cases(self, current_case: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find similar historical cases
        
        Args:
            current_case: Current case data
            limit: Maximum cases to return
            
        Returns:
            List of similar cases
        """
        if not self.case_log:
            return []
        
        # Simple similarity check (in real system, use embeddings)
        current_desc = current_case.get("description", "").lower()
        
        similar_cases = []
        for case in self.case_log[-50:]:  # Check last 50 cases
            case_desc = case.get("original_case", {}).get("description", "").lower()
            
            # Check for common keywords
            common_words = set(current_desc.split()) & set(case_desc.split())
            if len(common_words) >= 3:  # At least 3 common words
                similar_cases.append(case)
            
            if len(similar_cases) >= limit:
                break
        
        return similar_cases
    
    def generate_report(self, time_period: str = "daily") -> Dict[str, Any]:
        """
        Generate analysis report
        
        Args:
            time_period: daily, weekly, monthly
            
        Returns:
            Report data
        """
        now = datetime.now()
        
        if time_period == "daily":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif time_period == "weekly":
            start_time = now.replace(day=now.day-7)
        else:  # monthly
            start_time = now.replace(day=1)
        
        # Filter cases for period
        period_cases = []
        for case in self.case_log:
            analyzed_at = case.get("analyzed_at")
            if analyzed_at:
                case_time = datetime.fromisoformat(analyzed_at)
                if case_time >= start_time:
                    period_cases.append(case)
        
        # Generate statistics
        total_cases = len(period_cases)
        high_severity = sum(1 for case in period_cases 
                           if case.get("original_case", {}).get("severity") == "HIGH")
        
        agents_involved = set()
        for case in period_cases:
            agent = case.get("original_case", {}).get("agent")
            if agent:
                agents_involved.add(agent)
        
        return {
            "period": time_period,
            "start_time": start_time.isoformat(),
            "end_time": now.isoformat(),
            "total_cases_analyzed": total_cases,
            "high_severity_cases": high_severity,
            "agents_involved": list(agents_involved),
            "average_resolution_time": "N/A",  # Would track resolution times
            "common_issues": self._get_common_issues(period_cases),
            "recommendations": self._generate_recommendations(period_cases)
        }
    
    def _get_common_issues(self, cases: List[Dict[str, Any]]) -> List[str]:
        """Extract common issues from cases"""
        issues = []
        for case in cases:
            analysis = case.get("problem_summary") or case.get("raw_response", "")
            if analysis and isinstance(analysis, str):
                # Extract first sentence as issue
                first_sentence = analysis.split('.')[0]
                issues.append(first_sentence[:100])
        
        # Count occurrences
        from collections import Counter
        issue_counts = Counter(issues)
        
        return [f"{issue} ({count} times)" for issue, count in issue_counts.most_common(5)]
    
    def _generate_recommendations(self, cases: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations from cases"""
        recommendations = []
        
        # Check for recurring issues
        agent_issues = {}
        for case in cases:
            agent = case.get("original_case", {}).get("agent")
            if agent:
                agent_issues.setdefault(agent, 0)
                agent_issues[agent] += 1
        
        # Generate recommendations
        for agent, count in agent_issues.items():
            if count >= 3:
                recommendations.append(f"Agent {agent} has {count} issues - needs review")
        
        if not cases:
            recommendations.append("No cases analyzed - system running smoothly")
        
        return recommendations[:5]  # Top 5 recommendations