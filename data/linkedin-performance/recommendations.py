#!/usr/bin/env python3
"""
Performance-Based Recommendations Engine
Suggests optimal post types and hooks based on historical performance
"""

import json
from pathlib import Path
from analyze_performance import PerformanceAnalyzer

class RecommendationEngine:
    def __init__(self, csv_file):
        self.analyzer = PerformanceAnalyzer(str(csv_file))
        self.report = self.analyzer.generate_report()

    def get_best_post_types(self, limit=3):
        """Get post types ranked by engagement"""
        by_type = self.report['by_post_type']
        sorted_types = sorted(by_type.items(),
                             key=lambda x: x[1]['avg_engagement_rate'],
                             reverse=True)
        return [(t[0], t[1]['avg_engagement_rate']) for t in sorted_types[:limit]]

    def get_best_kmu_segments(self, limit=3):
        """Get KMU segments that engage most"""
        by_segment = self.report['by_kmu_segment']
        sorted_segments = sorted(by_segment.items(),
                                key=lambda x: x[1]['avg_engagement_rate'],
                                reverse=True)
        return [(s[0], s[1]['avg_engagement_rate']) for s in sorted_segments[:limit]]

    def get_best_hooks(self, limit=3):
        """Get hook variants ranked by engagement"""
        by_hook = self.report['by_hook_variant']
        sorted_hooks = sorted(by_hook.items(),
                             key=lambda x: x[1]['avg_engagement_rate'],
                             reverse=True)
        return [(h[0], h[1]['avg_engagement_rate']) for h in sorted_hooks[:limit]]

    def get_recommendations_for_next_post(self):
        """Generate full recommendation for next post"""
        best_types = self.get_best_post_types(1)
        best_segments = self.get_best_kmu_segments(1)
        best_hooks = self.get_best_hooks(1)

        recommendation = {
            'next_post_recommendation': {
                'post_type': best_types[0][0],
                'post_type_engagement': best_types[0][1],
                'kmu_segment': best_segments[0][0],
                'segment_engagement': best_segments[0][1],
                'hook_variant': best_hooks[0][0],
                'hook_engagement': best_hooks[0][1],
                'expected_engagement': round(
                    (best_types[0][1] + best_segments[0][1] + best_hooks[0][1]) / 3,
                    2
                ),
                'reasoning': f"Based on recent performance: {best_types[0][0]} posts with {best_hooks[0][0]} hook resonate best with {best_segments[0][0]} segment."
            },
            'top_3_post_types': self.get_best_post_types(3),
            'top_3_segments': self.get_best_kmu_segments(3),
            'top_3_hooks': self.get_best_hooks(3),
            'underperforming_segments': self._get_underperforming_segments(),
            'optimization_suggestions': self._get_optimization_suggestions()
        }
        return recommendation

    def _get_underperforming_segments(self):
        """Identify segments that underperform"""
        by_segment = self.report['by_kmu_segment']
        avg_engagement = self.report['avg_engagement_rate']

        underperformers = []
        for segment, metrics in by_segment.items():
            if metrics['avg_engagement_rate'] < avg_engagement - 2:
                underperformers.append({
                    'segment': segment,
                    'engagement': metrics['avg_engagement_rate'],
                    'gap': round(avg_engagement - metrics['avg_engagement_rate'], 2)
                })

        return sorted(underperformers, key=lambda x: x['gap'], reverse=True)

    def _get_optimization_suggestions(self):
        """Generate tactical suggestions"""
        suggestions = []

        # Suggestion 1: Top performer
        best_type = self.get_best_post_types(1)[0]
        suggestions.append(
            f"📈 Scale {best_type[0]} posts — they're performing {best_type[1]:.1f}% engagement (your best)"
        )

        # Suggestion 2: Segment focus
        best_segment = self.get_best_kmu_segments(1)[0]
        suggestions.append(
            f"🎯 Focus on {best_segment[0]} content — this segment shows {best_segment[1]:.1f}% engagement"
        )

        # Suggestion 3: Hook winner
        best_hook = self.get_best_hooks(1)[0]
        suggestions.append(
            f"🔥 Use {best_hook[0]} hook in next 3 posts — it's your winner at {best_hook[1]:.1f}%"
        )

        # Suggestion 4: Fix underperformers
        underperformers = self._get_underperforming_segments()
        if underperformers:
            worst = underperformers[0]
            suggestions.append(
                f"⚠️ {worst['segment']} posts underperform by {worst['gap']}pp — test new angles"
            )

        return suggestions

    def print_recommendations(self):
        """Print human-readable recommendations"""
        rec = self.get_recommendations_for_next_post()

        print("\n" + "="*70)
        print("🎯 NEXT POST RECOMMENDATION")
        print("="*70)
        print(f"Post Type: {rec['next_post_recommendation']['post_type']}")
        print(f"  └─ Expected Engagement: {rec['next_post_recommendation']['post_type_engagement']}%")
        print(f"\nTarget Segment: {rec['next_post_recommendation']['kmu_segment']}")
        print(f"  └─ Expected Engagement: {rec['next_post_recommendation']['segment_engagement']}%")
        print(f"\nHook Variant: {rec['next_post_recommendation']['hook_variant']}")
        print(f"  └─ Expected Engagement: {rec['next_post_recommendation']['hook_engagement']}%")
        print(f"\n🔮 Predicted Engagement: {rec['next_post_recommendation']['expected_engagement']}%")
        print(f"\n💡 Reasoning: {rec['next_post_recommendation']['reasoning']}")

        print("\n" + "="*70)
        print("📊 PERFORMANCE RANKING")
        print("="*70)

        print("\nTop 3 Post Types:")
        for i, (ptype, engagement) in enumerate(rec['top_3_post_types'], 1):
            print(f"  {i}. {ptype}: {engagement}%")

        print("\nTop 3 KMU Segments:")
        for i, (segment, engagement) in enumerate(rec['top_3_segments'], 1):
            print(f"  {i}. {segment}: {engagement}%")

        print("\nTop 3 Hook Variants:")
        for i, (hook, engagement) in enumerate(rec['top_3_hooks'], 1):
            print(f"  {i}. {hook}: {engagement}%")

        if rec['underperforming_segments']:
            print("\n⚠️ UNDERPERFORMING SEGMENTS (Fix these!):")
            for item in rec['underperforming_segments']:
                print(f"  • {item['segment']}: {item['engagement']}% (gap: -{item['gap']}pp)")

        print("\n" + "="*70)
        print("💡 OPTIMIZATION SUGGESTIONS")
        print("="*70)
        for suggestion in rec['optimization_suggestions']:
            print(f"{suggestion}")

        print("\n" + "="*70)
        return rec

if __name__ == '__main__':
    csv_file = Path(__file__).parent / 'posts-tracker.csv'
    engine = RecommendationEngine(csv_file)
    recommendations = engine.print_recommendations()

    # Save recommendations
    rec_file = Path(__file__).parent / 'recommendations.json'
    with open(rec_file, 'w', encoding='utf-8') as f:
        json.dump(recommendations, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Recommendations saved to {rec_file}")
