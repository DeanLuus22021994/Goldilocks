"""Tests for utility functions."""

import time
from unittest.mock import patch

from goldilocks.utils import (
    format_duration,
    generate_slug,
    is_safe_url,
    mask_sensitive_data,
    retry,
    safe_get,
    sanitize_filename,
    timer,
    truncate_string,
    validate_email,
)


class TestUtilityFunctions:
    """Test suite for utility functions."""

    def test_safe_get_existing_key(self) -> None:
        """Test safe_get with existing key."""
        data = {"key1": "value1", "key2": 42}

        result = safe_get(data, "key1")
        assert result == "value1"

        result = safe_get(data, "key2")
        assert result == 42

    def test_safe_get_missing_key_default(self) -> None:
        """Test safe_get with missing key and default value."""
        data = {"key1": "value1"}

        result = safe_get(data, "missing", "default")
        assert result == "default"

        result = safe_get(data, "missing")
        assert result is None

    def test_format_duration_milliseconds(self) -> None:
        """Test format_duration for milliseconds."""
        result = format_duration(0.001)
        assert result == "1.0ms"

        result = format_duration(0.5)
        assert result == "500.0ms"

    def test_format_duration_seconds(self) -> None:
        """Test format_duration for seconds."""
        result = format_duration(1.0)
        assert result == "1.00s"

        result = format_duration(30.5)
        assert result == "30.50s"

    def test_format_duration_minutes(self) -> None:
        """Test format_duration for minutes."""
        result = format_duration(60)
        assert result == "1.0m"

        result = format_duration(150)
        assert result == "2.5m"

    def test_format_duration_hours(self) -> None:
        """Test format_duration for hours."""
        result = format_duration(3600)
        assert result == "1.0h"

        result = format_duration(7200)
        assert result == "2.0h"

    def test_validate_email_valid(self) -> None:
        """Test validate_email with valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@numbers.net"
        ]

        for email in valid_emails:
            assert validate_email(email), f"Should validate {email}"

    def test_validate_email_invalid(self) -> None:
        """Test validate_email with invalid email addresses."""
        invalid_emails = [
            "not-an-email",
            "@domain.com",
            "user@",
            "user@domain",
            "user..double.dot@domain.com",
            ""
        ]

        for email in invalid_emails:
            assert not validate_email(email), f"Should not validate {email}"

    def test_sanitize_filename_dangerous_chars(self) -> None:
        """Test sanitize_filename removes dangerous characters."""
        dangerous = 'file<>:"/\\|?*name.txt'
        result = sanitize_filename(dangerous)
        assert result == "file_________name.txt"

    def test_sanitize_filename_empty(self) -> None:
        """Test sanitize_filename with empty or whitespace input."""
        assert sanitize_filename("") == "unnamed"
        assert sanitize_filename("   ") == "unnamed"
        assert sanitize_filename("...") == "unnamed"

    def test_sanitize_filename_normal(self) -> None:
        """Test sanitize_filename with normal filename."""
        result = sanitize_filename("normal_file.txt")
        assert result == "normal_file.txt"

    def test_generate_slug_normal_text(self) -> None:
        """Test generate_slug with normal text."""
        result = generate_slug("Hello World")
        assert result == "hello-world"

        result = generate_slug("This is a Test!")
        assert result == "this-is-a-test"

    def test_generate_slug_special_characters(self) -> None:
        """Test generate_slug removes special characters."""
        result = generate_slug("Hello @#$% World!!!")
        assert result == "hello-world"

    def test_generate_slug_max_length(self) -> None:
        """Test generate_slug respects max length."""
        long_text = "This is a very long title that exceeds the maximum length"
        result = generate_slug(long_text, max_length=20)
        assert len(result) <= 20
        assert not result.endswith("-")

    def test_generate_slug_empty(self) -> None:
        """Test generate_slug with empty or invalid input."""
        assert generate_slug("") == "untitled"
        assert generate_slug("!@#$%^&*()") == "untitled"

    def test_truncate_string_short_text(self) -> None:
        """Test truncate_string with text shorter than max length."""
        text = "Short text"
        result = truncate_string(text, max_length=20)
        assert result == "Short text"

    def test_truncate_string_long_text(self) -> None:
        """Test truncate_string with text longer than max length."""
        text = "This is a very long text that needs to be truncated"
        result = truncate_string(text, max_length=20)
        assert len(result) <= 20
        assert result.endswith("...")

    def test_truncate_string_custom_suffix(self) -> None:
        """Test truncate_string with custom suffix."""
        text = "Long text that needs truncation"
        result = truncate_string(text, max_length=15, suffix=" [more]")
        assert result.endswith(" [more]")
        assert len(result) <= 15

    def test_is_safe_url_safe(self) -> None:
        """Test is_safe_url with safe URLs."""
        safe_urls = [
            "/path/to/resource",
            "/user/profile",
            "/dashboard",
            "/"
        ]

        for url in safe_urls:
            assert is_safe_url(url), f"Should be safe: {url}"

    def test_is_safe_url_unsafe(self) -> None:
        """Test is_safe_url with unsafe URLs."""
        unsafe_urls = [
            "//evil.com/path",
            "http://external.com",
            "https://malicious.site",
            "",
            "javascript:alert('xss')"
        ]

        for url in unsafe_urls:
            assert not is_safe_url(url), f"Should be unsafe: {url}"

    def test_mask_sensitive_data_email(self) -> None:
        """Test mask_sensitive_data with email address."""
        result = mask_sensitive_data("user@example.com")
        assert result == "user***********"

    def test_mask_sensitive_data_short(self) -> None:
        """Test mask_sensitive_data with short string."""
        result = mask_sensitive_data("abc", visible_chars=4)
        assert result == "***"

    def test_mask_sensitive_data_custom_visible(self) -> None:
        """Test mask_sensitive_data with custom visible characters."""
        result = mask_sensitive_data("1234567890", visible_chars=2)
        assert result == "12********"


class TestRetryDecorator:
    """Test suite for retry decorator."""

    def test_retry_success_first_attempt(self) -> None:
        """Test retry decorator with successful first attempt."""
        call_count = 0

        @retry(max_attempts=3)
        def successful_function() -> str:
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_function()
        assert result == "success"
        assert call_count == 1

    def test_retry_success_after_failures(self) -> None:
        """Test retry decorator with success after failures."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def flaky_function() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = flaky_function()
        assert result == "success"
        assert call_count == 3

    def test_retry_exhausted_attempts(self) -> None:
        """Test retry decorator when all attempts are exhausted."""
        call_count = 0

        @retry(max_attempts=2, delay=0.01)
        def failing_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        try:
            failing_function()
            assert False, "Should have raised exception"
        except ValueError as e:
            assert str(e) == "Always fails"
            assert call_count == 2


