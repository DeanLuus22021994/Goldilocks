-- Goldilocks Database Initialization
-- Optimized for edge computing with lightweight schema
-- Follows MODERNIZE, LIGHTWEIGHT, HIGH COMPATIBILITY principles

-- Set session-specific configurations for optimal initialization
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER';
SET SESSION default_storage_engine = 'InnoDB';
SET SESSION character_set_server = utf8mb4;
SET SESSION collation_server = utf8mb4_unicode_ci;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use database with proper error handling
USE goldilocks;

-- Create additional application users for different connection types
-- Primary application user (matches Docker environment)
CREATE USER IF NOT EXISTS 'goldilocks_app'@'%' IDENTIFIED BY 'goldilocks_app_secure_2024';
GRANT ALL PRIVILEGES ON goldilocks.* TO 'goldilocks_app'@'%';

-- Alternative application user (matches application default config)
CREATE USER IF NOT EXISTS 'goldilocks_user'@'%' IDENTIFIED BY 'goldilocks_pass_2024';
GRANT ALL PRIVILEGES ON goldilocks.* TO 'goldilocks_user'@'%';

-- Test user for testing environment
CREATE USER IF NOT EXISTS 'goldilocks_test'@'%' IDENTIFIED BY 'goldilocks_test_2024';
GRANT ALL PRIVILEGES ON goldilocks.* TO 'goldilocks_test'@'%';

-- Read-only user for monitoring/reporting
CREATE USER IF NOT EXISTS 'goldilocks_readonly'@'%' IDENTIFIED BY 'goldilocks_readonly_2024';
GRANT SELECT ON goldilocks.* TO 'goldilocks_readonly'@'%';

-- Flush privileges to ensure users are created
FLUSH PRIVILEGES;

-- Users table for authentication with enhanced security
CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uuid CHAR(36) NOT NULL UNIQUE DEFAULT (UUID()),
    email VARCHAR(320) NOT NULL UNIQUE, -- RFC 5321 max length
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url VARCHAR(2048), -- Extended URL length
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_locked BOOLEAN DEFAULT FALSE,
    failed_login_attempts TINYINT UNSIGNED DEFAULT 0,
    last_failed_login_at TIMESTAMP NULL,
    role ENUM('user', 'admin', 'moderator', 'viewer') DEFAULT 'user',
    created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3), -- Microsecond precision
    updated_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    last_login_at TIMESTAMP(3) NULL,
    deleted_at TIMESTAMP(3) NULL, -- Soft delete support

    INDEX idx_email (email) USING BTREE,
    INDEX idx_username (username) USING BTREE,
    INDEX idx_uuid (uuid) USING HASH,
    INDEX idx_active_verified (is_active, is_verified) USING BTREE,
    INDEX idx_role (role) USING BTREE,
    INDEX idx_created (created_at) USING BTREE,
    INDEX idx_soft_delete (deleted_at) USING BTREE,

    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_username_format CHECK (username REGEXP '^[a-zA-Z0-9_-]+$'),
    CONSTRAINT chk_failed_attempts CHECK (failed_login_attempts <= 10)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED
  COMMENT='User accounts with enhanced security features';

-- User sessions with enhanced security and performance
CREATE TABLE IF NOT EXISTS user_sessions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL UNIQUE,
    user_id BIGINT UNSIGNED NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    csrf_token VARCHAR(255),
    fingerprint_hash VARCHAR(255),
    created_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3),
    expires_at TIMESTAMP(3) NOT NULL,
    last_activity_at TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    is_active BOOLEAN DEFAULT TRUE,
    device_info JSON,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_session_id (session_id) USING HASH,
    INDEX idx_user_active (user_id, is_active) USING BTREE,
    INDEX idx_expires (expires_at) USING BTREE,
    INDEX idx_last_activity (last_activity_at) USING BTREE,
    INDEX idx_ip_address (ip_address) USING BTREE,

    CONSTRAINT chk_session_duration CHECK (expires_at > created_at)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED
  COMMENT='User session management with enhanced security';

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

-- Create default admin user with modern security
-- Using stronger password hash (Argon2 format placeholder - actual hashing done by application)
INSERT INTO users (email, username, password_hash, full_name, role, is_active, is_verified) VALUES
('admin@goldilocks.local', 'admin', '$argon2id$v=19$m=65536,t=3,p=4$placeholder', 'System Administrator', 'admin', TRUE, TRUE)
ON DUPLICATE KEY UPDATE
    updated_at = CURRENT_TIMESTAMP(3),
    full_name = VALUES(full_name),
    is_active = VALUES(is_active),
    is_verified = VALUES(is_verified);

