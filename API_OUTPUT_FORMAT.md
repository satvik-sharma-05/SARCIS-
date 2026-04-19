# API Output Format - Rich Intelligence

## Segment Analysis Structure

Each analyzed audio segment now returns rich intelligence data:

```json
{
  "start": 0.0,
  "end": 15.5,
  "text": "मैं तीन दिन से पेमेंट नहीं कर पा रहा हूं, यह बहुत गंभीर है",
  "translated_text": "I haven't been able to make payment for three days, this is very serious",
  "language": "hi",
  
  "events": [
    "complaint",
    "technical_issue",
    "urgency"
  ],
  
  "sentiment": "frustrated",
  "sentiment_intensity": 0.85,
  
  "intent": "Demanding immediate resolution for payment system failure affecting business operations",
  
  "priority": "high",
  "risk_level": "moderate",
  "urgency": "immediate",
  
  "target": "payment system",
  
  "entities": [
    "payment",
    "3 days",
    "business"
  ],
  
  "confidence": 0.92,
  
  "summary": "Customer unable to process payments for 3 days, causing business disruption, requires immediate technical support",
  
  "analysis_source": "llm"
}
```

## Field Descriptions

### Basic Information
- **start** (float): Segment start time in seconds
- **end** (float): Segment end time in seconds
- **text** (string): Original transcribed text
- **translated_text** (string, optional): English translation if original was Hindi/Hinglish
- **language** (string): Detected language code (hi, en, ur, etc.)

### Intelligence Fields

#### events (array of strings)
Multiple event types can be detected simultaneously:
- `complaint` - Customer complaint
- `threat` - Direct threat
- `fraud_allegation` - Fraud accusation
- `legal_threat` - Legal action mentioned
- `refund_demand` - Refund request
- `technical_issue` - Technical problem
- `account_issue` - Account-related problem
- `payment_dispute` - Payment problem
- `service_failure` - Service not working
- `escalation` - Escalation demand
- `abuse` - Abusive language
- `positive_feedback` - Positive comment
- `general` - General inquiry

#### sentiment (string)
Emotional state of the speaker:
- `positive` - Happy, satisfied
- `negative` - Unhappy, dissatisfied
- `neutral` - No strong emotion
- `aggressive` - Hostile, confrontational
- `frustrated` - Annoyed, exasperated
- `fearful` - Worried, anxious
- `anxious` - Nervous, concerned
- `angry` - Furious, enraged
- `disappointed` - Let down, dissatisfied
- `satisfied` - Content, pleased

#### sentiment_intensity (float)
Strength of emotion from 0.0 to 1.0:
- `0.0 - 0.3` - Mild emotion
- `0.3 - 0.6` - Moderate emotion
- `0.6 - 0.8` - Strong emotion
- `0.8 - 1.0` - Extreme emotion

#### intent (string)
The true underlying purpose (contextual, not predefined):
- Examples:
  - "Demanding immediate refund due to service failure"
  - "Seeking technical support for payment gateway issue"
  - "Threatening legal action if problem not resolved"
  - "Requesting account access restoration"

#### priority (string)
Business priority level:
- `low` - Can wait, not urgent
- `medium` - Should be addressed soon
- `high` - Needs prompt attention
- `critical` - Requires immediate action

#### risk_level (string)
Threat/risk assessment:
- `low` - No significant risk
- `moderate` - Some risk, monitor
- `high` - Significant risk, escalate
- `extreme` - Critical risk, immediate action

#### urgency (string)
Time sensitivity:
- `low` - No time pressure
- `medium` - Address within days
- `high` - Address within hours
- `immediate` - Address right now

#### target (string or null)
Who/what is being targeted:
- Examples:
  - "customer support team"
  - "payment system"
  - "company reputation"
  - "specific employee"
  - null (if not applicable)

#### entities (array of strings)
Important entities extracted:
- Names: "John", "Acme Corp"
- Products: "Premium Plan", "Mobile App"
- Amounts: "₹5000", "$100", "5000 rupees"
- Dates: "3 days", "last week", "Monday"
- Services: "payment gateway", "customer support"

#### confidence (float)
Analysis confidence from 0.0 to 1.0:
- `0.0 - 0.5` - Low confidence
- `0.5 - 0.7` - Moderate confidence
- `0.7 - 0.9` - High confidence
- `0.9 - 1.0` - Very high confidence

#### summary (string)
Concise 1-2 sentence explanation of what's happening and why it matters:
- Contextual, not generic
- Actionable information
- Key details included

#### analysis_source (string)
Which analysis method was used:
- `llm` - Advanced LLM analysis (preferred)
- `nlp` - Rule-based NLP fallback
- `nlp_fallback` - Emergency fallback

## Example Use Cases

### High-Risk Threat Detection
```json
{
  "events": ["threat", "legal_threat", "escalation"],
  "sentiment": "aggressive",
  "sentiment_intensity": 0.95,
  "risk_level": "extreme",
  "urgency": "immediate",
  "summary": "Customer threatening legal action and public exposure if refund not processed within 24 hours"
}
```

### Technical Support Request
```json
{
  "events": ["technical_issue", "request"],
  "sentiment": "frustrated",
  "sentiment_intensity": 0.65,
  "risk_level": "low",
  "urgency": "high",
  "summary": "Customer unable to login for 2 days, requesting password reset assistance"
}
```

### Positive Feedback
```json
{
  "events": ["positive_feedback"],
  "sentiment": "satisfied",
  "sentiment_intensity": 0.80,
  "risk_level": "low",
  "urgency": "low",
  "summary": "Customer expressing appreciation for quick resolution of billing issue"
}
```

## Processing Time Metadata

Each file result includes performance metrics:

```json
{
  "file_id": "...",
  "file_name": "customer_call_01.mp3",
  "segments": [...],
  "processing_time": {
    "total": 21.45,
    "transcription": 12.34,
    "analysis": 8.56
  }
}
```

## Migration Notes

### Old Format → New Format Mapping

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `sentiment` (string) | `sentiment` (string) + `sentiment_intensity` (float) | Now includes intensity |
| `keywords` (array) | `entities` (array) | More specific extraction |
| `risk_signals` (array) | `risk_level` (string) | Consolidated assessment |
| N/A | `urgency` (string) | New field |
| N/A | `target` (string/null) | New field |
| N/A | `summary` (string) | New field |

### Backward Compatibility

The system handles both old and new formats:
- Old NLP fallback returns new structure
- Frontend should check for `sentiment.type` vs `sentiment` string
- Missing fields default to safe values

## API Endpoints

### Get Results
```
GET /clusters/{cluster_id}/results
```

Returns array of file results with segments in new format.

### Get Insights
```
GET /clusters/{cluster_id}/insights
```

Returns aggregated analytics using new intelligence fields.

---

**Last Updated:** After LLM Intelligence Upgrade  
**Version:** 2.0 (Rich Intelligence Format)