class TestTimerDecorator:
    """Test suite for timer decorator."""

    def test_timer_measures_execution_time(self) -> None:
        """Test that timer decorator measures execution time."""

        @timer
        def timed_function() -> str:
            time.sleep(0.01)  # Sleep for 10ms
            return "result"

        # Capture stdout to check timing output
        with patch('builtins.print') as mock_print:
            result = timed_function()
            assert result == "result"
            mock_print.assert_called_once()

            # Check that timing was printed
            call_args = mock_print.call_args[0][0]
            assert "timed_function took" in call_args
            assert "seconds" in call_args

    def test_timer_preserves_function_metadata(self) -> None:
        """Test that timer decorator preserves function metadata."""

        @timer
        def documented_function():
            """This function has documentation."""
            return "result"

        assert documented_function.__name__ == "documented_function"
        assert "This function has documentation" in documented_function.__doc__

    def test_timer_handles_exceptions(self) -> None:
        """Test that timer decorator handles exceptions properly."""

        @timer
        def failing_function():
            raise ValueError("Test exception")

        with patch('builtins.print'):
            try:
                failing_function()
                assert False, "Should have raised exception"
            except ValueError as e:
                assert str(e) == "Test exception"


class TestUtilityIntegration:
    """Integration tests for utility functions working together."""

    def test_email_validation_and_masking(self) -> None:
        """Test email validation combined with masking."""
        email = "user@example.com"

        # Validate email first
        assert validate_email(email)

        # Then mask for logging
        masked = mask_sensitive_data(email)
        assert masked.startswith("user")
        assert "example.com" not in masked

    def test_filename_sanitization_and_truncation(self) -> None:
        """Test filename sanitization combined with truncation."""
        dangerous_long_filename = "Very<>Long|File?Name*With/Dangerous\\Characters.txt"

        # Sanitize first
        clean_filename = sanitize_filename(dangerous_long_filename)
        assert '<>' not in clean_filename
        assert '|?' not in clean_filename

        # Then truncate if needed
        final_filename = truncate_string(clean_filename, max_length=20)
        assert len(final_filename) <= 20

    def test_slug_generation_with_truncation(self) -> None:
        """Test slug generation with built-in truncation."""
        long_title = "This is an extremely long blog post title that needs to be converted to a URL-friendly slug"

        slug = generate_slug(long_title, max_length=30)

        assert len(slug) <= 30
        assert slug.replace("-", "").isalnum()
        assert not slug.endswith("-")
        assert slug.startswith("this-is-an")
