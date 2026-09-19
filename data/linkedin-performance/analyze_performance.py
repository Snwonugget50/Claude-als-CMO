#!/usr/bin/env python3
"""
LinkedIn Post Performance Analyzer
Tracks engagement metrics by post type, KMU segment, and hook variant
"""

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

class PerformanceAnalyzer:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.posts = []
        self.load_data()

    def load_data(self):
        """Load posts from CSV"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                row['impressions'] = int(row['impressions'])
                row['engagement_rate'] = float(row['engagement_rate'])
                row['clicks'] = int(row['clicks'])
                row['comments'] = int(row['comments'])
                row['shares'] = int(row['shares'])
                row['ctr_percent'] = float(row['ctr_percent'])
                row['days_tracked'] = int(row['days_tracked'])
                self.posts.append(row)

    def analyze_by_post_type(self):
        """Aggregate performance by post type"""
        by_type = defaultdict(list)
        for post in self.posts:
            by_type[post['post_type']].append(post)

        results = {}
        for post_type, posts in by_type.items():
            avg_engagement = sum(p['engagement_rate'] for p in posts) / len(posts)
            avg_ctr = sum(p['ctr_percent'] for p in posts) / len(posts)
            total_clicks = sum(p['clicks'] for p in posts)
            total_comments = sum(p['comments'] for p in posts)

            results[post_type] = {
                'count': len(posts),
                'avg_engagement_rate': round(avg_engagement, 2),
                'avg_ctr': round(avg_ctr, 2),
                'total_clicks': total_clicks,
                'total_comments': total_comments,
                'avg_impressions': round(sum(p['impressions'] for p in posts) / len(posts), 0)
            }

        return results

    def analyze_by_kmu_segment(self):
        """Aggregate performance by KMU segment"""
        by_segment = defaultdict(list)
        for post in self.posts:
            by_segment[post['kmu_segment']].append(post)

        results = {}
        for segment, posts in by_segment.items():
            avg_engagement = sum(p['engagement_rate'] for p in posts) / len(posts)
            avg_ctr = sum(p['ctr_percent'] for p in posts) / len(posts)

            results[segment] = {
                'count': len(posts),
                'avg_engagement_rate': round(avg_engagement, 2),
                'avg_ctr': round(avg_ctr, 2),
                'total_clicks': sum(p['clicks'] for p in posts),
                'total_comments': sum(p['comments'] for p in posts)
            }

        return results

    def analyze_by_hook_variant(self):
        """Aggregate performance by hook variant"""
        by_hook = defaultdict(list)
        for post in self.posts:
            by_hook[post['hook_variant']].append(post)

        results = {}
        for hook, posts in by_hook.items():
            if len(posts) > 0:
                avg_engagement = sum(p['engagement_rate'] for p in posts) / len(posts)
                avg_ctr = sum(p['ctr_percent'] for p in posts) / len(posts)

                results[hook] = {
                    'count': len(posts),
                    'avg_engagement_rate': round(avg_engagement, 2),
                    'avg_ctr': round(avg_ctr, 2),
                    'best_performer': max(posts, key=lambda x: x['engagement_rate'])['post_id']
                }

        return results

    def get_top_performers(self, metric='engagement_rate', limit=3):
        """Get top performing posts"""
        sorted_posts = sorted(self.posts, key=lambda x: float(x[metric]), reverse=True)
        return sorted_posts[:limit]

    def generate_report(self):
        """Generate full performance report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_posts': len(self.posts),
            'total_impressions': sum(p['impressions'] for p in self.posts),
            'total_engagement': sum(p['engagement_rate'] for p in self.posts),
            'avg_engagement_rate': round(sum(p['engagement_rate'] for p in self.posts) / len(self.posts), 2),
            'by_post_type': self.analyze_by_post_type(),
            'by_kmu_segment': self.analyze_by_kmu_segment(),
            'by_hook_variant': self.analyze_by_hook_variant(),
            'top_3_by_engagement': [
                {k: v for k, v in post.items() if k in ['post_id', 'post_type', 'engagement_rate', 'clicks']}
                for post in self.get_top_performers('engagement_rate', 3)
            ]
        }
        return report

    def print_summary(self):
        """Print human-readable summary"""
        report = self.generate_report()

        print("\n" + "="*70)
        print("📊 LINKEDIN POST PERFORMANCE REPORT")
        print("="*70)
        print(f"Generated: {report['generated_at']}")
        print(f"Total Posts Analyzed: {report['total_posts']}")
        print(f"Total Impressions: {report['total_impressions']:,}")
        print(f"Avg Engagement Rate: {report['avg_engagement_rate']}%")

        print("\n📈 BY POST TYPE:")
        print("-" * 70)
        for post_type, metrics in sorted(report['by_post_type'].items(),
                                         key=lambda x: x[1]['avg_engagement_rate'],
                                         reverse=True):
            print(f"  {post_type}:")
            print(f"    Count: {metrics['count']} | Avg Engagement: {metrics['avg_engagement_rate']}% | Avg CTR: {metrics['avg_ctr']}%")
            print(f"    Total Clicks: {metrics['total_clicks']} | Total Comments: {metrics['total_comments']}")

        print("\n🎯 BY KMU SEGMENT:")
        print("-" * 70)
        for segment, metrics in sorted(report['by_kmu_segment'].items(),
                                       key=lambda x: x[1]['avg_engagement_rate'],
                                       reverse=True):
            print(f"  {segment}:")
            print(f"    Count: {metrics['count']} | Avg Engagement: {metrics['avg_engagement_rate']}% | Avg CTR: {metrics['avg_ctr']}%")

        print("\n🔥 BY HOOK VARIANT (Top Performers):")
        print("-" * 70)
        for hook, metrics in sorted(report['by_hook_variant'].items(),
                                    key=lambda x: x[1]['avg_engagement_rate'],
                                    reverse=True):
            print(f"  {hook}: {metrics['avg_engagement_rate']}% engagement | Best: {metrics['best_performer']}")

        print("\n⭐ TOP 3 POSTS:")
        print("-" * 70)
        for i, post in enumerate(report['top_3_by_engagement'], 1):
            print(f"  {i}. {post['post_id']} ({post['post_type']}) - {post['engagement_rate']}% engagement | {post['clicks']} clicks")

        print("\n" + "="*70)
        return report

if __name__ == '__main__':
    csv_file = Path(__file__).parent / 'posts-tracker.csv'
    analyzer = PerformanceAnalyzer(str(csv_file))
    report = analyzer.print_summary()

    # Save JSON report
    json_file = Path(__file__).parent / 'performance-report.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Report saved to {json_file}")
