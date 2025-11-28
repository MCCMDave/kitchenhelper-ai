-- Migration: Add strict_ingredients_only column to diet_profiles table
-- Date: 2025-11-28
-- Description: Adds boolean column to control whether profiles use strict ingredient filtering

ALTER TABLE diet_profiles ADD COLUMN strict_ingredients_only INTEGER DEFAULT 0;
