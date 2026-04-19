# Cluster Insights & Analytics Feature

## Overview

The Insights feature provides comprehensive visual analytics and rankings for each cluster, helping users quickly understand patterns, identify critical issues, and prioritize actions.

## Features

### 1. Key Metrics Dashboard
- **Total Files**: Number of files in cluster
- **Total Segments**: Total audio segments analyzed
- **Complaint Percentage**: % of segments with complaints
- **Urgency Percentage**: % of segments requiring immediate action
- **Negative Percentage**: % of negative sentiment
- **High Priority Percentage**: % of critical/high priority segments

### 2. Visual Charts

#### Sentiment Distribution (Pie Chart)
- Shows breakdown of positive, negative, and neutral sentiments
- Color-coded for easy identification
- Percentage labels on each slice

#### Priority Distribution (Pie Chart)
- Shows breakdown of critical, high, medium, and low priorities
- Helps identify urgency levels across cluster
- Color-coded by severity

#### Event Distribution (Bar Chart)
- Shows frequency of different event types
- Includes: complaints, urgency, requests, technical issues, etc.
- Sorted by frequency

#### Top Issues (Horizontal Bar Chart)
- Shows most common intents/issues
- Includes: technical issues, payment issues, refund requests, etc.
- Top 5 issues displayed

### 3. File Rankings

Files are ranked by importance score calculated as:

```
score = (
    complaint_count × 2 +
    urgency_count × 3 +
    escalation_count × 4 +
    negative_count × 1.5 +
    high_priority_count × 2 +
    risk_count × 5
)
```

**Ranking Display:**
- Top 10 files shown
- Medal icons for top 3 (🥇🥈🥉)
- Shows segment count, complaints, urgency, and risks
- Clickable to view detailed results
- Importance score prominently displayed

### 4. Risk Signals Alert

If risk signals are detected:
- Red alert box displayed
- Shows all risk types and counts
- Includes: legal threats, escalation risks, fraud allegations, security threats
- Helps identify critical issues requiring immediate attention

## Backend Implementation

### Endpoint
```
GET /clusters/{cluster_id}/insights
```

### Response Structure
```json
{
  "insights": {
    "cluster_id": "...",
    "cluster_name": "...",
    
    "metrics": {
      "total_files": 10,
      "total_segments": 150,
      "complaint_percentage": 35.5,
      "urgency_percentage": 12.3,
      "negative_percentage": 45.2,
      "high_priority_percentage": 28.7
    },
    
    "sentiment_distribution": {
      "positive": 50,
      "negative": 80,
      "neutral": 20
    },
    
    "sentiment_percentages": {
      "positive": 33.3,
      "negative": 53.3,
      "neutral": 13.3
    },
    
    "event_distribution": {
      "complaint": 45,
      "urgency": 20,
      "technical_issue": 30,
      "financial_issue": 15
    },
    
    "priority_distribution": {
      "critical": 10,
      "high": 35,
      "medium": 60,
      "low": 45
    },
    
    "language_distribution": {
      "en": 5,
      "hi": 3,
      "ur": 2
    },
    
    "top_files": [
      {
        "file_id": "...",
        "file_name": "complaint_01.mp3",
        "score": 45.5,
        "segments": 15,
        "complaint_count": 8,
        "urgency_count": 5,
        "escalation_count": 2,
        "negative_count": 12,
        "high_priority_count": 10,
        "risk_count": 1,
        "language": "hi",
        "summary": {...}
      }
    ],
    
    "top_issues": {
      "technical_issue": 45,
      "payment_issue": 30,
      "refund_request": 25,
      "account_issue": 15,
      "help_request": 10
    },
    
    "risk_signals": {
      "legal_threat": 3,
      "escalation_risk": 5,
      "fraud_allegation": 2
    },
    
    "avg_segments_per_file": 15.0,
    "files_with_risks": 3,
    "files_with_escalation": 5
  }
}
```

### Key Implementation Details

