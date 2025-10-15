-- Created on 2025-10-14
-- Purpose: Initiate staging + warehouse schemas for Coffee Canary

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
