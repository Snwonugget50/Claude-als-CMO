#!/bin/bash
# LinkedIn Performance Tracking & Recommendations

cd "$(dirname "$0")/../data/linkedin-performance" || exit 1

case "$1" in
    "report")
        echo "📊 Generating Performance Report..."
        python3 analyze_performance.py
        ;;
    "recommendations"|"rec")
        echo "🎯 Generating Next Post Recommendations..."
        python3 recommendations.py
        ;;
    "add")
        if [ -z "$2" ]; then
            echo "Usage: linkedin-performance.sh add \"LP-XXX,2026-09-19,Awareness,Segment,Hook,DE,3000,9.5,285,50,30,9.5,3,active\""
            exit 1
        fi
        echo "$2" >> posts-tracker.csv
        echo "✅ Post added to tracker"
        echo "📊 Re-running analysis..."
        python3 analyze_performance.py
        ;;
    "view")
        echo "📋 Current tracked posts:"
        echo ""
        column -t -s',' posts-tracker.csv
        ;;
    "help")
        echo "LinkedIn Performance Tracking Tool"
        echo ""
        echo "Usage: linkedin-performance.sh [command]"
        echo ""
        echo "Commands:"
        echo "  report              Generate full performance report"
        echo "  recommendations     Get recommendations for next post"
        echo "  add <post_data>     Add new post to tracker"
        echo "  view                View all tracked posts"
        echo "  help                Show this help message"
        echo ""
        echo "Example:"
        echo "  ./linkedin-performance.sh report"
        echo "  ./linkedin-performance.sh recommendations"
        echo "  ./linkedin-performance.sh add 'LP-006,2026-09-19,Awareness,AI-Skeptiker,Schnell-Gewinn-Framing,DE,3500,11.8,412,68,45,11.8,2,active'"
        ;;
    *)
        python3 recommendations.py
        ;;
esac