-- Create demo user for development/testing (if not in production)
INSERT INTO users (email, username, password_hash, full_name, role, is_active, is_verified) VALUES
('demo@goldilocks.local', 'demo', '$argon2id$v=19$m=65536,t=3,p=4$placeholder', 'Demo User', 'user', TRUE, TRUE)
ON DUPLICATE KEY UPDATE
    updated_at = CURRENT_TIMESTAMP(3),
    full_name = VALUES(full_name);

-- Create admin and demo profiles with enhanced metadata
INSERT INTO user_profiles (user_id, bio, company, job_title, timezone, language, theme)
SELECT u.id,
       CASE
           WHEN u.username = 'admin' THEN 'System Administrator with full access privileges'
           WHEN u.username = 'demo' THEN 'Demo user for testing and evaluation purposes'
           ELSE 'Default user profile'
       END as bio,
       'Goldilocks Platform' as company,
       CASE
           WHEN u.username = 'admin' THEN 'System Administrator'
           WHEN u.username = 'demo' THEN 'Demo User'
           ELSE 'User'
       END as job_title,
       'UTC' as timezone,
       'en' as language,
       'auto' as theme
FROM users u
WHERE u.username IN ('admin', 'demo')
ON DUPLICATE KEY UPDATE
    updated_at = CURRENT_TIMESTAMP(3),
    bio = VALUES(bio),
    company = VALUES(company),
    job_title = VALUES(job_title);

-- Performance optimizations for edge computing and high availability
-- Modern InnoDB settings optimized for containerized environments
SET SESSION innodb_strict_mode = ON;

-- Create performance schema views for monitoring (if available)
-- These will fail gracefully if performance_schema is disabled
SET @sql = IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'performance_schema') > 0,
    'CREATE OR REPLACE VIEW v_session_activity AS
     SELECT processlist_id, processlist_user, processlist_host, processlist_command,
            processlist_time, processlist_info
     FROM performance_schema.processlist
     WHERE processlist_user IS NOT NULL AND processlist_user != "system user"',
    'SELECT "Performance schema not available" as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Optimize table maintenance
OPTIMIZE TABLE users, user_sessions, user_profiles, activity_logs, system_settings;

-- Update table statistics for query optimizer
ANALYZE TABLE users, user_sessions, user_profiles, activity_logs, system_settings;

-- Set up automated maintenance events (if event scheduler is enabled)
SET @sql = IF(@@event_scheduler = 'ON',
    'CREATE EVENT IF NOT EXISTS evt_cleanup_expired_sessions
     ON SCHEDULE EVERY 1 HOUR
     STARTS CURRENT_TIMESTAMP
     DO DELETE FROM user_sessions WHERE expires_at < NOW() AND is_active = FALSE;

     CREATE EVENT IF NOT EXISTS evt_cleanup_old_activity_logs
     ON SCHEDULE EVERY 1 DAY
     STARTS CURRENT_TIMESTAMP + INTERVAL 1 HOUR
     DO DELETE FROM activity_logs WHERE created_at < NOW() - INTERVAL 90 DAY;',
    'SELECT "Event scheduler disabled, skipping automated maintenance" as message');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Log successful initialization with enhanced metadata
INSERT INTO activity_logs (action, resource_type, metadata) VALUES
('database_initialized', 'system', JSON_OBJECT(
    'timestamp', NOW(3),
    'version', '2.0.0',
    'schema_version', '1.0.0',
    'tables_created', 5,
    'default_users_created', 2,
    'performance_optimizations', TRUE,
    'edge_computing_ready', TRUE,
    'init_script', '01-init-database.sql'
));

-- Verify database integrity
CHECKSUM TABLE users, user_sessions, user_profiles, activity_logs, system_settings;

-- Final commit with success confirmation
COMMIT;

-- Display initialization summary
SELECT
    'Database initialization completed successfully' as status,
    COUNT(DISTINCT table_name) as tables_created,
    NOW(3) as completed_at
FROM information_schema.tables
WHERE table_schema = 'goldilocks'
  AND table_name IN ('users', 'user_sessions', 'user_profiles', 'activity_logs', 'system_settings');
