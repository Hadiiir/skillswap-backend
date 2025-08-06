-- Create database schema for SkillSwap
-- This script creates the necessary tables and indexes

-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_skills_category_status ON skills_skill(category_id, status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_skills_points ON skills_skill(points_required);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_skills_rating ON skills_skill(average_rating);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_skills_created ON skills_skill(created_at);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_points_user_type ON points_pointstransaction(user_id, transaction_type);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_points_status ON points_pointstransaction(status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_points_created ON points_pointstransaction(created_at);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_buyer_status ON points_order(buyer_id, status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_seller_status ON points_order(seller_id, status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status ON points_order(status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_created ON points_order(created_at);

-- Create full-text search indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_skills_search ON skills_skill USING gin(to_tsvector('english', title || ' ' || description || ' ' || tags));