1. **No Recomputation**: Uses existing results from MongoDB
2. **Efficient Aggregation**: Single query to fetch all results, then compute in memory
3. **Simple Logic**: Uses Python's Counter for frequency counting
4. **Clear Formulas**: Importance score formula is documented and easy to adjust

## Frontend Implementation

### Technology Stack
- **React**: Component framework
- **Recharts**: Chart library (simple and lightweight)
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations

### Page Structure
```
/insights/[id]/page.tsx
├── Header (with back button)
├── Key Metrics (4 cards)
├── Charts Row
│   ├── Sentiment Pie Chart
│   └── Priority Pie Chart
├── Event Distribution Bar Chart
├── Top Issues Horizontal Bar Chart
├── File Rankings List
└── Risk Signals Alert (if any)
```

### Navigation
- From cluster page: "View Insights" button (purple)
- From insights page: Back to cluster
- From file rankings: Click to view results

## Usage Flow

1. **Upload files** to cluster
2. **Run analysis** on cluster
3. **View Insights** button appears after analysis completes
4. **Click "View Insights"** to see analytics dashboard
5. **Review metrics** and charts
6. **Check file rankings** to prioritize
7. **Click on files** to view detailed results

## Performance

### Backend
- Single database query to fetch results
- In-memory aggregation (fast)
- No additional processing or model loading
- Response time: < 1 second for typical clusters

### Frontend
- Charts render client-side
- Smooth animations with Framer Motion
- Responsive design (mobile-friendly)
- Fast page load

## Customization

### Adjusting Importance Score
Edit `backend/main.py` in the insights endpoint:

```python
# Current formula
score = (
    complaint_count * 2 +
    urgency_count * 3 +
    escalation_count * 4 +
    negative_count * 1.5 +
    high_priority_count * 2 +
    risk_count * 5
)

# Adjust weights as needed
score = (
    complaint_count * YOUR_WEIGHT +
    urgency_count * YOUR_WEIGHT +
    ...
)
```

### Adding New Charts
1. Add data preparation in backend endpoint
2. Add chart component in frontend page
3. Use Recharts documentation for chart types

### Changing Colors
Edit colors in `frontend/app/insights/[id]/page.tsx`:

```typescript
const sentimentData = [
    { name: 'Positive', value: ..., color: '#10b981' }, // Change color
    { name: 'Negative', value: ..., color: '#ef4444' },
    ...
];
```

## Dependencies

### Backend
- No new dependencies (uses existing MongoDB, FastAPI)

### Frontend
- `recharts`: ^2.10.3 (added to package.json)

Install with:
```bash
cd frontend
npm install
```

## Testing

### 1. Backend Endpoint
```bash
# Get insights for a cluster
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/clusters/CLUSTER_ID/insights
```

### 2. Frontend Page
1. Navigate to cluster page
2. Ensure analysis is completed
3. Click "View Insights" button
4. Verify all charts and metrics display correctly

## Troubleshooting

### Issue: "No insights available"
**Solution**: Run analysis on the cluster first

### Issue: Charts not displaying
**Solution**: 
1. Check browser console for errors
2. Ensure recharts is installed: `npm install`
3. Restart frontend dev server

### Issue: File rankings show zero scores
**Solution**: Check if analysis detected any events/issues in the files

### Issue: Backend returns empty insights
**Solution**: Verify results exist in MongoDB for the cluster

## Code Quality

### Backend
- ✅ Clear comments explaining calculations
- ✅ Simple, readable logic
- ✅ No complex algorithms
- ✅ Efficient aggregation
- ✅ Proper error handling

### Frontend
- ✅ Component-based structure
- ✅ Responsive design
- ✅ Smooth animations
- ✅ Clear visual hierarchy
- ✅ Accessible colors

## Summary

The Insights feature provides:
- **Visual Analytics**: Easy-to-understand charts and graphs
- **File Rankings**: Prioritize files by importance
- **Risk Detection**: Highlight critical issues
- **Fast Performance**: No recomputation, uses existing data
- **Simple Code**: Easy to maintain and customize

Perfect for quickly understanding cluster patterns and identifying priority issues!
