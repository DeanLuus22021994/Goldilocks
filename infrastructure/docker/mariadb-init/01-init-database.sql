-- Goldilocks Database Initialization
-- Optimized for edge computing with lightweight schema

USE goldilocks;

-- Enable strict mode and proper charset
SET sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    role ENUM('user', 'admin', 'moderator') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,

    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_uuid (uuid),
    INDEX idx_active (is_active),
    INDEX idx_created (created_at)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED;

-- User sessions for authentication management
CREATE TABLE IF NOT EXISTS user_sessions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL UNIQUE,
    user_id BIGINT UNSIGNED NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_user_id (user_id),
    INDEX idx_expires (expires_at),
    INDEX idx_active (is_active)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED;

-- User profiles for extended information
CREATE TABLE IF NOT EXISTS user_profiles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    bio TEXT,
    location VARCHAR(255),
    website VARCHAR(500),
    company VARCHAR(255),
    job_title VARCHAR(255),
    timezone VARCHAR(64) DEFAULT 'UTC',
    language VARCHAR(8) DEFAULT 'en',
    theme ENUM('light', 'dark', 'auto') DEFAULT 'auto',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED;

-- Activity logs for audit and analytics
CREATE TABLE IF NOT EXISTS activity_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    action VARCHAR(64) NOT NULL,
    resource_type VARCHAR(64),
    resource_id VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED;

-- System settings for application configuration
CREATE TABLE IF NOT EXISTS system_settings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    key_name VARCHAR(255) NOT NULL UNIQUE,
    value_text TEXT,
    value_type ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_key_name (key_name),
    INDEX idx_public (is_public)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED;

-- Insert default system settings
INSERT INTO system_settings (key_name, value_text, value_type, description, is_public) VALUES
('app_name', 'Goldilocks', 'string', 'Application name', TRUE),
('app_version', '1.0.0', 'string', 'Application version', TRUE),
('registration_enabled', 'true', 'boolean', 'Enable user registration', FALSE),
('email_verification_required', 'false', 'boolean', 'Require email verification', FALSE),
('session_timeout_hours', '24', 'integer', 'Session timeout in hours', FALSE),
('max_login_attempts', '5', 'integer', 'Maximum login attempts before lockout', FALSE)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- Create default admin user (password: admin123!)
-- Password hash for 'admin123!' using bcrypt with cost 12
INSERT INTO users (email, username, password_hash, full_name, role, is_active, is_verified) VALUES
('admin@goldilocks.local', 'admin', '$2b$12$LQv3c4yqCukkAr1AhRVDnOJgYJ7HvX4qhTyYjHvg/WWELJQRdBgKS', 'Administrator', 'admin', TRUE, TRUE)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- Create admin profile
INSERT INTO user_profiles (user_id, bio, company, job_title)
SELECT id, 'System Administrator', 'Goldilocks', 'Administrator'
FROM users WHERE username = 'admin'
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- Performance optimizations for edge computing
-- Optimize InnoDB settings
SET GLOBAL innodb_buffer_pool_size = 268435456; -- 256MB
SET GLOBAL innodb_log_file_size = 67108864;     -- 64MB
SET GLOBAL innodb_flush_log_at_trx_commit = 2;  -- Faster commits
SET GLOBAL query_cache_size = 33554432;         -- 32MB query cache

-- Create indexes for common queries
ANALYZE TABLE users, user_sessions, user_profiles, activity_logs, system_settings;

-- Log initialization completion
INSERT INTO activity_logs (action, resource_type, metadata) VALUES
('database_initialized', 'system', JSON_OBJECT('timestamp', NOW(), 'version', '1.0.0'));

COMMIT;
