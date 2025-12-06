-- Migration: Add quantity and unit columns to ingredients table
-- Date: 2025-12-06

-- Add quantity column (nullable)
ALTER TABLE ingredients ADD COLUMN quantity REAL;

-- Add unit column (nullable)
ALTER TABLE ingredients ADD COLUMN unit TEXT;

-- Verify migration
SELECT name, quantity, unit FROM ingredients LIMIT 5;
