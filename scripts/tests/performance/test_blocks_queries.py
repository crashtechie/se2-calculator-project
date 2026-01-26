#!/usr/bin/env python
"""
Performance test script for Blocks views.

Tests the number of database queries executed by different views
to identify N+1 query problems and optimization opportunities.

Usage:
    uv run python scripts/tests/performance/test_blocks_queries.py
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'se2CalcProject.settings')
django.setup()

from django.test.utils import setup_test_environment
from django.db import connection, reset_queries
from django.test import Client
from blocks.models import Block


def test_list_view_queries():
    """Test query count for blocks list view."""
    client = Client()
    reset_queries()
    
    response = client.get('/blocks/')
    query_count = len(connection.queries)
    
    print(f"✓ List view queries: {query_count}")
    
    if query_count > 10:
        print(f"  ⚠️  WARNING: High query count detected!")
    
    return query_count


def test_detail_view_queries():
    """Test query count for blocks detail view."""
    client = Client()
    block = Block.objects.first()
    
    if not block:
        print("✗ No blocks found in database. Please load fixtures first.")
        return 0
    
    reset_queries()
    response = client.get(f'/blocks/{block.block_id}/')
    query_count = len(connection.queries)
    
    print(f"✓ Detail view queries: {query_count}")
    
    if query_count > 20:
        print(f"  ⚠️  WARNING: High query count detected!")
    
    return query_count


def test_create_view_queries():
    """Test query count for blocks create view (GET)."""
    client = Client()
    reset_queries()
    
    response = client.get('/blocks/create/')
    query_count = len(connection.queries)
    
    print(f"✓ Create view (GET) queries: {query_count}")
    
    if query_count > 15:
        print(f"  ⚠️  WARNING: High query count detected!")
    
    return query_count


def test_update_view_queries():
    """Test query count for blocks update view (GET)."""
    client = Client()
    block = Block.objects.first()
    
    if not block:
        print("✗ No blocks found in database. Please load fixtures first.")
        return 0
    
    reset_queries()
    response = client.get(f'/blocks/{block.block_id}/update/')
    query_count = len(connection.queries)
    
    print(f"✓ Update view (GET) queries: {query_count}")
    
    if query_count > 20:
        print(f"  ⚠️  WARNING: High query count detected!")
    
    return query_count


def print_query_details():
    """Print detailed query information for debugging."""
    if connection.queries:
        print("\n" + "="*60)
        print("QUERY DETAILS:")
        print("="*60)
        for idx, query in enumerate(connection.queries, 1):
            print(f"\nQuery {idx}:")
            print(f"  SQL: {query['sql'][:200]}...")
            print(f"  Time: {query['time']}s")


def main():
    """Run all performance tests."""
    print("="*60)
    print("BLOCKS VIEWS PERFORMANCE TEST")
    print("="*60)
    print()
    
    # Setup test environment
    setup_test_environment()
    
    # Run tests
    results = {}
    results['list'] = test_list_view_queries()
    results['detail'] = test_detail_view_queries()
    results['create'] = test_create_view_queries()
    results['update'] = test_update_view_queries()
    
    # Summary
    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)
    total_queries = sum(results.values())
    print(f"Total queries across all views: {total_queries}")
    print()
    
    # Performance recommendations
    if any(v > 15 for v in results.values()):
        print("⚠️  RECOMMENDATIONS:")
        print("  - Consider using select_related() for ForeignKey relationships")
        print("  - Consider using prefetch_related() for ManyToMany/reverse FK")
        print("  - Review template tags that may trigger additional queries")
        print("  - Consider caching frequently accessed data")
    else:
        print("✓ Query counts look good!")
    
    print()
    print("="*60)


if __name__ == '__main__':
    main()
